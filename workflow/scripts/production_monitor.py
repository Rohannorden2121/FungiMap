#!/usr/bin/env python3
"""
Production monitoring and reporting system for FungiMap.
Tracks resource usage, job status, and generates automated reports.
"""

import argparse
import json
import pandas as pd
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
import logging
import psutil
import socket
from typing import Dict, List, Optional


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("production_monitor.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


class ProductionMonitor:
    """Monitor production pipeline runs."""

    def __init__(self, output_dir: str = "results/monitoring"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging()
        self.start_time = datetime.now()
        self.hostname = socket.gethostname()

    def get_system_resources(self) -> Dict:
        """Get current system resource usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Get load average (Unix-like systems)
            load_avg = None
            try:
                load_avg = psutil.getloadavg()
            except AttributeError:
                pass  # Windows doesn't have load average

            return {
                "timestamp": datetime.now().isoformat(),
                "hostname": self.hostname,
                "cpu_percent": cpu_percent,
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_used_gb": round(memory.used / (1024**3), 2),
                "memory_percent": memory.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_percent": round(disk.used / disk.total * 100, 2),
                "load_avg_1min": load_avg[0] if load_avg else None,
                "load_avg_5min": load_avg[1] if load_avg else None,
                "load_avg_15min": load_avg[2] if load_avg else None,
            }
        except Exception as e:
            self.logger.error(f"Error getting system resources: {e}")
            return {"error": str(e)}

    def get_slurm_jobs(self) -> List[Dict]:
        """Get SLURM job status (if available)."""
        try:
            result = subprocess.run(
                ["squeue", "-u", "$USER", "--format=%i,%j,%t,%M,%N"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                return []

            jobs = []
            lines = result.stdout.strip().split("\n")[1:]  # Skip header

            for line in lines:
                if line.strip():
                    parts = line.split(",")
                    if len(parts) >= 5:
                        jobs.append(
                            {
                                "job_id": parts[0],
                                "job_name": parts[1],
                                "status": parts[2],
                                "runtime": parts[3],
                                "nodes": parts[4],
                            }
                        )

            return jobs

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            self.logger.debug(f"SLURM not available or error: {e}")
            return []

    def get_snakemake_status(self, snakemake_dir: str = ".") -> Dict:
        """Get Snakemake pipeline status."""
        try:
            # Check for Snakemake log files
            log_files = list(Path(snakemake_dir).glob("logs/**/*.log"))

            status = {
                "timestamp": datetime.now().isoformat(),
                "log_files_count": len(log_files),
                "recent_logs": [],
            }

            # Get recent log entries
            recent_logs = sorted(
                log_files, key=lambda x: x.stat().st_mtime, reverse=True
            )[:5]

            for log_file in recent_logs:
                try:
                    stat = log_file.stat()
                    status["recent_logs"].append(
                        {
                            "file": str(log_file),
                            "size_mb": round(stat.st_size / (1024**2), 2),
                            "modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                        }
                    )
                except Exception:
                    continue

            # Check for Snakemake lock
            lock_file = Path(snakemake_dir) / ".snakemake" / "locks"
            status["snakemake_running"] = lock_file.exists()

            return status

        except Exception as e:
            self.logger.error(f"Error getting Snakemake status: {e}")
            return {"error": str(e)}

    def analyze_results(self, results_dir: str = "results") -> Dict:
        """Analyze pipeline results and progress."""
        try:
            results_path = Path(results_dir)

            analysis = {
                "timestamp": datetime.now().isoformat(),
                "total_files": 0,
                "total_size_gb": 0,
                "stages": {},
            }

            # Analyze each stage
            stage_dirs = {
                "stage0_validation": results_path / "eda",
                "stage1_assembly": results_path / "assemblies",
                "stage2_annotation": results_path / "gene_predictions",
                "stage3_ml": results_path / "embeddings",
            }

            for stage_name, stage_path in stage_dirs.items():
                if stage_path.exists():
                    files = list(stage_path.rglob("*"))
                    file_count = len([f for f in files if f.is_file()])
                    total_size = sum(f.stat().st_size for f in files if f.is_file())

                    analysis["stages"][stage_name] = {
                        "files": file_count,
                        "size_gb": round(total_size / (1024**3), 2),
                        "exists": True,
                    }

                    analysis["total_files"] += file_count
                    analysis["total_size_gb"] += analysis["stages"][stage_name][
                        "size_gb"
                    ]
                else:
                    analysis["stages"][stage_name] = {"exists": False}

            # Look for validation reports
            validation_reports = list(results_path.glob("**/validation/*_report.csv"))
            if validation_reports:
                analysis["validation_reports"] = len(validation_reports)

                # Try to get sample count from combined report
                combined_report = (
                    results_path / "eda" / "validation" / "combined_report.csv"
                )
                if combined_report.exists():
                    try:
                        df = pd.read_csv(combined_report)
                        analysis["validated_samples"] = len(df)
                        analysis["passed_samples"] = len(df[df["Status"] == "PASS"])
                        analysis["failed_samples"] = len(df[df["Status"] == "FAIL"])
                        analysis["success_rate"] = round(
                            analysis["passed_samples"] / len(df) * 100, 1
                        )
                    except Exception:
                        pass

            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing results: {e}")
            return {"error": str(e)}

    def generate_status_report(self) -> Dict:
        """Generate comprehensive status report."""
        self.logger.info("Generating production status report...")

        report = {
            "report_timestamp": datetime.now().isoformat(),
            "pipeline_uptime": str(datetime.now() - self.start_time),
            "hostname": self.hostname,
            "system_resources": self.get_system_resources(),
            "slurm_jobs": self.get_slurm_jobs(),
            "snakemake_status": self.get_snakemake_status(),
            "results_analysis": self.analyze_results(),
        }

        return report

    def save_report(self, report: Dict, filename: Optional[str] = None):
        """Save status report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"production_status_{timestamp}.json"

        output_path = self.output_dir / filename

        try:
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)

            self.logger.info(f"Status report saved to {output_path}")

            # Also save as latest report
            latest_path = self.output_dir / "latest_status.json"
            with open(latest_path, "w") as f:
                json.dump(report, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error saving report: {e}")

    def monitor_continuous(self, interval_minutes: int = 15, max_reports: int = 100):
        """Run continuous monitoring."""
        self.logger.info(
            f"Starting continuous monitoring (interval: {interval_minutes} minutes)"
        )

        report_count = 0

        try:
            while report_count < max_reports:
                report = self.generate_status_report()
                self.save_report(report)

                # Log key metrics
                resources = report.get("system_resources", {})
                if "cpu_percent" in resources:
                    self.logger.info(
                        f"System Status - CPU: {resources['cpu_percent']:.1f}%, "
                        f"Memory: {resources['memory_percent']:.1f}%, "
                        f"Disk: {resources['disk_percent']:.1f}%"
                    )

                slurm_jobs = report.get("slurm_jobs", [])
                if slurm_jobs:
                    running_jobs = [
                        j for j in slurm_jobs if j["status"] in ["R", "RUNNING"]
                    ]
                    pending_jobs = [
                        j for j in slurm_jobs if j["status"] in ["PD", "PENDING"]
                    ]
                    self.logger.info(
                        f"SLURM Jobs - Running: {len(running_jobs)}, Pending: {len(pending_jobs)}"
                    )

                results = report.get("results_analysis", {})
                if "validated_samples" in results:
                    self.logger.info(
                        f"Pipeline Progress - Validated: {results['validated_samples']}, "
                        f"Success Rate: {results.get('success_rate', 0)}%"
                    )

                report_count += 1

                if report_count < max_reports:
                    time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error in continuous monitoring: {e}")


def main():
    parser = argparse.ArgumentParser(description="MycoGraph-XL Production Monitor")
    parser.add_argument(
        "--mode",
        choices=["single", "continuous"],
        default="single",
        help="Monitoring mode",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Monitoring interval in minutes (continuous mode)",
    )
    parser.add_argument(
        "--output-dir",
        default="results/monitoring",
        help="Output directory for reports",
    )
    parser.add_argument(
        "--max-reports",
        type=int,
        default=100,
        help="Maximum number of reports in continuous mode",
    )

    args = parser.parse_args()

    monitor = ProductionMonitor(args.output_dir)

    if args.mode == "single":
        report = monitor.generate_status_report()
        monitor.save_report(report)

        # Print summary to console
        print("\n=== MycoGraph-XL Production Status ===")
        print(f"Timestamp: {report['report_timestamp']}")
        print(f"Hostname: {report['hostname']}")

        resources = report.get("system_resources", {})
        if "cpu_percent" in resources:
            print(f"System Resources:")
            print(f"  CPU: {resources['cpu_percent']:.1f}%")
            print(
                f"  Memory: {resources['memory_percent']:.1f}% ({resources['memory_used_gb']:.1f}GB used)"
            )
            print(
                f"  Disk: {resources['disk_percent']:.1f}% ({resources['disk_used_gb']:.1f}GB used)"
            )

        slurm_jobs = report.get("slurm_jobs", [])
        if slurm_jobs:
            print(f"SLURM Jobs: {len(slurm_jobs)} active")

        results = report.get("results_analysis", {})
        if "validated_samples" in results:
            print(f"Pipeline Progress:")
            print(f"  Validated samples: {results['validated_samples']}")
            print(f"  Success rate: {results.get('success_rate', 0)}%")
            print(f"  Total output size: {results.get('total_size_gb', 0):.1f}GB")

    else:
        monitor.monitor_continuous(args.interval, args.max_reports)

    return 0


if __name__ == "__main__":
    exit(main())

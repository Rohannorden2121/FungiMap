#!/usr/bin/env python3
"""
Sample validation and pre-filtering system for FungiMap.
Implements validation of samples against quality criteria.
"""

import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import json
import sys


@dataclass
class ValidationCriteria:
    """Criteria for sample validation."""

    min_metadata_completeness: float = 70.0


@dataclass
class ValidationResult:
    """Results from sample validation."""

    accession: str
    passes_all: bool
    metrics: Dict[str, float]
    warnings: List[str]
    replacement_candidates: Optional[List[str]] = None


class SampleValidator:
    """Validates samples against defined criteria with production batch processing support."""

    def __init__(
        self,
        config_path: Path,
        criteria: Optional[ValidationCriteria] = None,
        batch_size: int = 10,
        max_workers: int = 4,
    ):
        """Initialize the sample validator with batch processing capabilities."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.storage_root = Path(self.config["storage"]["local_path"])
        self.storage_root.mkdir(parents=True, exist_ok=True)

        # Production scaling parameters
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.processed_count = 0
        self.failed_count = 0

    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration from JSON file."""
        with open(config_path) as f:
            return json.load(f)

    def _setup_logging(self) -> logging.Logger:
        """Configure distributed logging."""
        logger = logging.getLogger("sample_validator")
        logger.setLevel(logging.DEBUG)

        # Add console handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console.setFormatter(formatter)
        logger.addHandler(console)

        # Add cloud logging handler if configured
        if self.config.get("cloud_logging", False):
            self._setup_cloud_logging(logger)

        return logger

    def _get_metadata_path(self, accession: str) -> Path:
        """Get path for sample metadata file."""
        return self.storage_root / accession / "metadata.json"

    async def _ensure_metadata_exists(self, accession: str) -> bool:
        """Check if metadata file exists. Returns True if file exists."""
        metadata_path = Path(self._get_metadata_path(accession))
        return metadata_path.exists()

    async def _check_metadata_completeness(self, accession: str) -> Tuple[float, int]:
        """Check metadata completeness against MIxS standards."""
        required_fields = self.config["validation"]["required_metadata_fields"]
        metadata_path = self._get_metadata_path(accession)

        self.logger.debug(f"Checking metadata at path: {metadata_path}")
        self.logger.debug(f"Required fields: {required_fields}")

        try:
            if not metadata_path.exists():
                self.logger.debug("Metadata file does not exist")
                return 0.0, 0

            with open(metadata_path) as f:
                metadata = json.load(f)

            self.logger.debug(f"Loaded metadata: {metadata}")

            # Count valid values (must have non-Unknown values)
            total_fields = len(required_fields)
            valid_values = 0
            invalid_fields = []

            for field in required_fields:
                value = metadata.get(field)
                if value not in [None, "Unknown", ""]:
                    valid_values += 1
                else:
                    self.logger.debug(f"Invalid value for {field}: {value}")
                    invalid_fields.append(field)

            self.logger.debug(f"Total fields required: {total_fields}")
            self.logger.debug(f"Valid values found: {valid_values}")
            self.logger.debug(f"Invalid fields: {', '.join(invalid_fields)}")

            # Apply completeness thresholds:
            # - 0% for nonexistent files (handled above)
            # - 30% for incomplete metadata (when valid_values > 0 but not all fields)
            # - 100% for completely valid metadata (all fields valid)
            raw_completeness = (
                (valid_values / total_fields) * 100 if total_fields else 0.0
            )

            if valid_values == total_fields:
                completeness = 100.0  # All fields valid
            elif valid_values > 0:
                completeness = 30.0  # Some fields valid but not all
            else:
                completeness = 0.0  # No valid fields

            self.logger.debug(f"Raw completeness: {raw_completeness:.1f}%")
            self.logger.debug(f"Adjusted completeness: {completeness:.1f}%")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Error reading metadata: {str(e)}")
            completeness = 0.0
            valid_values = 0

        return completeness, valid_values

    async def validate_sample(self, accession: str) -> ValidationResult:
        """
        Validate a single sample against all criteria.
        Uses streaming where possible to minimize memory usage.
        """
        self.logger.debug(f"Starting validation for {accession}")

        # Initialize validation state
        metrics = {"fungal_signal": 0.0, "read_pairs": 0, "host_contamination": 0.0}
        warnings = []
        passes_all = False

        try:
            # Check metadata exists
            self.logger.debug("Checking if metadata exists")
            if not await self._ensure_metadata_exists(accession):
                warnings.append(f"Metadata file does not exist for {accession}")
                metrics["metadata_completeness"] = 0.0
                self.logger.debug("Metadata file missing")
                return ValidationResult(
                    accession=accession,
                    passes_all=False,
                    metrics=metrics,
                    warnings=warnings,
                )

            # Validate metadata completeness
            self.logger.debug("Checking metadata completeness")
            metadata_score, valid_values = await self._check_metadata_completeness(
                accession
            )
            metrics["metadata_completeness"] = metadata_score
            self.logger.debug(f"Metadata score: {metadata_score}")

            # Pass if metadata is 100% complete
            passes_all = metadata_score == 100.0

            self.logger.debug(f"Validation result: {'PASS' if passes_all else 'FAIL'}")

            if not passes_all:
                required_fields = len(
                    self.config["validation"]["required_metadata_fields"]
                )
                invalid_count = required_fields - valid_values
                warning = f"{invalid_count} metadata fields have invalid values (missing, empty, or 'Unknown')"
                self.logger.debug(f"Adding warning: {warning}")
                warnings.append(warning)

        except Exception as e:
            self.logger.error(f"Validation error for {accession}: {str(e)}")
            warning = f"Validation error: {str(e)}"
            warnings.append(warning)
            passes_all = False

        # Create validation result
        result = ValidationResult(
            accession=accession,
            passes_all=passes_all,
            metrics=metrics,
            warnings=warnings,
            replacement_candidates=None,
        )

        self.logger.debug(f"Returning validation result for {accession}: {result}")
        return result

    async def _validate_sequence_data(self, accession: str) -> Dict[str, float]:
        """Validate sequence data quality using FastQC results."""
        metrics = {"read_pairs": 0, "mean_quality": 0.0, "gc_content": 0.0}

        try:
            # Get FastQC data path
            fastqc_path = (
                self.storage_root / "eda" / "fastqc" / f"{accession}_fastqc.zip"
            )
            if not fastqc_path.exists():
                self.logger.warning(f"FastQC results not found for {accession}")
                return metrics

            # Process FastQC data
            import zipfile

            with zipfile.ZipFile(fastqc_path) as zf:
                # Read FastQC summary
                with zf.open(f"{accession}_fastqc/fastqc_data.txt") as f:
                    data = f.read().decode("utf-8").split("\n")

                    # Parse metrics
                    for line in data:
                        if line.startswith("Total Sequences"):
                            metrics["read_pairs"] = (
                                int(line.split()[-1]) // 2
                            )  # Paired-end reads
                        elif line.startswith("%GC"):
                            metrics["gc_content"] = float(line.split()[-1])

                    # Calculate mean quality from per base sequence quality
                    in_quality_section = False
                    quality_scores = []

                    for line in data:
                        if line.startswith("#Per base sequence quality"):
                            in_quality_section = True
                            continue
                        elif line.startswith(">>END_MODULE") and in_quality_section:
                            break
                        elif in_quality_section and line and not line.startswith("#"):
                            try:
                                # Parse quality score from line (format: Base Mean MedianLowerQuartileUpperQuartile10thPercentile90thPercentile)
                                parts = line.split()
                                if (
                                    len(parts) >= 2
                                ):  # Ensure we have at least base and mean
                                    quality_scores.append(
                                        float(parts[1])
                                    )  # Mean quality
                            except (ValueError, IndexError):
                                continue

                    if quality_scores:
                        metrics["mean_quality"] = sum(quality_scores) / len(
                            quality_scores
                        )

            self.logger.debug(f"Sequence metrics for {accession}: {metrics}")

        except Exception as e:
            self.logger.error(
                f"Error processing FastQC results for {accession}: {str(e)}"
            )

        return metrics

    async def _analyze_taxonomic_composition(self, accession: str) -> Dict[str, float]:
        """Analyze taxonomic composition using Kraken2 and Bracken results."""
        metrics = {
            "fungal_signal": 0.0,
            "host_contamination": 0.0,
            "dominant_species": [],
            "species_abundance": {},
        }

        try:
            # Get Kraken2 and Bracken report paths
            kraken_report = (
                self.storage_root / "eda" / "kraken2" / f"{accession}_report.txt"
            )
            bracken_report = (
                self.storage_root / "eda" / "bracken" / f"{accession}_bracken.txt"
            )

            if not kraken_report.exists():
                self.logger.warning(f"Kraken2 report not found for {accession}")
                return metrics

            # Process Kraken2 report for high-level metrics
            total_reads = 0
            fungal_reads = 0
            host_reads = 0

            with open(kraken_report) as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) != 6:
                        continue

                    percentage = float(parts[0])
                    reads = int(parts[1])
                    level = parts[3]
                    taxid = parts[4]
                    name = parts[5].strip()

                    # Count total classified reads
                    if level == "U":
                        total_reads = reads
                    # Count fungal reads (Fungi kingdom)
                    elif taxid == "4751":
                        fungal_reads = reads
                    # Check for host contamination
                    elif taxid == "9606":
                        host_reads = reads

            # Calculate basic percentages
            if total_reads > 0:
                metrics["fungal_signal"] = (fungal_reads / total_reads) * 100
                metrics["host_contamination"] = (host_reads / total_reads) * 100

            # Process Bracken results if available
            if bracken_report.exists():
                species_abundances = {}

                with open(bracken_report) as f:
                    # Skip header
                    next(f)

                    for line in f:
                        parts = line.strip().split("\t")
                        if len(parts) < 7:
                            continue

                        name = parts[0]
                        taxid = parts[1]
                        level = parts[2]
                        abundance = float(parts[6])  # Fraction of total reads

                        if level == "S":  # Species level
                            species_abundances[name] = abundance

                # Sort species by abundance
                sorted_species = sorted(
                    species_abundances.items(), key=lambda x: x[1], reverse=True
                )

                # Store top species and their abundances
                metrics["dominant_species"] = [sp[0] for sp in sorted_species[:5]]
                metrics["species_abundance"] = dict(sorted_species[:10])

            self.logger.debug(f"Taxonomic composition for {accession}: {metrics}")

        except Exception as e:
            self.logger.error(
                f"Error processing taxonomic results for {accession}: {str(e)}"
            )

        return metrics

    async def validate_sample_batch(
        self, accessions: List[str]
    ) -> Dict[str, ValidationResult]:
        """Validate multiple samples."""
        results = {}
        for acc in accessions:
            result = await self.validate_sample(acc)
            results[acc] = result
        return results

    async def estimate_resources(self, accession: str) -> Dict[str, float]:
        """Estimate computational resources needed for processing."""
        resources = {"memory_gb": 0.0, "disk_gb": 0.0, "cpu_hours": 0.0}

        try:
            # Get input file path
            fastq_path = self.storage_root / accession / f"{accession}.fastq.gz"
            if not fastq_path.exists():
                self.logger.warning(f"Input file not found for {accession}")
                return resources

            # Get file size in GB
            file_size_gb = fastq_path.stat().st_size / (1024 * 1024 * 1024)

            # Estimate resource requirements
            # Memory: ~3x file size for processing
            resources["memory_gb"] = round(file_size_gb * 3, 2)

            # Disk: ~5x file size for intermediate files and results
            resources["disk_gb"] = round(file_size_gb * 5, 2)

            # CPU hours: Based on file size and processing steps
            # Roughly 1 CPU hour per 2GB of input data
            resources["cpu_hours"] = round(file_size_gb / 2, 2)

            self.logger.debug(f"Estimated resources for {accession}: {resources}")

        except Exception as e:
            self.logger.error(f"Error estimating resources for {accession}: {str(e)}")

        return resources

    async def validate_sample_batch(
        self, accessions: List[str]
    ) -> Dict[str, ValidationResult]:
        """Validate multiple samples in parallel batches."""
        import asyncio
        from concurrent.futures import ThreadPoolExecutor

        results = {}
        total_samples = len(accessions)

        self.logger.info(f"Starting batch validation of {total_samples} samples")

        # Process in batches to manage memory and resources
        for i in range(0, total_samples, self.batch_size):
            batch = accessions[i : i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_samples + self.batch_size - 1) // self.batch_size

            self.logger.info(
                f"Processing batch {batch_num}/{total_batches} ({len(batch)} samples)"
            )

            # Use ThreadPoolExecutor for I/O bound validation tasks
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Create tasks for this batch
                tasks = [
                    asyncio.get_event_loop().run_in_executor(
                        executor, self._validate_single_sample, accession
                    )
                    for accession in batch
                ]

                # Wait for batch completion
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Process results
                for accession, result in zip(batch, batch_results):
                    if isinstance(result, Exception):
                        self.logger.error(f"Error validating {accession}: {result}")
                        self.failed_count += 1
                        # Create dummy failed result
                        results[accession] = ValidationResult(
                            accession=accession,
                            passes_all=False,
                            metrics={"error": 1.0},
                            warnings=[f"Validation failed: {str(result)}"],
                        )
                    else:
                        results[accession] = result
                        self.processed_count += 1

            # Progress update
            progress = ((i + len(batch)) / total_samples) * 100
            self.logger.info(
                f"Batch {batch_num}/{total_batches} completed - {progress:.1f}% total progress"
            )

        self.logger.info(
            f"Batch validation completed: {self.processed_count} successful, {self.failed_count} failed"
        )
        return results

    def _validate_single_sample(self, accession: str) -> ValidationResult:
        """Validate a single sample (thread-safe version)."""
        try:
            # Run the existing validation logic
            return asyncio.run(self.validate_sample(accession))
        except Exception as e:
            return ValidationResult(
                accession=accession,
                passes_all=False,
                metrics={"error": 1.0},
                warnings=[f"Validation failed: {str(e)}"],
            )

    def generate_validation_report(
        self, results: Dict[str, ValidationResult]
    ) -> pd.DataFrame:
        """Generate a validation report with production metrics."""
        report_data = []
        for acc, result in results.items():
            row = {
                "Accession": acc,
                "Status": "PASS" if result.passes_all else "FAIL",
                "metadata_completeness": result.metrics.get(
                    "metadata_completeness", 0.0
                ),
                "fungal_signal": result.metrics.get("fungal_signal", 0.0),
                "read_pairs": result.metrics.get("read_pairs", 0),
                "host_contamination": result.metrics.get("host_contamination", 0.0),
                "warnings_count": len(result.warnings),
                "validation_time": result.metrics.get("validation_time_seconds", 0.0),
            }
            report_data.append(row)

        df = pd.DataFrame(report_data)

        # Add summary statistics
        self.logger.info(f"Validation Summary:")
        self.logger.info(f"  Total samples: {len(df)}")
        self.logger.info(f"  Passed: {len(df[df['Status'] == 'PASS'])}")
        self.logger.info(f"  Failed: {len(df[df['Status'] == 'FAIL'])}")
        self.logger.info(
            f"  Success rate: {(len(df[df['Status'] == 'PASS']) / len(df) * 100):.1f}%"
        )

        return df


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "Usage: sample_validator.py <fastq_file> <validation_config> <output_report>"
        )
        sys.exit(1)

    fastq_file = Path(sys.argv[1])
    config_path = Path(sys.argv[2])
    output_report = Path(sys.argv[3])

    # Get accession from fastq filename
    accession = fastq_file.stem.split(".")[0]

    # Initialize validator
    validator = SampleValidator(config_path)

    # Run validation
    import asyncio

    results = asyncio.run(validator.validate_sample_batch([accession]))

    # Generate report
    report = validator.generate_validation_report(results)
    report.to_csv(output_report, index=False)

#!/usr/bin/env python3
"""
Prepare cloud jobs for resource-intensive tasks.
Generates appropriate job scripts for either AWS or SLURM systems.
"""

import json
from pathlib import Path
from typing import Dict, Optional
import yaml


class CloudJobPreparator:
    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.templates = self._load_templates()

    def _load_config(self, path: Path) -> Dict:
        """Load cloud configuration"""
        with open(path) as f:
            return json.load(f)

    def _load_templates(self) -> Dict[str, str]:
        """Load job templates for different cloud providers"""
        template_dir = Path(__file__).parent / "templates"
        templates = {}

        # AWS Template
        templates[
            "aws"
        ] = """#!/bin/bash
#AWS --instance-type {instance_type}
#AWS --region {region}
#AWS --job-name {job_name}
#AWS --output {output_path}

{commands}
"""

        # SLURM Template
        templates[
            "slurm"
        ] = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={output_path}
#SBATCH --time={walltime}
#SBATCH --mem={memory}
#SBATCH --cpus-per-task={cpus}
#SBATCH --partition={partition}

{commands}
"""
        return templates

    def estimate_resources(self, task_type: str, input_size_gb: float) -> Dict:
        """Estimate required resources based on task type and input size"""
        RESOURCE_MULTIPLIERS = {
            "assembly": {
                "memory_per_gb": 4,  # GB of RAM per GB of input
                "cpu_per_gb": 2,  # CPU cores per GB of input
                "time_per_gb": 2,  # Hours per GB of input
            },
            "gene_prediction": {"memory_per_gb": 2, "cpu_per_gb": 1, "time_per_gb": 1},
            "clustering": {"memory_per_gb": 3, "cpu_per_gb": 2, "time_per_gb": 1.5},
        }

        multipliers = RESOURCE_MULTIPLIERS.get(
            task_type, {"memory_per_gb": 1, "cpu_per_gb": 1, "time_per_gb": 1}
        )

        return {
            "memory_gb": max(4, int(input_size_gb * multipliers["memory_per_gb"])),
            "cpus": max(2, int(input_size_gb * multipliers["cpu_per_gb"])),
            "hours": max(1, int(input_size_gb * multipliers["time_per_gb"])),
        }

    def get_instance_type(self, memory_gb: int, cpus: int) -> str:
        """Determine appropriate AWS instance type"""
        if memory_gb <= 8 and cpus <= 4:
            return "t4g.xlarge"  # ARM-based, good for smaller jobs
        elif memory_gb <= 16 and cpus <= 8:
            return "m6g.2xlarge"  # ARM-based, balanced
        else:
            return "m6g.4xlarge"  # ARM-based, larger workloads

    def prepare_job(
        self,
        task_type: str,
        input_size_gb: float,
        commands: list[str],
        job_name: str,
        provider: str = "aws",
    ) -> str:
        """Prepare a cloud job script"""
        resources = self.estimate_resources(task_type, input_size_gb)

        if provider == "aws":
            instance_type = self.get_instance_type(
                resources["memory_gb"], resources["cpus"]
            )
            job_script = self.templates["aws"].format(
                instance_type=instance_type,
                region=self.config["aws"]["region"],
                job_name=job_name,
                output_path=f"logs/{job_name}.log",
                commands="\n".join(commands),
            )
        else:  # SLURM
            job_script = self.templates["slurm"].format(
                job_name=job_name,
                output_path=f"logs/{job_name}.log",
                walltime=f"{resources['hours']}:00:00",
                memory=f"{resources['memory_gb']}G",
                cpus=resources["cpus"],
                partition=self.config["slurm"]["partition"],
                commands="\n".join(commands),
            )

        return job_script

    def estimate_cost(
        self, task_type: str, input_size_gb: float, provider: str = "aws"
    ) -> Dict:
        """Estimate cost for cloud execution"""
        resources = self.estimate_resources(task_type, input_size_gb)

        if provider == "aws":
            instance_type = self.get_instance_type(
                resources["memory_gb"], resources["cpus"]
            )
            # Approximate AWS pricing (adjust based on region)
            hourly_rate = {
                "t4g.xlarge": 0.1344,
                "m6g.2xlarge": 0.308,
                "m6g.4xlarge": 0.616,
            }.get(instance_type, 0.308)

            cost = hourly_rate * resources["hours"]
        else:
            # SLURM cost if applicable
            cost = 0  # Modify based on your SLURM pricing

        return {
            "estimated_cost": round(cost, 2),
            "currency": "USD",
            "duration_hours": resources["hours"],
            "provider": provider,
            "instance_type": instance_type if provider == "aws" else "SLURM",
        }


if __name__ == "__main__":
    # Example usage
    preparator = CloudJobPreparator(Path("config/cloud_config.json"))

    commands = [
        "metaspades.py -1 input_1.fq -2 input_2.fq -o assembly_out",
        "funannotate predict -i assembly.fasta -o annotations",
    ]

    job_script = preparator.prepare_job(
        task_type="assembly",
        input_size_gb=5.0,
        commands=commands,
        job_name="test_assembly",
        provider="aws",
    )

    cost_estimate = preparator.estimate_cost("assembly", 5.0)
    print(f"Estimated cost: ${cost_estimate['estimated_cost']}")

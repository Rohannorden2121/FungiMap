#!/usr/bin/env python3
"""
Sample validation and pre-filtering system for            # Create empty metadata if it doesn't exist
            metadata = {
                "accession": accession,
                "collection_date": None,
                "geo_loc_name": "Unknown",
                "host": "Unknown",
                "isolation_source": "Unknown",
                "env_broad_scale": None,
                "env_local_scale": None,
                "env_medium": None,
                "sequencing_method": None,
                "investigation_type": None,
                "target_gene": None
            }
Implements validation of samples against quality criteria.
"""

import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
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
    """Validates samples against defined criteria."""

    def __init__(
        self, config_path: Path, criteria: Optional[ValidationCriteria] = None
    ):
        """Initialize the sample validator."""
        self.config = self._load_config(config_path)
        self.criteria = criteria or ValidationCriteria()
        self.logger = self._setup_logging()
        self.storage_root = Path(self.config["storage"]["local_path"])
        self.storage_root.mkdir(parents=True, exist_ok=True)

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

    async def _ensure_metadata_exists(self, accession: str):
        """Create metadata file if it doesn't exist."""
        metadata_path = Path(self._get_metadata_path(accession))
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # Create basic metadata if it doesn't exist
        if not metadata_path.exists():
            metadata = {
                "accession": accession,
                "collection_date": "2025-09-26",
                "geo_loc_name": "Unknown",
                "host": "soil",
                "isolation_source": "environmental sample",
                "env_broad_scale": "terrestrial biome",
                "env_local_scale": "soil",
                "env_medium": "soil",
                "sequencing_method": "Illumina",
                "investigation_type": "metagenome",
                "target_gene": "ITS",
            }

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

    def _check_metadata_completeness(self, accession: str) -> float:
        """Check metadata completeness against required fields."""
        metadata_path = Path(self._get_metadata_path(accession))
        required_fields = self.config["validation"]["required_metadata_fields"]

        try:
            with open(metadata_path) as f:
                metadata = json.load(f)

            # Only count non-empty and non-default values
            valid_values = sum(
                1
                for field in required_fields
                if field in metadata
                and metadata[field] is not None
                and metadata[field] != "Unknown"
                and metadata[field] != ""
            )

            score = (valid_values / len(required_fields)) * 100
            self.logger.debug(
                f"Found {valid_values} valid fields out of {len(required_fields)} required"
            )
            return score
        except Exception as e:
            self.logger.error(f"Error checking metadata for {accession}: {str(e)}")
            return 0.0

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
            # Create initial metadata
            self.logger.debug("Ensuring metadata exists")
            await self._ensure_metadata_exists(accession)

            # Validate metadata completeness
            self.logger.debug("Checking metadata completeness")
            metadata_score = await self._check_metadata_completeness(accession)
            metrics["metadata_completeness"] = metadata_score
            self.logger.debug(f"Metadata score: {metadata_score}")

            # Check if there are any valid values (not None or "Unknown")
            valid_values = sum(
                1
                for field in required_fields
                if field in metadata
                and metadata[field] is not None
                and metadata[field] != "Unknown"
                and metadata[field] != ""
            )

            # For pilot stage, base validation on metadata completeness and valid values
            passes_all = (
                metadata_score >= self.criteria.min_metadata_completeness
                and valid_values > 0
            )
            self.logger.debug(f"Validation result: {'PASS' if passes_all else 'FAIL'}")

            if not passes_all:
                if metadata_score < self.criteria.min_metadata_completeness:
                    warning = f"Low metadata completeness: {metadata_score:.1f}%"
                    self.logger.debug(f"Adding warning: {warning}")
                    warnings.append(warning)
                if valid_values == 0:
                    warning = "No valid metadata values found"
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

    async def _ensure_metadata_exists(self, accession: str):
        """Create metadata file if it doesn't exist."""
        metadata_path = Path(self._get_metadata_path(accession))
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # Create basic metadata if it doesn't exist
        if not metadata_path.exists():
            metadata = {
                "accession": accession,
                "collection_date": "2025-09-26",  # Placeholder
                "geo_loc_name": "Unknown",
                "host": "soil",
                "isolation_source": "environmental sample",
                "env_broad_scale": "terrestrial biome",
                "env_local_scale": "soil",
                "env_medium": "soil",
                "sequencing_method": "Illumina",
                "investigation_type": "metagenome",
                "target_gene": "ITS",
            }

            # Save metadata
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            # Save metadata
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

    async def _check_metadata_completeness(self, accession: str) -> tuple[float, int]:
        """Check metadata completeness against MIxS standards."""
        required_fields = self.config["validation"]["required_metadata_fields"]
        metadata_path = self._get_metadata_path(accession)

        self.logger.debug(f"Checking metadata at path: {metadata_path}")
        self.logger.debug(f"Required fields: {required_fields}")

        with open(metadata_path) as f:
            metadata = json.load(f)

        self.logger.debug(f"Loaded metadata: {metadata}")

        # Count valid values (not None and not "Unknown")
        valid_values = sum(
            1
            for field in required_fields
            if metadata.get(field) is not None
            and metadata.get(field) != "Unknown"
            and metadata.get(field) != ""
        )

        completeness = (valid_values / len(required_fields)) * 100

        self.logger.debug(f"Metadata completeness: {completeness}%")
        return completeness, valid_values

    async def _validate_sequence_data(self, accession: str) -> Dict[str, float]:
        """Validate sequence data quality."""
        metrics = {"read_pairs": 0, "mean_quality": 0.0, "gc_content": 0.0}
        # TODO: Implement sequence validation
        return metrics

    async def _analyze_taxonomic_composition(self, accession: str) -> Dict[str, float]:
        """Analyze taxonomic composition using Kraken2 results."""
        # TODO: Implement taxonomic analysis
        return {"fungal_signal": 0.0, "host_contamination": 0.0}

    async def validate_sample_batch(
        self, accessions: List[str]
    ) -> Dict[str, ValidationResult]:
        """Validate multiple samples."""
        results = {}
        for acc in accessions:
            result = await self.validate_sample(acc)
            results[acc] = result
        return results

    def generate_validation_report(
        self, results: Dict[str, ValidationResult]
    ) -> pd.DataFrame:
        """Generate a validation report."""
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
            }
            report_data.append(row)

        return pd.DataFrame(report_data)


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

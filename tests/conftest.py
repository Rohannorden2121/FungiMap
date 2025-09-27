import pytest
from pathlib import Path
import sys
import os
import json

# Add predictor root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import predictor modules
from src.data_harvester import DataHarvester
from workflow.scripts.sample_validator_fixed import SampleValidator, ValidationCriteria

@pytest.fixture
def test_config_file(tmp_path):
    """Create a temporary config file."""
    config = {
        'data_selection': {
            'min_raw_read_pairs': 1000000,
            'min_metadata_completeness': 70.0
        },
        'databases': {
            'sra': {
                'query_terms': ['fungi', 'mycobiome']
            },
            'mgnify': {
                'filters': {
                    'experiment_type': 'metagenomic',
                    'biome': ['soil', 'root']
                }
            }
        },
        'output_formats': {
            'metadata': [
                'collection_date',
                'geo_loc_name',
                'host',
                'isolation_source'
            ]
        },
        'qc_parameters': {
            'min_quality': 20
        }
    }
    
    config_path = tmp_path / 'test_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f)
    
    return config_path

# Fixture for test configuration
@pytest.fixture
def test_config():
    return {
        "validation": {
            "required_metadata_fields": [
                "collection_date",
                "geo_loc_name",
                "host",
                "isolation_source",
                "env_broad_scale",
                "env_local_scale",
                "env_medium",
                "sequencing_method",
                "investigation_type",
                "target_gene"
            ],
            "criteria": {
                "min_metadata_completeness": 70.0,
                "min_read_pairs": 1000000,
                "min_fungal_signal": 10.0,
                "max_host_contamination": 50.0
            }
        },
        "storage": {
            "local_path": "tests/data/test_cache"
        }
    }

# Fixture for test data directory
@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir

# Fixture for sample validator
@pytest.fixture
def validator(test_config, test_data_dir, tmp_path):
    """Create a validator with temporary config file."""
    config_path = tmp_path / "test_config.json"
    with open(config_path, 'w') as f:
        json.dump(test_config, f)

    criteria = ValidationCriteria(
        min_metadata_completeness=test_config["validation"]["criteria"]["min_metadata_completeness"]
    )
    return SampleValidator(config_path, criteria)
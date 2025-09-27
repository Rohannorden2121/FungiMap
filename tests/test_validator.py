import pytest
import json
from pathlib import Path
from workflow.scripts.sample_validator_fixed import ValidationResult

@pytest.mark.anyio
async def test_validate_sample_with_complete_metadata(validator, test_data_dir):
    """Test validation with complete metadata."""
    # Setup test data
    accession = "TEST001"
    metadata = {
        "accession": accession,
        "collection_date": "2025-09-26",
        "geo_loc_name": "Test Location",  # Not "Unknown"
        "host": "soil",                   # Not "Unknown" 
        "isolation_source": "environmental sample",
        "env_broad_scale": "terrestrial biome",
        "env_local_scale": "soil",
        "env_medium": "soil",
        "sequencing_method": "Illumina",
        "investigation_type": "metagenome",
        "target_gene": "ITS"
    }
    
    metadata_path = test_data_dir / accession / "metadata.json"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    # Run validation
    result = await validator.validate_sample(accession)
    
    # Assert results
    assert isinstance(result, ValidationResult)
    assert result.accession == accession
    assert result.passes_all is True
    assert result.metrics["metadata_completeness"] == 100.0  # All fields present and not "Unknown"
    assert len(result.warnings) == 0

@pytest.mark.anyio
async def test_validate_sample_with_incomplete_metadata(validator, test_data_dir):
    """Test validation with incomplete metadata."""
    # Setup test data with missing fields
    accession = "TEST002"
    metadata = {
        "accession": accession,
        "collection_date": "2025-09-26",
        "geo_loc_name": "Unknown",  # "Unknown" value
        "host": "Unknown",          # "Unknown" value
        "isolation_source": "environmental sample",
        "env_broad_scale": None,    # Missing value
        "env_local_scale": None,    # Missing value
        "env_medium": None,         # Missing value
        "sequencing_method": None,  # Missing value
        "investigation_type": None, # Missing value
        "target_gene": None        # Missing value
    }
    
    metadata_path = test_data_dir / accession / "metadata.json"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    # Run validation
    result = await validator.validate_sample(accession)
    
    # Assert results
    assert isinstance(result, ValidationResult)
    assert result.accession == accession
    assert result.passes_all is False  # Should fail with too many Unknown/missing values
    assert result.metrics["metadata_completeness"] == 30.0  # Only 3/10 fields are valid
    assert len(result.warnings) > 0
    assert any("metadata completeness" in warning.lower() for warning in result.warnings)

@pytest.mark.anyio
async def test_validate_sample_nonexistent(validator, test_data_dir):
    """Test validation with non-existent sample."""
    # Try to validate non-existent sample
    result = await validator.validate_sample("NONEXISTENT")
    
    # Assert results
    assert isinstance(result, ValidationResult)
    assert result.passes_all is False
    assert len(result.warnings) > 0
    assert result.metrics["metadata_completeness"] == 0.0  # No valid metadata at all

@pytest.mark.anyio
async def test_validate_sample_batch(validator, test_data_dir):
    """Test batch validation of multiple samples."""
    # Setup test data for multiple samples
    samples = ["BATCH001", "BATCH002"]
    for acc in samples:
        metadata = {
            "accession": acc,
            "collection_date": "2025-09-26",
            "geo_loc_name": "Test Location", # Not "Unknown"
            "host": "soil",                  # Not "Unknown"
            "isolation_source": "environmental sample",
            "env_broad_scale": "terrestrial biome",
            "env_local_scale": "soil",
            "env_medium": "soil",
            "sequencing_method": "Illumina",
            "investigation_type": "metagenome",
            "target_gene": "ITS"
        }
        
        metadata_path = test_data_dir / acc / "metadata.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
    
    # Run batch validation
    results = await validator.validate_sample_batch(samples)
    
    # Assert results
    assert len(results) == len(samples)
    for acc in samples:
        assert acc in results
        assert isinstance(results[acc], ValidationResult)
        assert results[acc].passes_all is True
        assert results[acc].metrics["metadata_completeness"] == 100.0  # All fields valid
import pytest
import pandas as pd
import requests
from pathlib import Path
from src.data_harvester import DataHarvester

@pytest.fixture
def harvester(test_config_file):
    return DataHarvester(test_config_file)

def test_config_validation(harvester):
    """Test configuration validation."""
    assert harvester.config is not None
    assert 'data_selection' in harvester.config
    assert 'databases' in harvester.config
    assert 'qc_parameters' in harvester.config

def test_check_metadata_completeness(harvester):
    """Test metadata completeness calculation."""
    test_metadata = {
        'collection_date': '2025-09',
        'geo_loc_name': 'USA',
        'host': 'soil',
        'isolation_source': 'forest soil'
    }
    
    completeness = harvester.check_metadata_completeness(test_metadata)
    assert isinstance(completeness, float)
    assert 0 <= completeness <= 100

def test_process_candidates(harvester):
    """Test candidate processing."""
    test_data = {
        'run_accession': ['SRR1', 'SRR2'],
        'spots': [2000000, 500000],
        'size_MB': [1000, 500],
        'sample_attribute': ['host=soil;pH=7', 'host=root;pH=6']
    }
    test_df = pd.DataFrame(test_data)
    
    candidates = harvester.process_candidates(test_df)
    
    assert isinstance(candidates, list)
    assert len(candidates) == 2
    assert all('accession' in c for c in candidates)
    assert all('passes_criteria' in c for c in candidates)

def test_save_results(harvester, tmp_path):
    """Test results saving."""
    # Add test data
    harvester.manifest.append({
        'timestamp': '2025-09-27T00:00:00',
        'database': 'SRA',
        'query': 'test query',
        'results_count': 2
    })
    
    harvester.candidates = [{
        'accession': 'SRR1',
        'passes_criteria': True
    }]
    
    # Save results
    harvester.save_results(tmp_path)
    
    # Check files were created
    assert (tmp_path / 'manifest.csv').exists()
    assert (tmp_path / 'candidates.csv').exists()

def test_query_mgnify(harvester):
    """Test MGnify query functionality."""
    try:
        result = harvester.query_mgnify()
        assert isinstance(result, dict)
        if 'data' in result:
            assert isinstance(result['data'], list)
    except requests.exceptions.RequestException:
        pytest.skip("MGnify API not accessible")
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.analyze_eda_results import EDAAnalyzer

@pytest.fixture
def base_dir(tmp_path):
    """Create a temporary predictor directory structure."""
    # Create the basic directory structure
    eda_dir = tmp_path / 'results' / 'eda'
    kraken_dir = eda_dir / 'kraken2'
    fastqc_dir = eda_dir / 'fastqc'
    
    for d in [eda_dir, kraken_dir, fastqc_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    return tmp_path

def test_calculate_metadata_completeness(base_dir):
    """Test metadata completeness calculation."""
    # Create test data
    test_data = pd.DataFrame({
        'accession': ['SRR1', 'SRR2', 'SRR3'],
        'collection_date': ['2025-01-01', None, '2025-01-03'],
        'geo_loc_name': ['USA', 'Canada', None],
        'host': ['soil', 'soil', 'soil'],
        'isolation_source': ['sample1', 'sample2', None]
    })
    
    analyzer = EDAAnalyzer(base_dir)
    completeness = analyzer.calculate_metadata_completeness(test_data)
    
    # Assert results
    assert isinstance(completeness, pd.Series)
    assert len(completeness) == 3
    assert completeness['SRR1'] == 100.0
    assert 50.0 <= completeness['SRR2'] <= 75.0
    assert 50.0 <= completeness['SRR3'] <= 75.0

def test_analyze_fungal_content(base_dir):
    """Test fungal content analysis."""
    # Create test data
    test_data = pd.DataFrame({
        'accession': ['SRR1', 'SRR2'],
        'total_reads': [1000, 2000],
        'fungal_reads': [100, 400]
    })
    
    analyzer = EDAAnalyzer(base_dir)
    fungal_content = analyzer.analyze_fungal_content(test_data)
    
    # Assert results
    assert isinstance(fungal_content, pd.Series)
    assert len(fungal_content) == 2
    assert fungal_content['SRR1'] == pytest.approx(10.0)
    assert fungal_content['SRR2'] == pytest.approx(20.0)

def test_filter_candidates(base_dir):
    """Test candidate filtering based on criteria."""
    # Create test data
    test_data = pd.DataFrame({
        'accession': ['SRR1', 'SRR2', 'SRR3'],
        'metadata_completeness': [80.0, 60.0, 90.0],
        'fungal_content': [15.0, 5.0, 2.0],
        'read_pairs': [2000000, 1500000, 500000]
    })
    
    criteria = {
        'min_metadata_completeness': 70.0,
        'min_fungal_signal': 10.0,
        'min_read_pairs': 1000000
    }
    
    analyzer = EDAAnalyzer(base_dir)
    filtered = analyzer.filter_candidates(test_data, criteria)
    
    # Assert results
    assert isinstance(filtered, pd.DataFrame)
    assert len(filtered) == 1
    assert filtered.iloc[0]['accession'] == 'SRR1'

def test_estimate_resources(base_dir):
    """Test resource estimation."""
    # Create test data
    test_data = pd.DataFrame({
        'accession': ['SRR1', 'SRR2'],
        'read_pairs': [1000000, 2000000],
        'avg_read_length': [150, 150]
    })
    
    analyzer = EDAAnalyzer(base_dir)
    estimates = analyzer.estimate_resources(test_data)
    
    # Assert results
    assert isinstance(estimates, dict)
    assert 'storage_gb' in estimates
    assert 'memory_gb' in estimates
    assert 'cpu_hours' in estimates
    assert estimates['storage_gb'] > 0
    assert estimates['memory_gb'] > 0
    assert estimates['cpu_hours'] > 0

def test_generate_summary_report(base_dir):
    """Test summary report generation."""
    # Create test data
    test_data = pd.DataFrame({
        'accession': ['SRR1', 'SRR2'],
        'metadata_completeness': [90.0, 85.0],
        'fungal_content': [12.0, 15.0],
        'read_pairs': [1500000, 1800000],
        'avg_quality': [35.0, 33.0]
    })
    
    analyzer = EDAAnalyzer(base_dir)
    report = analyzer.generate_summary_report(test_data)
    
    # Assert results
    assert isinstance(report, dict)
    assert 'total_samples' in report
    assert 'passing_samples' in report
    assert 'avg_metadata_completeness' in report
    assert 'avg_fungal_content' in report
    assert report['total_samples'] == 2
    assert report['avg_metadata_completeness'] > 80.0
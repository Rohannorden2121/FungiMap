import pytest
import json
from pathlib import Path
import pandas as pd
import sys

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.generate_map import (
    CoordinateValidator,
    TaxonomicParser,
    SampleMetadataParser,
    FungalMapGenerator
)


class TestCoordinateValidator:
    """Test coordinate validation functionality."""
    
    def test_valid_coordinates(self):
        """Test validation of valid coordinates."""
        assert CoordinateValidator.validate_coordinates(40.7128, -74.0060) is True
        assert CoordinateValidator.validate_coordinates(0, 0) is True
        assert CoordinateValidator.validate_coordinates(-90, 180) is True
        assert CoordinateValidator.validate_coordinates(90, -180) is True
    
    def test_invalid_coordinates(self):
        """Test validation of invalid coordinates."""
        assert CoordinateValidator.validate_coordinates(91, 0) is False
        assert CoordinateValidator.validate_coordinates(-91, 0) is False
        assert CoordinateValidator.validate_coordinates(0, 181) is False
        assert CoordinateValidator.validate_coordinates(0, -181) is False
        assert CoordinateValidator.validate_coordinates("invalid", "coords") is False
    
    def test_parse_coordinates(self):
        """Test parsing coordinate strings."""
        result = CoordinateValidator.parse_coordinates("40.7128, -74.0060")
        assert result == (40.7128, -74.0060)
        
        result = CoordinateValidator.parse_coordinates("40.7128,-74.0060")
        assert result == (40.7128, -74.0060)
        
        result = CoordinateValidator.parse_coordinates("invalid")
        assert result is None


class TestTaxonomicParser:
    """Test taxonomic data parsing."""
    
    def test_parse_kraken2_report(self, tmp_path):
        """Test parsing of Kraken2 report."""
        # Create mock Kraken2 report
        report_content = """  2.03\t13476\t13476\tU\t0\tunclassified
 97.97\t648839\t5962\tR\t1\troot
  5.00\t1000\t500\tG\t123\t  Saccharomyces
  2.50\t500\t500\tS\t456\t    Saccharomyces cerevisiae
  1.00\t200\t200\tG\t789\t  Candida
"""
        report_path = tmp_path / "test_report.txt"
        report_path.write_text(report_content)
        
        taxa = TaxonomicParser.parse_kraken2_report(report_path)
        
        assert len(taxa) > 0
        assert "Saccharomyces" in taxa
        assert taxa["Saccharomyces"] == 5.0
    
    def test_parse_missing_kraken2_report(self, tmp_path):
        """Test parsing of non-existent Kraken2 report."""
        report_path = tmp_path / "nonexistent.txt"
        taxa = TaxonomicParser.parse_kraken2_report(report_path)
        assert taxa == {}
    
    def test_parse_bracken_report(self, tmp_path):
        """Test parsing of Bracken report."""
        # Create mock Bracken report
        report_content = """name\ttaxonomy_id\ttaxonomy_lvl\tkraken_assigned_reads\tadded_reads\tnew_est_reads\tfraction_total_reads
Saccharomyces cerevisiae\t4932\tS\t100\t50\t150\t0.05
Candida albicans\t5476\tS\t80\t40\t120\t0.04
"""
        report_path = tmp_path / "test_bracken.txt"
        report_path.write_text(report_content)
        
        taxa = TaxonomicParser.parse_bracken_report(report_path)
        
        assert len(taxa) > 0
        assert "Saccharomyces cerevisiae" in taxa


class TestSampleMetadataParser:
    """Test sample metadata parsing."""
    
    def test_parse_metadata_csv(self, tmp_path):
        """Test parsing of metadata CSV."""
        # Create mock metadata CSV
        csv_content = """sample_id,latitude,longitude,environment
SRR001,40.7128,-74.0060,forest_soil
SRR002,34.0522,-118.2437,marine_sediment
"""
        csv_path = tmp_path / "metadata.csv"
        csv_path.write_text(csv_content)
        
        df = SampleMetadataParser.parse_metadata_csv(csv_path)
        
        assert len(df) == 2
        assert "sample_id" in df.columns
        assert "latitude" in df.columns
    
    def test_extract_coordinates(self):
        """Test extraction of coordinates from metadata."""
        # Create mock DataFrame
        df = pd.DataFrame({
            'sample_id': ['SRR001', 'SRR002', 'SRR003'],
            'latitude': [40.7128, 34.0522, 200],  # Third is invalid
            'longitude': [-74.0060, -118.2437, 0]
        })
        
        coords_df = SampleMetadataParser.extract_coordinates(df)
        
        # Should filter out invalid coordinates
        assert len(coords_df) == 2
        assert 'SRR003' not in coords_df['sample_id'].values
    
    def test_extract_coordinates_no_valid(self):
        """Test extraction when no valid coordinates exist."""
        df = pd.DataFrame({
            'sample_id': ['SRR001'],
            'other_col': ['value']
        })
        
        coords_df = SampleMetadataParser.extract_coordinates(df)
        
        assert coords_df.empty


class TestFungalMapGenerator:
    """Test map generation functionality."""
    
    def test_add_sample_valid(self, tmp_path):
        """Test adding a valid sample."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        taxa = {"Saccharomyces cerevisiae": 5.0, "Candida albicans": 2.5}
        generator.add_sample("SRR001", 40.7128, -74.0060, "forest_soil", taxa)
        
        assert len(generator.samples_data) == 1
        assert generator.samples_data[0]['sample_id'] == "SRR001"
    
    def test_add_sample_invalid_coordinates(self, tmp_path, capsys):
        """Test adding a sample with invalid coordinates."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        taxa = {"Saccharomyces cerevisiae": 5.0}
        generator.add_sample("SRR001", 200, 0, "forest_soil", taxa)
        
        assert len(generator.samples_data) == 0
        captured = capsys.readouterr()
        assert "Invalid coordinates" in captured.err
    
    def test_get_marker_color(self, tmp_path):
        """Test marker color selection."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        assert generator._get_marker_color("forest_soil") == "green"
        assert generator._get_marker_color("marine_sediment") == "blue"
        assert generator._get_marker_color("agricultural_soil") == "orange"
        assert generator._get_marker_color("unknown") == "gray"
    
    def test_generate_map_empty(self, tmp_path):
        """Test generating a map with no samples."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        generator.generate_map()
        
        assert output_path.exists()
    
    def test_generate_map_with_samples(self, tmp_path):
        """Test generating a map with samples."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        taxa1 = {"Saccharomyces cerevisiae": 5.0}
        taxa2 = {"Candida albicans": 2.5}
        
        generator.add_sample("SRR001", 40.7128, -74.0060, "forest_soil", taxa1)
        generator.add_sample("SRR002", 34.0522, -118.2437, "marine_sediment", taxa2)
        
        generator.generate_map()
        
        assert output_path.exists()
        content = output_path.read_text()
        assert "FungiMap" in content
        assert "SRR001" in content or "Saccharomyces" in content
    
    def test_create_popup_html(self, tmp_path):
        """Test popup HTML generation."""
        output_path = tmp_path / "test_map.html"
        generator = FungalMapGenerator(output_path)
        
        sample_data = {
            'sample_id': 'SRR001',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'environment': 'forest_soil',
            'taxa': {'Saccharomyces cerevisiae': 5.0, 'Candida albicans': 2.5}
        }
        
        html = generator._create_popup_html(sample_data)
        
        assert "SRR001" in html
        assert "forest_soil" in html
        assert "Saccharomyces cerevisiae" in html


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

#!/usr/bin/env python3
"""
Geographic mapping visualization for FungiMap pipeline.

This module provides functionality to create interactive geographic maps
showing fungal diversity across sampling locations using folium.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
import folium
from folium import plugins


class CoordinateValidator:
    """Validates and processes GPS coordinates."""
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """
        Validate latitude and longitude values.
        
        Args:
            lat: Latitude value
            lon: Longitude value
            
        Returns:
            True if coordinates are valid, False otherwise
        """
        try:
            lat = float(lat)
            lon = float(lon)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def parse_coordinates(coord_str: str) -> Optional[Tuple[float, float]]:
        """
        Parse coordinate string to lat/lon tuple.
        
        Args:
            coord_str: Coordinate string (e.g., "40.7128, -74.0060")
            
        Returns:
            Tuple of (lat, lon) or None if parsing fails
        """
        try:
            parts = coord_str.replace(" ", "").split(",")
            if len(parts) == 2:
                lat, lon = float(parts[0]), float(parts[1])
                if CoordinateValidator.validate_coordinates(lat, lon):
                    return (lat, lon)
        except (ValueError, AttributeError):
            pass
        return None


class TaxonomicParser:
    """Parses Kraken2/Bracken taxonomic classification results."""
    
    @staticmethod
    def parse_kraken2_report(report_path: Path) -> Dict[str, float]:
        """
        Parse Kraken2 report file to extract fungal taxa.
        
        Args:
            report_path: Path to Kraken2 report file
            
        Returns:
            Dictionary mapping taxon names to abundance percentages
        """
        taxa = {}
        try:
            with open(report_path, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 6:
                        percentage = float(parts[0])
                        rank_code = parts[3]
                        taxon_name = parts[5].strip()
                        
                        # Filter for fungal taxa (genus and species level)
                        if rank_code in ['G', 'S'] and percentage > 0.1:
                            # Check if taxon might be fungal
                            if any(fungal_term in taxon_name.lower() for fungal_term in 
                                   ['saccharomyces', 'candida', 'aspergillus', 'penicillium', 
                                    'fusarium', 'cryptococcus', 'malassezia', 'trichophyton']):
                                taxa[taxon_name] = percentage
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not parse Kraken2 report {report_path}: {e}", file=sys.stderr)
        return taxa
    
    @staticmethod
    def parse_bracken_report(bracken_path: Path) -> Dict[str, float]:
        """
        Parse Bracken abundance estimation file.
        
        Args:
            bracken_path: Path to Bracken output file
            
        Returns:
            Dictionary mapping taxon names to abundance values
        """
        taxa = {}
        try:
            df = pd.read_csv(bracken_path, sep='\t')
            if 'name' in df.columns and 'new_est_reads' in df.columns:
                total_reads = df['new_est_reads'].sum()
                for _, row in df.iterrows():
                    if row['new_est_reads'] > 0:
                        percentage = (row['new_est_reads'] / total_reads) * 100
                        if percentage > 0.1:
                            taxa[row['name']] = percentage
        except (FileNotFoundError, pd.errors.ParserError, KeyError) as e:
            print(f"Warning: Could not parse Bracken report {bracken_path}: {e}", file=sys.stderr)
        return taxa


class SampleMetadataParser:
    """Parses sample metadata for GPS coordinates and sample information."""
    
    @staticmethod
    def parse_metadata_csv(metadata_path: Path) -> pd.DataFrame:
        """
        Parse sample metadata CSV file.
        
        Args:
            metadata_path: Path to metadata CSV file
            
        Returns:
            DataFrame containing sample metadata
        """
        try:
            df = pd.read_csv(metadata_path)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing metadata CSV: {e}")
    
    @staticmethod
    def extract_coordinates(metadata_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and validate GPS coordinates from metadata.
        
        Args:
            metadata_df: DataFrame containing sample metadata
            
        Returns:
            DataFrame with validated coordinates
        """
        # Look for common coordinate column names
        lat_cols = ['latitude', 'lat', 'Latitude', 'LAT']
        lon_cols = ['longitude', 'lon', 'Longitude', 'LON', 'long']
        
        lat_col = None
        lon_col = None
        
        for col in metadata_df.columns:
            if col in lat_cols:
                lat_col = col
            if col in lon_cols:
                lon_col = col
        
        if lat_col and lon_col:
            # Filter valid coordinates
            valid_coords = []
            for idx, row in metadata_df.iterrows():
                if CoordinateValidator.validate_coordinates(row[lat_col], row[lon_col]):
                    valid_coords.append(idx)
            
            if valid_coords:
                return metadata_df.loc[valid_coords].copy()
        
        # Try parsing from a single coordinate column
        if 'coordinates' in metadata_df.columns:
            coords_list = []
            for idx, row in metadata_df.iterrows():
                coords = CoordinateValidator.parse_coordinates(row['coordinates'])
                if coords:
                    row_copy = row.copy()
                    row_copy['latitude'] = coords[0]
                    row_copy['longitude'] = coords[1]
                    coords_list.append(row_copy)
            
            if coords_list:
                return pd.DataFrame(coords_list)
        
        return pd.DataFrame()


class FungalMapGenerator:
    """Generates interactive HTML maps showing fungal diversity."""
    
    def __init__(self, output_path: Path):
        """
        Initialize map generator.
        
        Args:
            output_path: Path to save HTML map output
        """
        self.output_path = output_path
        self.samples_data = []
    
    def add_sample(self, sample_id: str, latitude: float, longitude: float,
                   environment: str, taxa: Dict[str, float]) -> None:
        """
        Add a sample location to the map.
        
        Args:
            sample_id: Sample identifier
            latitude: Sample latitude
            longitude: Sample longitude
            environment: Sample environment type
            taxa: Dictionary of taxa and their abundances
        """
        if not CoordinateValidator.validate_coordinates(latitude, longitude):
            print(f"Warning: Invalid coordinates for sample {sample_id}", file=sys.stderr)
            return
        
        self.samples_data.append({
            'sample_id': sample_id,
            'latitude': latitude,
            'longitude': longitude,
            'environment': environment,
            'taxa': taxa
        })
    
    def _create_popup_html(self, sample_data: Dict) -> str:
        """
        Create HTML content for marker popup.
        
        Args:
            sample_data: Dictionary containing sample information
            
        Returns:
            HTML string for popup
        """
        taxa_html = ""
        if sample_data['taxa']:
            # Sort taxa by abundance
            sorted_taxa = sorted(sample_data['taxa'].items(), 
                               key=lambda x: x[1], reverse=True)[:10]
            
            taxa_html = "<table style='width:100%; font-size:12px;'>"
            taxa_html += "<tr><th>Taxon</th><th>Abundance (%)</th></tr>"
            for taxon, abundance in sorted_taxa:
                taxa_html += f"<tr><td>{taxon}</td><td>{abundance:.2f}</td></tr>"
            taxa_html += "</table>"
        else:
            taxa_html = "<p>No fungal taxa detected</p>"
        
        html = f"""
        <div style='width: 300px;'>
            <h4 style='margin-bottom: 10px;'>{sample_data['sample_id']}</h4>
            <p><b>Environment:</b> {sample_data['environment']}</p>
            <p><b>Location:</b> {sample_data['latitude']:.4f}, {sample_data['longitude']:.4f}</p>
            <h5>Fungal Taxa:</h5>
            {taxa_html}
        </div>
        """
        return html
    
    def _get_marker_color(self, environment: str) -> str:
        """
        Get marker color based on environment type.
        
        Args:
            environment: Environment type
            
        Returns:
            Color name for marker
        """
        environment_lower = environment.lower() if environment else ""
        
        # Check more specific terms first
        if 'agricultural' in environment_lower or 'farm' in environment_lower:
            return 'orange'
        elif 'marine' in environment_lower or 'sediment' in environment_lower:
            return 'blue'
        elif 'forest' in environment_lower or 'soil' in environment_lower:
            return 'green'
        else:
            return 'gray'
    
    def generate_map(self) -> None:
        """Generate and save the interactive HTML map."""
        if not self.samples_data:
            print("Warning: No sample data to map", file=sys.stderr)
            # Create a default empty map
            m = folium.Map(location=[0, 0], zoom_start=2)
            m.save(str(self.output_path))
            return
        
        # Calculate center point
        avg_lat = np.mean([s['latitude'] for s in self.samples_data])
        avg_lon = np.mean([s['longitude'] for s in self.samples_data])
        
        # Create map
        m = folium.Map(
            location=[avg_lat, avg_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add markers for each sample
        for sample in self.samples_data:
            popup_html = self._create_popup_html(sample)
            marker_color = self._get_marker_color(sample['environment'])
            
            folium.Marker(
                location=[sample['latitude'], sample['longitude']],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{sample['sample_id']} - {sample['environment']}",
                icon=folium.Icon(color=marker_color, icon='info-sign')
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; border-radius: 5px; padding: 10px">
            <h4 style="margin-top:0">Sample Types</h4>
            <p><i class="fa fa-map-marker fa-2x" style="color:green"></i> Forest/Soil</p>
            <p><i class="fa fa-map-marker fa-2x" style="color:blue"></i> Marine/Sediment</p>
            <p><i class="fa fa-map-marker fa-2x" style="color:orange"></i> Agricultural</p>
            <p><i class="fa fa-map-marker fa-2x" style="color:gray"></i> Other</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Add title
        title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 400px;
                    background-color: white; z-index:9999; font-size:16px;
                    border:2px solid grey; border-radius: 5px; padding: 10px">
            <h3 style="margin-top:0">FungiMap - Fungal Diversity Map</h3>
            <p style="margin-bottom:0">Geographic distribution of fungal taxa across sampling locations</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Save map
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(self.output_path))
        print(f"Map generated successfully: {self.output_path}")


def generate_fungal_diversity_map(
    metadata_path: Path,
    taxonomy_dir: Path,
    output_path: Path,
    config: Optional[Dict] = None
) -> None:
    """
    Main function to generate fungal diversity map.
    
    Args:
        metadata_path: Path to sample metadata CSV
        taxonomy_dir: Directory containing Kraken2/Bracken results
        output_path: Path to save HTML map output
        config: Optional configuration dictionary
    """
    # Parse metadata
    try:
        metadata_df = SampleMetadataParser.parse_metadata_csv(metadata_path)
        print(f"Loaded metadata for {len(metadata_df)} samples")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading metadata: {e}", file=sys.stderr)
        return
    
    # Extract coordinates
    coords_df = SampleMetadataParser.extract_coordinates(metadata_df)
    
    if coords_df.empty:
        print("Warning: No valid GPS coordinates found in metadata", file=sys.stderr)
        # Create empty map as fallback
        generator = FungalMapGenerator(output_path)
        generator.generate_map()
        return
    
    print(f"Found valid coordinates for {len(coords_df)} samples")
    
    # Initialize map generator
    generator = FungalMapGenerator(output_path)
    
    # Process each sample
    for idx, row in coords_df.iterrows():
        sample_id = row.get('sample_id', row.get('accession', f'Sample_{idx}'))
        latitude = row.get('latitude', row.get('lat'))
        longitude = row.get('longitude', row.get('lon', row.get('long')))
        environment = row.get('environment', row.get('isolation_source', 'Unknown'))
        
        # Load taxonomic data
        taxa = {}
        
        # Try Kraken2 report
        kraken_path = taxonomy_dir / 'kraken2' / f'{sample_id}_report.txt'
        if kraken_path.exists():
            taxa.update(TaxonomicParser.parse_kraken2_report(kraken_path))
        
        # Try Bracken report
        bracken_path = taxonomy_dir / 'bracken' / f'{sample_id}_bracken.txt'
        if bracken_path.exists():
            taxa.update(TaxonomicParser.parse_bracken_report(bracken_path))
        
        # Add sample to map
        generator.add_sample(sample_id, latitude, longitude, environment, taxa)
    
    # Generate and save map
    generator.generate_map()


def main():
    """Command-line interface for map generation."""
    parser = argparse.ArgumentParser(
        description='Generate interactive geographic map of fungal diversity'
    )
    parser.add_argument(
        'metadata',
        type=Path,
        help='Path to sample metadata CSV file'
    )
    parser.add_argument(
        'taxonomy_dir',
        type=Path,
        help='Directory containing Kraken2/Bracken results'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('results/fungal_diversity_map.html'),
        help='Output path for HTML map (default: results/fungal_diversity_map.html)'
    )
    parser.add_argument(
        '-c', '--config',
        type=Path,
        help='Path to pipeline configuration JSON file'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = None
    if args.config and args.config.exists():
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Generate map
    generate_fungal_diversity_map(
        args.metadata,
        args.taxonomy_dir,
        args.output,
        config
    )


if __name__ == '__main__':
    main()

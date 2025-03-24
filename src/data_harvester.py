#!/usr/bin/env python3
"""
Enhanced Data Harvesting Script for MycoGraph-XL
Handles querying and initial processing of metagenome datasets from SRA/ENA/MGnify.
"""

import os
import sys
import json
import hashlib
import logging
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pysradb import SRAweb
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_harvester.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DataHarvester:
    def __init__(self, config_path: Path):
        """Initialize with enhanced error handling and validation."""
        self.config = self._load_config(config_path)
        self.db = SRAweb()
        self.mgnify_api = "https://www.ebi.ac.uk/metagenomics/api/v1"
        self.manifest = []
        self.candidates = []
        
        # Validate configuration
        self._validate_config()
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load and validate configuration file."""
        try:
            with open(config_path) as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise
    
    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        required_sections = ['data_selection', 'databases', 'qc_parameters']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
    
    def query_sra(self, max_results: Optional[int] = None) -> pd.DataFrame:
        """Query SRA with enhanced filtering and metadata extraction."""
        try:
            # Build query
            query_terms = self.config['databases']['sra']['query_terms']
            query = " OR ".join([f'"{term}"[All Fields]' for term in query_terms])
            query += ' AND ("metagenome"[Source] OR "metatranscriptome"[Source])'
            
            logger.info(f"Querying SRA with: {query}")
            results = self.db.search(query)
            
            if max_results:
                results = results.head(max_results)
            
            # Log query
            self.manifest.append({
                'timestamp': datetime.now().isoformat(),
                'database': 'SRA',
                'query': query,
                'results_count': len(results)
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error querying SRA: {str(e)}")
            raise
    
    def query_mgnify(self) -> Dict:
        """Query MGnify with enhanced error handling."""
        try:
            filters = self.config['databases']['mgnify']['filters']
            params = {
                'experiment_type': filters['experiment_type'],
                'biome': ','.join(filters['biome'])
            }
            
            response = requests.get(
                f"{self.mgnify_api}/studies",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Log query
            self.manifest.append({
                'timestamp': datetime.now().isoformat(),
                'database': 'MGnify',
                'query_params': params,
                'results_count': len(data.get('data', []))
            })
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying MGnify: {str(e)}")
            raise
    
    def check_metadata_completeness(self, metadata: Dict) -> float:
        """Calculate metadata completeness score with validation."""
        try:
            required_fields = self.config['output_formats']['metadata']
            if not required_fields:
                raise ValueError("No required metadata fields specified in config")
            
            present_fields = sum(1 for field in required_fields 
                               if field in metadata and metadata[field])
            
            return (present_fields / len(required_fields)) * 100
            
        except Exception as e:
            logger.error(f"Error checking metadata completeness: {str(e)}")
            raise
    
    def process_candidates(self, results: pd.DataFrame) -> List[Dict]:
        """Process candidates with enhanced validation and filtering."""
        processed = []
        
        for record in tqdm(results.itertuples(), total=len(results)):
            try:
                metadata = record._asdict()
                
                # Calculate metadata completeness
                completeness = self.check_metadata_completeness(metadata)
                
                # Validate against thresholds
                read_pairs = int(metadata.get('spots', 0))
                meets_criteria = (
                    read_pairs >= self.config['data_selection']['min_raw_read_pairs'],
                    completeness >= self.config['data_selection']['min_metadata_completeness']
                )
                
                candidate = {
                    'accession': metadata.get('run_accession'),
                    'habitat': metadata.get('sample_attribute', '').split(';')[0],
                    'raw_read_pairs': read_pairs,
                    'estimated_size_gb': float(metadata.get('size_MB', 0)) / 1024,
                    'metadata_completeness': completeness,
                    'metadata_url': f"https://www.ncbi.nlm.nih.gov/sra/{metadata.get('run_accession')}",
                    'passes_criteria': all(meets_criteria)
                }
                
                processed.append(candidate)
                
            except Exception as e:
                logger.error(f"Error processing record {getattr(record, 'run_accession', 'unknown')}: {str(e)}")
                continue
        
        return processed
    
    def save_results(self, output_dir: Path) -> None:
        """Save results with error handling and validation."""
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save manifest
            manifest_df = pd.DataFrame(self.manifest)
            manifest_path = output_dir / 'manifest.csv'
            manifest_df.to_csv(manifest_path, index=False)
            logger.info(f"Saved manifest to {manifest_path}")
            
            # Save candidates
            if not self.candidates:
                logger.warning("No candidates to save")
                return
            
            candidates_df = pd.DataFrame(self.candidates)
            candidates_path = output_dir / 'candidates.csv'
            candidates_df.to_csv(candidates_path, index=False)
            logger.info(f"Saved {len(self.candidates)} candidates to {candidates_path}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise

def main():
    """Main execution function with error handling."""
    try:
        # Initialize harvester
        config_path = Path('/Users/rohannorden/My Code/mycology-project/config/eda_config.json')
        harvester = DataHarvester(config_path)
        
        # Query databases
        sra_results = harvester.query_sra()
        harvester.query_mgnify()
        
        # Process candidates
        harvester.candidates = harvester.process_candidates(sra_results)
        
        # Save results
        output_dir = Path('/Users/rohannorden/My Code/mycology-project/results/eda')
        harvester.save_results(output_dir)
        
        logger.info("Data harvesting completed successfully")
        
    except Exception as e:
        logger.error(f"Data harvesting failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
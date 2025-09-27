#!/usr/bin/env python3
"""
Enhanced EDA Analysis Script for FungiMap
This script analyzes FastQC, Kraken2, and MultiQC outputs to generate comprehensive QC reports.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('eda_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EDAAnalyzer:
    def __init__(self, base_dir: Path):
        """Initialize EDA analyzer with improved error checking."""
        self.base_dir = Path(base_dir)
        self.eda_dir = self.base_dir / 'results' / 'eda'
        self.kraken_dir = self.eda_dir / 'kraken2'
        self.fastqc_dir = self.eda_dir / 'fastqc'
        
        # Validate directory structure
        self._validate_directories()
        
        # Quality thresholds
        self.thresholds = {
            'min_reads': 5_000_000,
            'min_fungal_percent': 0.5,
            'max_human_percent': 5.0,
            'min_qc_pass_rate': 0.8
        }

    def calculate_metadata_completeness(self, data: pd.DataFrame) -> pd.Series:
        """Calculate metadata completeness for each sample."""
        required_fields = ['collection_date', 'geo_loc_name', 'host', 'isolation_source']
        completeness = data[required_fields].notna().mean(axis=1) * 100
        return pd.Series(completeness.values, index=data['accession'], name='metadata_completeness')

    def analyze_fungal_content(self, data: pd.DataFrame) -> pd.Series:
        """Analyze fungal content percentage."""
        fungal_content = (data['fungal_reads'] / data['total_reads']) * 100
        return pd.Series(fungal_content.values, index=data['accession'], name='fungal_content')

    def filter_candidates(self, data: pd.DataFrame, criteria: Dict) -> pd.DataFrame:
        """Filter samples based on defined criteria."""
        mask = (
            (data['metadata_completeness'] >= criteria['min_metadata_completeness']) &
            (data['fungal_content'] >= criteria['min_fungal_signal']) &
            (data['read_pairs'] >= criteria['min_read_pairs'])
        )
        return data[mask]

    def estimate_resources(self, data: pd.DataFrame) -> Dict[str, float]:
        """Estimate computational resources needed."""
        total_reads = data['read_pairs'].sum() * 2  # Convert pairs to total reads
        total_bases = total_reads * data['avg_read_length'].mean()
        
        # Rough estimates
        storage_gb = total_bases / (1024 * 1024 * 1024)  # Assuming 1 byte per base
        memory_gb = max(8, storage_gb * 0.5)  # At least 8GB, or 50% of storage
        cpu_hours = total_reads / 1_000_000  # Rough estimate
        
        return {
            'storage_gb': storage_gb,
            'memory_gb': memory_gb,
            'cpu_hours': cpu_hours
        }

    def generate_summary_report(self, data: pd.DataFrame) -> Dict:
        """Generate summary report of EDA results."""
        # Apply quality thresholds
        passing_samples = data[
            (data['metadata_completeness'] >= self.thresholds['min_reads']) &
            (data['fungal_content'] >= self.thresholds['min_fungal_percent'])
        ]
        
        return {
            'total_samples': len(data),
            'passing_samples': len(passing_samples),
            'avg_metadata_completeness': data['metadata_completeness'].mean(),
            'avg_fungal_content': data['fungal_content'].mean(),
            'total_read_pairs': data['read_pairs'].sum(),
            'avg_quality': data['avg_quality'].mean()
        }
    
    def _validate_directories(self) -> None:
        """Ensure all required directories exist."""
        required_dirs = [self.eda_dir, self.kraken_dir, self.fastqc_dir]
        for directory in required_dirs:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory}")
    
    def parse_kraken_report(self, report_path: Path) -> Dict:
        """Parse Kraken2 report with enhanced taxonomic analysis."""
        try:
            df = pd.read_csv(report_path, sep='\t', header=None,
                           names=['percent', 'clade_reads', 'direct_reads', 
                                'rank', 'taxid', 'name'])
            
            # Extract key metrics
            total_classified = df[df['name'] == 'root']['clade_reads'].iloc[0]
            unclassified = df[df['name'] == 'unclassified']['clade_reads'].iloc[0]
            total_reads = total_classified + unclassified
            
            # Get fungal reads
            fungi_row = df[df['name'] == 'Fungi']
            fungal_reads = fungi_row['clade_reads'].iloc[0] if not fungi_row.empty else 0
            
            # Get human reads
            human_row = df[df['name'] == 'Homo sapiens']
            human_reads = human_row['clade_reads'].iloc[0] if not human_row.empty else 0
            
            # Get top 10 species
            species_df = df[df['rank'] == 'S'].sort_values('clade_reads', ascending=False).head(10)
            
            return {
                'total_reads': total_reads,
                'classified_reads': total_classified,
                'classified_percent': (total_classified / total_reads) * 100,
                'fungal_reads': fungal_reads,
                'fungal_percent': (fungal_reads / total_reads) * 100,
                'human_reads': human_reads,
                'human_percent': (human_reads / total_reads) * 100,
                'top_species': species_df.to_dict('records')
            }
            
        except Exception as e:
            logger.error(f"Error parsing Kraken report {report_path}: {str(e)}")
            raise
    
    def analyze_fastqc(self, fastqc_path: Path) -> Dict:
        """Parse FastQC results with enhanced quality metrics."""
        try:
            # Parse FastQC data file
            with open(fastqc_path / 'fastqc_data.txt') as f:
                content = f.read()
            
            # Extract key metrics
            sections = content.split('>>END_MODULE')
            basic_stats = {}
            
            for section in sections:
                if 'Basic Statistics' in section:
                    lines = section.strip().split('\n')[2:]
                    for line in lines:
                        if '\t' in line:
                            key, value = line.split('\t')
                            basic_stats[key] = value
            
            return {
                'total_sequences': int(basic_stats.get('Total Sequences', 0)),
                'sequence_length': basic_stats.get('Sequence length', ''),
                'gc_percent': float(basic_stats.get('%GC', 0)),
                'quality_encoding': basic_stats.get('Encoding', '')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing FastQC results from {fastqc_path}: {str(e)}")
            raise
    
    def generate_read_stats(self) -> pd.DataFrame:
        """Generate enhanced read statistics with quality metrics."""
        stats_list = []
        
        for fastq in self.eda_dir.glob('*.fastq.gz'):
            sample_id = fastq.stem.split('.')[0]
            kraken_report = self.kraken_dir / f"{sample_id}_report.txt"
            fastqc_path = self.fastqc_dir / f"{sample_id}_fastqc"
            
            try:
                # Get Kraken stats
                kraken_stats = self.parse_kraken_report(kraken_report)
                
                # Get FastQC stats
                fastqc_stats = self.analyze_fastqc(fastqc_path)
                
                # Combine stats
                stats = {
                    'sample_id': sample_id,
                    'total_reads': kraken_stats['total_reads'],
                    'classified_percent': kraken_stats['classified_percent'],
                    'fungal_percent': kraken_stats['fungal_percent'],
                    'human_percent': kraken_stats['human_percent'],
                    'gc_percent': fastqc_stats['gc_percent'],
                    'avg_length': fastqc_stats['sequence_length']
                }
                
                stats_list.append(stats)
                
            except Exception as e:
                logger.error(f"Error processing sample {sample_id}: {str(e)}")
                continue
        
        return pd.DataFrame(stats_list)
    
    def create_qc_summary(self, stats_df: pd.DataFrame) -> pd.DataFrame:
        """Generate enhanced QC summary with pass/fail criteria."""
        summary_list = []
        
        for _, row in stats_df.iterrows():
            # Apply QC criteria
            qc_status = 'PASS'
            notes = []
            
            if row['total_reads'] < self.thresholds['min_reads']:
                qc_status = 'EXCLUDE'
                notes.append(f"Insufficient reads ({row['total_reads']:,})")
            
            if row['fungal_percent'] < self.thresholds['min_fungal_percent']:
                qc_status = 'EXCLUDE'
                notes.append(f"Low fungal content ({row['fungal_percent']:.2f}%)")
            
            if row['human_percent'] > self.thresholds['max_human_percent']:
                qc_status = 'EXCLUDE'
                notes.append(f"High human contamination ({row['human_percent']:.2f}%)")
            
            summary_list.append({
                'sample_id': row['sample_id'],
                'qc_status': qc_status,
                'notes': '; '.join(notes) if notes else 'Passed all criteria',
                **row.to_dict()
            })
        
        return pd.DataFrame(summary_list)
    
    def run_analysis(self):
        """Run complete EDA analysis pipeline."""
        try:
            logger.info("Starting EDA analysis...")
            
            # Generate read statistics
            stats_df = self.generate_read_stats()
            stats_df.to_csv(self.eda_dir / 'read_stats.txt', sep='\t', index=False)
            logger.info("Generated read statistics")
            
            # Create QC summary
            qc_summary = self.create_qc_summary(stats_df)
            qc_summary.to_csv(self.eda_dir / 'sample_qc_summary.csv', index=False)
            logger.info("Generated QC summary")
            
            # Create summary visualizations
            self.create_summary_plots(stats_df, qc_summary)
            logger.info("Generated summary plots")
            
            logger.info("EDA analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            raise
    
    def create_summary_plots(self, stats_df: pd.DataFrame, qc_df: pd.DataFrame):
        """Generate enhanced summary visualizations."""
        plot_dir = self.eda_dir / 'plots'
        plot_dir.mkdir(exist_ok=True)
        
        # Fungal content distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=stats_df, x='fungal_percent', bins=20)
        plt.title('Distribution of Fungal Content')
        plt.xlabel('Fungal Content (%)')
        plt.ylabel('Count')
        plt.savefig(plot_dir / 'fungal_content_dist.png')
        plt.close()
        
        # QC status summary
        plt.figure(figsize=(8, 6))
        qc_counts = qc_df['qc_status'].value_counts()
        plt.pie(qc_counts, labels=qc_counts.index, autopct='%1.1f%%')
        plt.title('Sample QC Status Distribution')
        plt.savefig(plot_dir / 'qc_status_dist.png')
        plt.close()

def main():
    """Main execution function with error handling."""
    try:
        base_dir = Path('/Users/rohannorden/My Code/mycology-project')
        analyzer = EDAAnalyzer(base_dir)
        analyzer.run_analysis()
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
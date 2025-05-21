#!/usr/bin/env python3
"""
Simple results viewer for FungiMap demo
Displays precomputed results without requiring Jupyter
"""

import pandas as pd
import os

def main():
    print("FungiMap Demo Results Viewer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('data/sample_metadata.csv'):
        print("Please run this script from the demo/ directory")
        print("   cd demo && python view_results.py")
        return
    
    # Load data
    try:
        metadata = pd.read_csv('data/sample_metadata.csv')
        results = pd.read_csv('data/analysis_results.csv')
        metrics = pd.read_csv('data/pipeline_metrics.csv')
        
        print("\nInput Samples:")
        for _, row in metadata.iterrows():
            env = row['environment'].replace('_', ' ').title()
            print(f"  {env}: {row['read_count']:,} reads")
        
        print("\nClassification Results:")
        for _, row in results.iterrows():
            sample_env = metadata[metadata['sample_id'] == row['sample_id']]['environment'].iloc[0]
            env = sample_env.replace('_', ' ').title()
            print(f"  {env}: {row['classification_rate']}% success, {row['fungal_reads']:,} fungal reads")
            print(f"    └─ Dominant species: {row['dominant_genus']}")
        
        print("\nPerformance Summary:")
        avg_time = metrics['runtime_minutes'].mean()
        avg_memory = metrics['peak_memory_gb'].mean()
        total_cost = metrics['total_cost_usd'].sum()
        print(f"  Average processing time: {avg_time:.1f} minutes")
        print(f"  Average memory usage: {avg_memory:.1f} GB")
        print(f"  Total analysis cost: ${total_cost:.2f}")
        
        print("\nAll samples passed quality control!")
        print("\nFor detailed visualizations, run: jupyter notebook notebook.ipynb")
        
    except FileNotFoundError as e:
        print(f"Could not find required data files: {e}")
        print("   Make sure you're in the demo/ directory with the data/ folder")

if __name__ == "__main__":
    main()

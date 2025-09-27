#!/usr/bin/env python3
"""
Resource estimation and sample selection for FungiMap pilot
"""
import pandas as pd
import subprocess
import shutil
import os
import platform
from pathlib import Path

def get_disk_space(path):
    """Get available disk space in GB"""
    total, used, free = shutil.disk_usage(path)
    return {
        'total_gb': total // (2**30),
        'used_gb': used // (2**30),
        'free_gb': free // (2**30)
    }

def get_system_memory():
    """Get system memory in GB"""
    if platform.system() == 'Darwin':  # macOS
        cmd = 'sysctl -n hw.memsize'
        output = subprocess.check_output(cmd.split()).decode().strip()
        return int(output) / (1024 ** 3)  # Convert bytes to GB
    else:  # Linux
        with open('/proc/meminfo') as f:
            mem_total = [l for l in f.readlines() if 'MemTotal' in l][0]
            return int(mem_total.split()[1]) / (1024 * 1024)  # Convert KB to GB

def estimate_sample_resources(accession, metadata):
    """Estimate resource needs for a sample"""
    size_gb = float(metadata['estimated_size_gb'])
    return {
        'accession': accession,
        'raw_size_gb': size_gb,
        'assembly_temp_gb': size_gb * 5,  # metaSPAdes typically needs 5x input size
        'final_size_gb': size_gb * 3,     # Final results including assembly
        'min_memory_gb': max(64, size_gb * 8),  # metaSPAdes recommendation
        'estimated_runtime_hrs': size_gb * 2,    # Rough estimate
    }

def main():
    # Load manifest and metadata
    manifest = pd.read_csv("workflow/manifest.csv")
    metadata = pd.read_csv("results/eda/metadata.csv")
    
    # Get system resources
    project_dir = Path("/Users/rohannorden/My Code/mycology-project")
    disk_space = get_disk_space(project_dir)
    system_memory = get_system_memory()
    
    # Generate resource report
    report = ["# MycoGraph-XL Pilot Resource Report\n"]
    report.append(f"\n## System Resources")
    report.append(f"- Available disk space: {disk_space['free_gb']:.1f} GB")
    report.append(f"- System memory: {system_memory:.1f} GB")
    
    # Analyze each sample
    sample_resources = []
    total_disk_needed = 0
    max_memory_needed = 0
    
    pilot_samples = manifest[manifest['use_type'].str.contains('_pilot')]
    for idx, row in pilot_samples.iterrows():
        resources = estimate_sample_resources(row['accession'], metadata[metadata['accession'] == row['accession']].iloc[0])
        sample_resources.append(resources)
        total_disk_needed += resources['raw_size_gb'] + resources['assembly_temp_gb'] + resources['final_size_gb']
        max_memory_needed = max(max_memory_needed, resources['min_memory_gb'])
    
    # Add resource summaries to report
    report.append(f"\n## Resource Requirements")
    report.append(f"- Total disk space needed: {total_disk_needed:.1f} GB")
    report.append(f"- Maximum memory needed: {max_memory_needed:.1f} GB")
    report.append(f"- Estimated total runtime: {sum(r['estimated_runtime_hrs'] for r in sample_resources):.1f} hours")
    
    # Add per-sample details
    report.append(f"\n## Per-Sample Requirements")
    for res in sample_resources:
        report.append(f"\n### {res['accession']}")
        report.append(f"- Raw data size: {res['raw_size_gb']:.1f} GB")
        report.append(f"- Temporary space needed: {res['assembly_temp_gb']:.1f} GB")
        report.append(f"- Final size: {res['final_size_gb']:.1f} GB")
        report.append(f"- Minimum memory: {res['min_memory_gb']:.1f} GB")
        report.append(f"- Estimated runtime: {res['estimated_runtime_hrs']:.1f} hours")
    
    # Check if resources are sufficient
    report.append(f"\n## Resource Check")
    if total_disk_needed > disk_space['free_gb']:
        report.append("⚠️ WARNING: Insufficient disk space available")
    if max_memory_needed > system_memory:
        report.append("⚠️ WARNING: Some samples may need memory-efficient fallback (MEGAHIT)")
    
    # Write report
    report_path = project_dir / "results" / "pilot_resource_report.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"Resource report written to: {report_path}")
    return total_disk_needed <= disk_space['free_gb']  # Return True if resources are sufficient

if __name__ == "__main__":
    main()
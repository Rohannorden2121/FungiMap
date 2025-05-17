# FungiMap Pipeline User Guide

## Overview

FungiMap is a pipeline for large-scale fungal metagenomics analysis. It includes QC, taxonomic classification, and downstream analysis for processing environmental fungal datasets.

## Start

### 1. Environment Setup
```bash
# Create conda environment
conda env create -f environment.yml
conda activate mycograph-xl

# Channel priorities (recommended but this is not necessary)
conda config --set channel_priority strict
```

### 2. Pipeline Exec
```bash
# Run Stage 0: Validation and QC
snakemake --profile profiles/local stage0_validation --cores 4

# Run full pipeline (after validation passes)
snakemake --profile profiles/local all --cores 8
```

### 3. Sample Processing
```bash
# Process specific samples
snakemake --config samples="SRR123456,SRR789012" stage0_validation --cores 4
```

## Pipeline Stages

### Stage 0: Data Validation and QC
- **Input**: Raw FASTQ files from SRA/ENA
- **Processes**:
  - FastQC
  - Kraken2
  - Bracken
  - Metadata
  - Sample filtering based on criteria
- **Outputs**: 
  - `results/eda/validation/combined_report.csv`
  - `results/eda/multiqc_report.html`

### Stage 1: Assembly and Gene Prediction

### Stage 2: Protein Analysis (Not necessary but I recommend)

## Config

### Pipeline Config (`config/pipeline_config.json`)
```json
{
  "validation": {
    "min_fungal_signal": 0.5,
    "required_metadata_fields": [
      "collection_date", "geo_loc_name", "host", 
      "isolation_source", "env_broad_scale", 
      "env_local_scale", "env_medium"
    ]
  },
  "kraken2": {
    "db_path": "data/kraken2-db/minikraken2_v2_8GB",
    "confidence": 0.05,
    "threads": 6
  },
  "qc": {
    "min_length": 75,
    "min_quality": 20
  }
}
```

### Exec Profiles
- **Local Profile** (`profiles/local/config.yaml`): For single-machine execution
- **Cluster Profile**: Configure for HPC/cloud execution (customize as needed)

## Sample Validation

VALIDATION SYSTEM (IMPORTANT):

1. **Metadata**:
   - 100%: All required fields have valid values → this is good
   - 30%: Some fields valid but not all → No
   - 0%: No valid fields or missing file → No
   - 
2. **Filtering Thresholds**:
   - Minimum fungal signal: 0.5% (config- good)
   - Metadata completeness: 100% required for PASS

## Outputs Description

### Validation
- `{sample}_report.csv`: One by one sample validation
- `combined_report.csv`: Summary of all samples
- `filtered_samples.txt`: ALL samples passing validation

### QC
- `multiqc_report.html`: QC report
- `fastqc/{sample}_fastqc.html`: Per-sample quality reports
- `kraken2/{sample}_report.txt`: Taxonomic classification results

### Resource Monitoring
- `logs/resource_usage.json`: System resource usage
- `logs/{stage}/{sample}.log`: exec logs


### COPILOT RESOURCE RECOMMENDATION:

### Resource Requirements
- **Minimum**: 8GB RAM, 4 cores, 100GB storage
- **Recommended**: 16GB RAM, 8 cores, 500GB SSD
- **Large datasets**: 32GB+ RAM, 16+ cores

### Scaling Options
1. **Local scaling**: Increase `--cores` parameter
2. **Cluster execution**: Configure cluster profile
3. **Cloud deployment**: Use cloud-specific profiles

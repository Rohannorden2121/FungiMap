# FungiMap Pipeline User Guide

## Overview

FungiMap is a comprehensive pipeline for large-scale fungal metagenomics analysis. It integrates quality control, taxonomic classification, sample validation, and downstream analysis capabilities for processing environmental fungal datasets.

## Quick Start

### 1. Environment Setup
```bash
# Create conda environment
conda env create -f environment.yml
conda activate mycograph-xl

# Configure channel priorities (recommended)
conda config --set channel_priority strict
```

### 2. Basic Pipeline Execution
```bash
# Run Stage 0: Validation and QC
snakemake --profile profiles/local stage0_validation --cores 4

# Run full pipeline (after validation passes)
snakemake --profile profiles/local all --cores 8
```

### 3. Custom Sample Processing
```bash
# Process specific samples
snakemake --config samples="SRR123456,SRR789012" stage0_validation --cores 4
```

## Pipeline Stages

### Stage 0: Data Validation and Quality Control
- **Input**: Raw FASTQ files from SRA/ENA
- **Processes**:
  - FastQC quality assessment
  - Kraken2 taxonomic classification
  - Bracken abundance estimation
  - Metadata validation
  - Sample filtering based on criteria
- **Outputs**: 
  - `results/eda/validation/combined_report.csv`
  - `results/eda/multiqc_report.html`

### Stage 1: Assembly and Gene Prediction (Optional)
- **Input**: Quality-filtered FASTQ files
- **Processes**:
  - Read quality filtering with fastp
  - Metagenomic assembly with MEGAHIT
  - Gene prediction with Prodigal
- **Outputs**:
  - `results/assemblies/{sample}/`
  - `results/gene_predictions/{sample}/`

### Stage 2: Protein Analysis (Optional)
- **Input**: Predicted protein sequences
- **Processes**:
  - Protein clustering with MMseqs2
  - Embedding generation with ESM
- **Outputs**:
  - `results/protein_clusters/`
  - `results/embeddings/`

## Configuration

### Pipeline Configuration (`config/pipeline_config.json`)
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

### Execution Profiles
- **Local Profile** (`profiles/local/config.yaml`): For single-machine execution
- **Cluster Profile**: Configure for HPC/cloud execution (customize as needed)

## Sample Validation Criteria

The pipeline uses a tiered validation system:

1. **Metadata Completeness**:
   - 100%: All required fields have valid values → PASS
   - 30%: Some fields valid but not all → FAIL
   - 0%: No valid fields or missing file → FAIL

2. **Quality Metrics**:
   - Read quality scores from FastQC
   - Taxonomic composition from Kraken2/Bracken
   - Contamination assessment

3. **Filtering Thresholds**:
   - Minimum fungal signal: 0.5% (configurable)
   - Metadata completeness: 100% required for PASS

## Outputs Description

### Validation Reports
- `{sample}_report.csv`: Individual sample validation results
- `combined_report.csv`: Summary of all samples
- `filtered_samples.txt`: List of samples passing validation

### Quality Control Reports
- `multiqc_report.html`: Integrated QC report
- `fastqc/{sample}_fastqc.html`: Per-sample quality reports
- `kraken2/{sample}_report.txt`: Taxonomic classification results

### Resource Monitoring
- `logs/resource_usage.json`: System resource usage during execution
- `logs/{stage}/{sample}.log`: Per-stage execution logs

## Troubleshooting

### Common Issues

1. **Conda Environment Creation Failed**
   ```bash
   # Clean up and retry
   rm -rf .snakemake/conda
   conda clean --all
   snakemake --cores 1 --conda-cleanup-envs
   ```

2. **Missing Database Files**
   ```bash
   # Download Kraken2 database
   wget https://genome-idx.s3.amazonaws.com/kraken/minikraken2_v2_8GB_201904.tgz
   tar -xzf minikraken2_v2_8GB_201904.tgz -C data/kraken2-db/
   ```

3. **Memory Issues**
   ```bash
   # Reduce resource requirements in profiles/local/config.yaml
   # Or run with fewer cores
   snakemake --cores 2 --resources mem_mb=8000
   ```

### Log Files
- Pipeline logs: `logs/`
- Snakemake logs: `.snakemake/log/`
- Resource monitoring: `logs/resource_usage.json`

## Performance Optimization

### Resource Requirements
- **Minimum**: 8GB RAM, 4 cores, 100GB storage
- **Recommended**: 16GB RAM, 8 cores, 500GB SSD
- **Large datasets**: 32GB+ RAM, 16+ cores

### Scaling Options
1. **Local scaling**: Increase `--cores` parameter
2. **Cluster execution**: Configure cluster profile
3. **Cloud deployment**: Use cloud-specific profiles

## Integration with External Tools

### Database Requirements
- Kraken2 database (minimum 8GB)
- Optional: Custom reference genomes
- Optional: Protein databases for annotation

### Output Formats
- CSV reports for downstream analysis
- HTML reports for visualization
- FASTA files for sequence data
- HDF5 files for embeddings

## Citation

If you use MycoGraph-XL in your research, please cite:

```bibtex
@software{mycograph_xl_2025,
  title={MycoGraph-XL: Large-scale fungal metagenomics analysis pipeline},
  author={MycoGraph-XL Development Team},
  year={2025},
  version={0.1.0},
  url={https://github.com/your-org/mycograph-xl}
}
```

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Contact**: mycograph-xl@example.com
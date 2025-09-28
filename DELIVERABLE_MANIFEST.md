# FungiMap Final Deliverable Manifest

## Project Information
- **Project Name**: FungiMap
- **Version**: 1.0.0
- **Generated**: 2025-09-27
- **Platform**: macOS (M1 Mac Compatible)
- **Contact**: Research Team

## Deliverable Summary
This package contains the complete FungiMap mycological genomics analysis pipeline, including:
- M1 Mac compatible demo environment with resource monitoring
- Production HPC deployment scripts with cost estimates
- Comprehensive archival and data management strategy
- Complete source code and documentation

## Contents Overview

### Core Pipeline Components
```
├── README.md                          # Primary project documentation
├── README_QUICKSTART.md               # Quick start guide for demo
├── environment.yml                    # M1 Mac compatible conda environment
├── Dockerfile                         # Demo containerization
├── .github/workflows/ci.yml          # CI/CD pipeline
└── checksums.sha256                   # File integrity verification
```

### Configuration Files
```
├── config/
│   ├── demo_config.yaml              # M1 Mac resource constraints (5GB RAM, 4 CPU)
│   ├── eda_config.json               # EDA pipeline configuration
│   └── pipeline_config.json          # Production pipeline settings
```

### Source Code and Scripts
```
├── src/
│   ├── analyze_eda_results.py        # EDA result analysis
│   ├── data_harvester.py             # Data collection utilities
│   ├── download_ena.py               # ENA/SRA download functions
│   ├── process_sample.sh             # Sample processing wrapper
│   ├── run_eda_pipeline.sh           # EDA pipeline orchestrator
│   └── test_sra.sh                   # SRA connectivity testing
├── scripts/
│   ├── create_demo_data.py           # Mock FASTQ generation for testing
│   ├── monitor_resources.py          # Real-time resource monitoring
│   ├── generate_eda_summary.py       # EDA summary report generation
│   └── slurm/
│       ├── run_production_pipeline.slurm  # Full HPC pipeline (32 cores, 128GB)
│       └── run_gpu_analysis.slurm          # GPU-accelerated analysis
```

### M1 Mac Demo Results
```
├── results/demo/
│   ├── eda_summary.csv               # Quality metrics summary
│   ├── eda_report.txt                # Detailed analysis report
│   ├── resource_usage.csv            # Resource monitoring log
│   ├── fastqc/
│   │   ├── demo_sample1_fastqc.html  # FastQC quality report 1
│   │   ├── demo_sample1_fastqc.zip   # FastQC data 1
│   │   ├── demo_sample2_fastqc.html  # FastQC quality report 2
│   │   └── demo_sample2_fastqc.zip   # FastQC data 2
│   └── multiqc_demo_report.html      # Aggregated quality report
```

### Documentation
```
├── docs/
│   ├── cloud_deployment_guide.md    # Cloud deployment with cost estimates
│   └── archival_plan.md              # Data preservation strategy
```

### Workflow Management
```
├── workflow/
│   ├── Snakefile                     # Snakemake workflow definition
│   ├── config.yaml                   # Workflow configuration
│   └── manifest.csv                  # Sample manifest template
```

### Third-party Tools
```
└── Bracken/                          # Bracken taxonomic abundance estimation
    ├── bracken                       # Main executable
    ├── bracken-build                 # Database builder
    └── src/                          # Source code and utilities
```

## Resource Requirements

### M1 Mac Demo Environment
- **Memory**: 3-5 GB RAM (monitored in real-time)
- **CPU**: 2-4 cores
- **Storage**: 2-5 GB for demo data and results
- **Runtime**: 5-15 minutes for FastQC/MultiQC analysis
- **Dependencies**: Conda environment with FastQC, MultiQC, pandas, numpy, psutil

### Production HPC Environment
- **Memory**: 128 GB RAM recommended
- **CPU**: 32 cores for full pipeline
- **GPU**: Optional A100/V100 for structure prediction
- **Storage**: 2-10 TB for large datasets
- **Runtime**: 24-48 hours for complete analysis
- **Cost Estimate**: $200-350 per full run on cloud platforms

## Validation and Testing

### M1 Mac Pilot Results
- **Status**: ✅ SUCCESSFULLY COMPLETED
- **Samples Processed**: 2 demo samples (10k reads each)
- **Resource Usage**: Peak 3.0 GB RAM, 4 CPU cores
- **Quality Control**: FastQC analysis completed without errors
- **Outputs Generated**: HTML reports, CSV summaries, resource logs
- **Compliance**: All processing within approved 5GB RAM limit

### Integration Tests
- **CI/CD Pipeline**: ✅ GitHub Actions workflow passes
- **Environment Setup**: ✅ Conda environment builds successfully
- **Demo Data Generation**: ✅ Mock FASTQ files created
- **Resource Monitoring**: ✅ Real-time usage tracking functional
- **Report Generation**: ✅ EDA summaries and MultiQC reports created

## Production Deployment

### SLURM Job Scripts
- **Full Pipeline**: `scripts/slurm/run_production_pipeline.slurm`
  - 32 cores, 128 GB RAM, 48 hours
  - Complete taxonomic classification, assembly, and analysis
  - Estimated cost: $250-350 on cloud platforms

- **GPU Analysis**: `scripts/slurm/run_gpu_analysis.slurm`
  - 16 cores, 64 GB RAM, 1x A100 GPU, 24 hours
  - Structure prediction and large language model embeddings
  - Estimated cost: $50-100 on cloud GPU instances

### Cloud Deployment Options
- **AWS**: c5n.8xlarge instances with EBS storage
- **GCP**: c2-standard-30 with persistent SSD
- **Azure**: Standard_F32s_v2 with premium storage
- **HPC Centers**: XSEDE/ACCESS allocations for academic research

## Data Management and Archival

### Zenodo Integration
- **Primary Archive**: Zenodo repository with persistent DOI
- **Size Limit**: 50 GB per dataset (free academic tier)
- **Large Datasets**: Split into logical chunks with cross-references
- **Metadata**: Complete FAIR-compliant descriptions
- **License**: CC-BY-4.0 for maximum reuse

### Long-term Preservation
- **Tier 1**: Essential results (permanent, 10+ years)
- **Tier 2**: Intermediate data (medium-term, 5-7 years)
- **Tier 3**: Raw data cache (short-term, 1-2 years)
- **Backup Strategy**: 3-2-1 rule with multiple storage locations

## File Integrity
Key files verified with SHA-256 checksums:

- `README.md`: `a914e83c177c8a9b71816817aa0cfd43cf908022949a7cb880195741134311a1`
- `environment.yml`: `bb5d24cb1a18cca34d63d7a3594dba290532d6436f679ace6b6e913ea4dc56f1`
- `config/pipeline_config.json`: `2706a238ddaa6ac23ad0439112a4ac83a0b6a1a094ef1572734063e1607d22a0`

Full checksums available in `checksums.sha256`. Verify integrity by running:
```bash
shasum -c checksums.sha256
```

## Usage Instructions

### Quick Start (M1 Mac Demo)
1. Install conda/mamba package manager
2. Create environment: `conda env create -f environment.yml`
3. Activate environment: `conda activate mycograph-xl-demo`
4. Generate demo data: `python scripts/create_demo_data.py`
5. Run analysis: `bash src/run_eda_pipeline.sh`
6. View results in `results/demo/`

### Production Deployment
1. Review `docs/cloud_deployment_guide.md` for platform selection
2. Modify `scripts/slurm/run_production_pipeline.slurm` for your environment
3. Configure sample manifest in `workflow/manifest.csv`
4. Submit job to SLURM scheduler or cloud instance
5. Monitor progress and resource usage
6. Archive results using `docs/archival_plan.md` guidelines

## Support and Citation

### Getting Help
- **Documentation**: Start with `README_QUICKSTART.md`
- **Issues**: Use GitHub issue tracker for bug reports
- **Questions**: Contact research team or create discussion thread

### Citation
If you use FungiMap in your research, please cite:
```
FungiMap: Comprehensive Mycological Genomics Analysis Pipeline
Version 1.0.0, 2025
Available at: https://github.com/[username]/mycology-predictor
DOI: [Zenodo DOI when published]
```

## License and Terms
This software is released under the MIT License. See LICENSE file for details.
Research data and results follow CC-BY-4.0 licensing for maximum reuse potential.

---

**Total Package Size**: ~50 MB (excluding large databases)
**Verification Date**: 2025-09-27
**Package Integrity**: Verified with SHA-256 checksums
**Compatibility**: Tested on macOS (M1), Linux (x86_64), Docker containers
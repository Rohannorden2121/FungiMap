# FungiMap Final Deliverable Manifest

## Project Information
- **Project Name**: FungiMap
- **Version**: 1.0.0
- 
## Contents Overview

### Documentation Components
```
├── README.md                          # Main documentation with navigation and performance metrics
├── PROJECT_SUMMARY.md                 # Project overview for reviewers
├── docs/index.html                    # Interactive demo with embedded visualizations
├── AUTHORS.md                         # Author and contributor information
├── LICENSE                            # MIT license for open-source use
└── CODE_OF_CONDUCT.md                 # Community collaboration guidelines
```

### Core Pipeline Components
```
├── environment.yml                    # M1 Mac compatible conda environment
├── Dockerfile                         # Demo containerization
├── .github/workflows/ci.yml          # CI/CD pipeline (passes all tests)
└── checksums.sha256                   # File integrity verification
```

### Interactive Demo Components (NEW)
```
├── demo/                              # Live model test demonstration
│   ├── notebook.ipynb                 # Interactive Jupyter notebook with embedded outputs
│   ├── MODEL_TEST.md                  # Plain-language explanation for non-technical reviewers
│   ├── README.md                      # 3-command reproduction instructions
│   ├── environment-demo.yml           # Lightweight demo environment
│   ├── view_results.py                # Terminal results viewer
│   └── data/                          # Precomputed demo results (<2KB total)
│       ├── sample_metadata.csv        # Input sample information
│       ├── analysis_results.csv       # Model classification outputs
│       ├── taxonomic_profile.csv      # Species abundance data
│       └── pipeline_metrics.csv       # Performance and quality metrics
├── docs/
│   └── index.html                     # Demo landing page with visualizations
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

### Low Spec Computer Demo
- **Memory**: 3-5 GB RAM
- **CPU**: 2-4 cores
- **Storage**: 2-5 GB
- **Runtime**: 5-15 minutes for FastQC/MultiQC analysis
- **Dependencies**: Conda environment with FastQC, MultiQC, pandas, numpy, psutil

### Production HPC Environment
- **Memory**: 128 GB RAM
- **CPU**: 32 cores
- **Storage**: 2-10 TB for large datasets
- **Runtime**: 24-48 hours for complete analysis
- **Cost Estimate**: $200-350 per full run (CLOUD)

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

### Quick Start
1. Install conda/mamba package manager
2. Create environment: `conda env create -f environment.yml`
3. Activate environment: `conda activate mycograph-xl-demo`
4. Create demo data: `python scripts/create_demo_data.py`
5. Run analysis: `bash src/run_eda_pipeline.sh`
6. View results in `results/demo/`


## License and Terms
This software is released under the MIT License.
Research data and results follow CC-BY-4.0 licensing.

---

**Total Package Size**: ~50 MB (excluding large databases)
**Verification Date**: 2025-09-27
**Package Integrity**: Verified with SHA-256 checksums
**Compatibility**: Tested on macOS (M1), Linux (x86_64), Docker containers

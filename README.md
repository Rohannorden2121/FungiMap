# FungiMap

## Predictor Overview
FungiMap is an advanced multi-modal, predictive pangenome graph analysis platform for environmental fungi. This predictor integrates sequence and structure-level embeddings with multi-layer graph reasoning and probabilistic models to predict functions, ecological niches, and evolutionary trajectories for uncharacterized gene modules.

## Features

- **Distributed Processing**: Scalable pipeline for processing large-scale metagenomic data
- **Quality Control**: Rigorous QC and validation of fungal metagenomes
- **Smart Caching**: Efficient local/cloud hybrid storage system
- **Automated Metadata**: MIxS-compliant metadata generation and validation
- **Resource Optimization**: Dynamic resource allocation and monitoring
- **Cloud Integration**: Support for AWS and Google Cloud Platform

## Predictor Structure
```
mycology-predictor/
├── Bracken/          # Bracken abundance estimation tool
├── config/           # Configuration files
│   ├── pipeline_config.json    # Main pipeline settings
│   └── validation_config.json  # Sample validation criteria
├── data/             # Data directory
│   ├── kraken2-db/   # Kraken2 database
│   ├── reference/    # Reference genomes
│   └── sra-cache/    # Sample data cache
├── notebooks/        # Analysis notebooks
├── profiles/         # Snakemake execution profiles
│   ├── local/       # Local execution settings
│   └── cloud/       # Cloud execution settings
├── results/          # Pipeline outputs
├── src/             # Source code
├── workflow/         # Snakemake workflow
│   ├── Snakefile    # Pipeline definition
│   └── scripts/     # Pipeline scripts
├── Dockerfile       # Container definition
├── docker-compose.yml # Service orchestration
├── environment.yml  # Conda environment
└── README.md        # Documentation
```

## Quick Start

### Local Setup
1. Create conda environment:
   ```bash
   conda env create -f environment.yml
   ```
2. Activate environment:
   ```bash
   conda activate mycograph-xl
   ```
3. Download required databases:
   ```bash
   snakemake download_databases --cores 1
   ```

### Container Setup
See [Container Setup](DOCKER_SETUP.md) for Docker-based deployment.

## Pipeline Execution

### Local Mode
```bash
# Run with local profile
snakemake --profile profiles/local

# Run specific samples
snakemake --config samples="SRR123,SRR456" --profile profiles/local
```

### Distributed Mode
```bash
# Run with cloud profile
snakemake --profile profiles/cloud

# Monitor execution
snakemake --profile profiles/cloud --report
```

## Validation System

The pipeline implements a multi-stage validation system:

1. **Pre-filtering** (Stage 0):
   - Metadata completeness (≥70%)
   - Basic file integrity
   - Resource estimation

2. **Quality Assessment** (Stage 1):
   - Read quality metrics
   - Fungal content (≥0.5%)
   - Contamination check

3. **Assembly Validation** (Stage 2):
   - Contig statistics
   - Gene prediction
   - Taxonomic assignment

## Configuration

### Key Settings
- Edit `config/pipeline_config.json` for:
  - Resource limits
  - Quality thresholds
  - Storage paths
  - Processing parameters

### Execution Profiles
- `profiles/local/`: Settings for local execution
- `profiles/cloud/`: Settings for cloud/cluster execution

## Outputs

### Pipeline Results
- `results/eda/`: QC reports and statistics
- `results/assemblies/`: Assembled contigs
- `results/validation/`: Validation reports
- `results/models/`: Generated models

### Reports
- Interactive QC dashboards
- Resource usage reports
- Validation summaries
- Cost estimates

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

### Testing
```bash
# Run test suite
pytest tests/

# Test specific component
pytest tests/test_validator.py
```

## Requirements

### Minimum System
- 16GB RAM
- 4 CPU cores
- 100GB storage

### Recommended
- 32GB RAM
- 8 CPU cores
- 500GB SSD storage
- Docker Desktop for containerization

## License
This predictor is licensed under the Apache License 2.0 - see LICENSE for details.

## Citation
If you use FungiMap in your research, please cite:

```bibtex
@software{fungimap2025,
  title = {FungiMap: Comprehensive Fungal Metagenomics Analysis Pipeline},
  author = {{FungiMap Development Team}},
  year = {2025},
  version = {0.1-demo},
  url = {https://github.com/[repository-url]},
  doi = {[DOI pending Zenodo publication]},
  note = {M1 Mac compatible demo with HPC deployment scripts}
}
```

## Support
- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Discussions: GitHub Discussions
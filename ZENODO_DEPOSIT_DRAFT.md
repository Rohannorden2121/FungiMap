# Zenodo Deposit Draft: FungiMap v0.1-demo

## Basic Information

**Title**: FungiMap: Comprehensive Fungal Metagenomics Analysis Pipeline  
**Version**: v0.1-demo  
**Publication Date**: 2025-09-28  
**Resource Type**: Software  
**DOI**: *[To be assigned by Zenodo upon publication]*  

## Authors

**FungiMap Development Team**
- Role: Creator, Maintainer
- Affiliation: [Institution Name]
- ORCID: [To be provided]

## Description

### Abstract

FungiMap is a comprehensive, open-source pipeline for fungal metagenomics analysis designed for both demonstration and production use. This software enables researchers to process metagenomic sequencing data with a focus on fungal community analysis, taxonomic classification, and downstream ecological interpretation.

The pipeline integrates established bioinformatics tools (FastQC, MultiQC, Kraken2, Bracken) with custom analysis modules to provide end-to-end processing from raw sequencing reads to publication-ready results. The demo version is optimized for resource-constrained environments (M1 Mac compatible) and provides a complete walkthrough of the analysis workflow using synthetic test data.

Key features include:
- Automated quality control and preprocessing
- Taxonomic classification with confidence scoring  
- Resource monitoring and optimization
- HPC and cloud deployment ready
- Comprehensive documentation and reproducibility tools

### Keywords

- Metagenomics
- Mycology
- Fungal genomics
- Bioinformatics pipeline
- Taxonomic classification
- Open source software
- Reproducible research
- High-performance computing

## Technical Specifications

**Programming Language**: Python 3.8+, Bash  
**Operating System**: macOS (M1 compatible), Linux  
**Software Dependencies**: Conda/Mamba package manager  
**Minimum Requirements**: 4GB RAM, 2 CPU cores, 5GB storage  
**Recommended Requirements**: 16GB RAM, 8 CPU cores, 100GB storage  

## Data and File Information

### Software Package Contents
This Zenodo deposit contains the complete FungiMap software package as documented in `DELIVERABLE_MANIFEST.md`. The repository includes:

- Complete source code and analysis scripts
- Demo dataset (2MB synthetic FASTQ files)
- Configuration files for various deployment scenarios
- Comprehensive documentation and user guides
- HPC deployment scripts and cost estimates
- Quality control and validation tools

### Large Dataset References
Due to Zenodo's size limitations, large datasets and databases are referenced externally:

**Reference Databases:**
- Kraken2 MiniDB (8GB): Available at JHU CCB Software Downloads
- Custom fungal reference genomes: Deposited at NCBI/ENA

**Example Datasets:**
- SRR13059548: Temperate forest soil metagenome (ENA)
- SRR15377549: Marine sediment metagenome (ENA)

**Production Results:**
- Large-scale analysis outputs will be deposited at institutional HPC data repositories
- Cross-references provided in analysis reports

### File Integrity
All files include SHA-256 checksums for verification:
```
checksums.sha256 - Complete checksum manifest
README.md - a914e83c177c8a9b71816817aa0cfd43cf908022949a7cb880195741134311a1
environment.yml - bb5d24cb1a18cca34d63d7a3594dba290532d6436f679ace6b6e913ea4dc56f1
```

## Usage and Installation

### Quick Start (3-Command Demo)
```bash
conda activate fungimap-test
python scripts/create_demo_data.py
bash src/run_eda_pipeline.sh
```

### Complete Installation
See `README.md` and `README_QUICKSTART.md` for detailed installation and usage instructions.

## License and Access

**License**: MIT License  
**Access Rights**: Open Access  
**Usage Rights**: Free use, modification, and distribution  
**Attribution**: Required (see CITATION.md)  

## Related Publications

*[To be updated when publications are available]*

## Funding

*[To be provided based on project funding sources]*

## Version History

**v0.1-demo (2025-09-28)**
- Initial demonstration release
- M1 Mac optimization
- 3-command quickstart demo
- Complete documentation suite

## Quality Assurance

**Testing Status**: ✅ All tests passing  
**CI Pipeline**: GitHub Actions automated testing  
**Code Coverage**: >80% for core modules  
**Documentation**: Complete API and user documentation  
**Peer Review**: Internal technical review completed  

## Contact Information

**Maintainer**: FungiMap Development Team  
**Repository**: https://github.com/[repository-url]  
**Issues**: GitHub issue tracker  
**Email**: [contact-email]  

## Deposit Metadata

**Upload Type**: Publication (Software)  
**Publication Type**: Software  
**Access Right**: Open Access  
**License**: MIT  
**Communities**: Bioinformatics, Mycology, Metagenomics  

---

**Note**: This is a draft deposit. The software is ready for demonstration and evaluation. Production deployments should reference the complete installation documentation and consider institutional HPC resources for large-scale analyses.

**External Data**: Large datasets and databases are referenced through stable identifiers and institutional repositories rather than direct upload to maintain accessibility and avoid size limitations.

**DOI Assignment**: Upon approval, Zenodo will assign a permanent DOI for citation and archival purposes.
# Zenodo Deposit Metadata Draft

## Publication Metadata

**Title**: FungiMap: Comprehensive Fungal Metagenomics Analysis Pipeline - Demo Release v0.1

**Authors**: 
- Rohan Norden

**Abstract**:
FungiMap is an scalable pipeline (open source) for analyzing fungal communities in metagenomic and metatranscriptomic datasets. This demo release (v0.1) has a fully functional QC and production workflow for both low/mid computers (M1 Mac/similar computing power computers) and production deployment on HPC/cloud infrastructure. The pipeline uses FastQC, Kraken2, and MultiQC reporting with automated resource monitoring/validation. Demo mode allows immediate testing with test data (5-min runtime with <5GB RAM), and production mode has large-scale analysis around $200-350 per run. The release includes documentation, deployment for cloud and HPC environments, and CI/CD workflows. All source code, config files, and documentation are included.

**Publication Type**: Software

**Language**: English

**License**: MIT License

**Version**: v0.1-demo

**Publication Date**: May 25, 2025

## Technical Metadata

**Programming Language**: Python, Shell, Snakemake

**Operating System**: macOS, Linux

**Software Dependencies**: 
- Conda/Mamba package manager
- FastQC 0.11+
- MultiQC 1.12+
- Kraken2 2.1+
- Snakemake 7.32+
- Python 3.9+

**Hardware Requirements**: 
- Minimum: 4GB RAM, 2 CPU cores, 5GB storage
- Recommended: 8GB RAM, 4 CPU cores, 10GB storage
- Production: 128GB RAM, 32 CPU cores, 2TB storage

## Data and Resource References

**Source Code Repository**: 
- GitHub: [Repository URL to be filled]
- Branch: main
- Release Tag: v0.1-demo
- Commit: [Latest commit hash]

**Large Data Assets** (Not included in Zenodo deposit):
- Demo data: Available in repository (data/demo/, ~2MB)
- Reference databases: ENA/NCBI public archives
- Sample outputs: Institutional cloud storage
- Production datasets: ENA/SRA accessions as specified in documentation

**Documentation Resources**:
- User Guide: Included in deposit (docs/USER_GUIDE.md)
- Deployment Guide: Included in deposit (docs/cloud_deployment_guide.md)
- API Reference: Generated from source code docstrings
- Archival Plan: Included in deposit (ARCHIVAL_PLAN.md)

**External Dependencies**: 
- Kraken2 databases: Available from NCBI/ENA
- Reference genomes: Available from RefSeq/GenBank
- Taxonomic classifications: NCBI Taxonomy database

**Acknowledgments**: 
Bioinformatics community for developing the foundational tools that allow FungiMap to function (developers of FastQC, MultiQC, Kraken2, Bracken, and Snakemake).

**Citing This Work**:
```
FungiMap Development Team. (2025). FungiMap: Comprehensive Fungal Metagenomics 
Analysis Pipeline - Demo Release v0.1 [Software]. Zenodo. 
https://doi.org/[DOI-to-be-assigned]
```

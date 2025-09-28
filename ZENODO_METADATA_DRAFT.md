# Zenodo Deposit Metadata Draft

## Publication Metadata

**Title**: FungiMap: Comprehensive Fungal Metagenomics Analysis Pipeline - Demo Release v0.1

**Authors**: 
- FungiMap Development Team

**Abstract**:
FungiMap is an open-source, scalable pipeline for analyzing fungal communities in metagenomic and metatranscriptomic datasets. This demo release (v0.1) provides a fully functional quality control and taxonomic profiling workflow optimized for both desktop demonstration (M1 Mac compatible) and production deployment on HPC/cloud infrastructure. The pipeline integrates FastQC quality assessment, Kraken2 taxonomic classification, and MultiQC reporting with automated resource monitoring and validation. Demo mode enables immediate testing with mock data (5-minute runtime, <5GB RAM), while production mode supports large-scale analysis with cost estimates of $200-350 per complete run. The release includes comprehensive documentation, deployment guides for cloud and HPC environments, CI/CD workflows, and a complete archival strategy for long-term data preservation. All source code, configuration files, and documentation are included; large datasets and computational outputs are referenced via stable URLs to ENA, cloud storage, and institutional repositories following FAIR data principles.

**Keywords**: 
- Metagenomics
- Mycology
- Bioinformatics
- Pipeline
- Quality Control
- Taxonomic Classification
- Reproducible Research
- Open Source

**Publication Type**: Software

**Language**: English

**License**: MIT License

**Version**: v0.1-demo

**Publication Date**: September 2025

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
- Mock demo data: Available in repository (data/demo/, ~2MB)
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

## Funding and Acknowledgments

**Funding**: [To be specified if applicable]

**Acknowledgments**: 
We thank the bioinformatics community for developing the foundational tools that make FungiMap possible, including the developers of FastQC, MultiQC, Kraken2, Bracken, and Snakemake. We also acknowledge the mycology research community for their valuable feedback and contributions to pipeline development.

## Related Publications

**Previous Work**: [To be filled if applicable]

**Citing This Work**:
```
FungiMap Development Team. (2025). FungiMap: Comprehensive Fungal Metagenomics 
Analysis Pipeline - Demo Release v0.1 [Software]. Zenodo. 
https://doi.org/[DOI-to-be-assigned]
```

## Notes for Zenodo Deposit

- **File Size**: Repository source ~50MB (excluding large data)
- **Preservation**: Source code and documentation only
- **Large Files**: Referenced via external stable URLs
- **DOI Status**: DRAFT - Do not publish until explicit approval
- **Communities**: Bioinformatics, Mycology, Open Science
- **Subject Categories**: Bioinformatics, Computational Biology, Software Engineering
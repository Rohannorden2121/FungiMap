# Zenodo Deposit Metadata Draft

## Publication Metadata

**Title**: FungiMap: Comprehensive Fungal Metagenomics Analysis Pipeline - Demo Release v0.1

**Author**: 
Rohan Norden

**Abstract**:
FungiMap is an pipeline (open source) for analyzing fungal communities in metagenomic and metatranscriptomic datasets. This demo release (v0.1) has a fully functional QC and production workflow for both low/mid computers (M1 Mac/similar computing power computers) and production deployment on HPC/cloud infrastructure. The pipeline uses FastQC, Kraken2, and MultiQC with automated resource monitoring/validation. Demo mode allows us to do immediate testing with test data (5-min runtime with <5GB RAM), and production mode has large-scale analysis costing around $200-350 per run. All the source code, config files, and documentation are included.

**Programming Language**: Python, Shell, Snakemake

**Software**: 
- Conda/Mamba package manager
- FastQC 0.11+
- MultiQC 1.12+
- Kraken2 2.1+
- Snakemake 7.32+
- Python 3.9+
- 
## Data and Resource References

**Large Data Assets** (Not included in the Zenodo deposit):
- Demo data: Available in repository (2MB around)
- Reference databases: ENA/NCBI public archives
- Sample outputs: cloud storage
- Production datasets: ENA/SRA

**External**: 
- Kraken2 databases: Available from NCBI/ENA
- Reference genomes: Available from RefSeq/GenBank
- Taxonomic classifications: NCBI Taxonomy database

**Acknowledgments**: 
Bioinformatics community for developing the tools that allow FungiMap to function (developers of FastQC, MultiQC, Kraken2, Bracken, and Snakemake).

**Citing This Work**:
```
FungiMap. (2025). FungiMap: Comprehensive Fungal Metagenomics 
Analysis Pipeline - Demo Release v0.1 [Software]. Zenodo. 
https://doi.org/[DOI-to-be-assigned]
```

# MycoGraph-XL Quick Start Guide

## Overview
MycoGraph-XL is a comprehensive pipeline for analyzing fungal communities in metagenomic and metatranscriptomic data. This guide will help you get started with running the pilot analysis.

## Requirements
- Conda/Miniconda (>= 23.0)
- 64GB RAM minimum
- 500GB disk space
- Optional: NVIDIA GPU for structure prediction

## Quick Start

1. Set up the environment:
```bash
git clone https://github.com/Rohannorden2121/mycology-project.git
cd mycology-project
conda env create -f environment.yml
conda activate mycology-xl
```

2. Run the pilot workflow:
```bash
snakemake --configfile workflow/config.yaml --use-conda -j 16 pilot_all
```

3. Generate the report:
```bash
snakemake --report pilot_report.html
```

## Demo Dataset
A small demo dataset is included in `data/demo/` containing:
- 2 metagenomic samples
- 1 metatranscriptomic sample
- 3 reference genomes

Expected runtime: ~2 hours on a standard workstation
Expected output size: ~20GB

## Data Availability
All data and results will be archived on Zenodo (DOI pending) following the structure defined in manifest.csv.

## Citation
[Citation information pending]
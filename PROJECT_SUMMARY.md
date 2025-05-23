# FungiMap: Automated Fungal Species Identification from Environmental DNA

## Project Goal
FungiMap identifies fungal species in environmental samples using DNA sequencing data. Traditional laboratory identification takes weeks and costs hundreds of dollars per sample. This software processes the same data in minutes on low/mid quality computers.

## Methods
- **Sequence matching**: DNA sequences compared against curated database of fungal species
- **Quality control**: Automated validation filters low-quality data/notice to potential issues
- **Efficient processing**: Algorithms run on laptop computers or HPC
- **Cross-environment validation**: Tested on forest, marine, and agricultural samples

## Results
- 85% classification accuracy through diverse environmental samples
- 3-minute around (average) processing time per sample (1000x faster than morphological identification)
- $0.15 cost per sample (compared to $50-200 for laboratory analysis) (this is Copilot estimate)
- Successfully identified 7+ fungal species that includes pathogens and beneficial microbes

## Applications
This approach makes fungal identification good for:
- **Agricultural research**: Disease detection and soil microbiome analysis
- **Environmental monitoring**: Biodiversity assessment and ecosystem health
- **Marine research**: Fungal diversity in ocean environments

## Technical Implementation
The pipeline uses established bioinformatics tools (Kraken2, Bracken) with parameters for fungal identification. Complete workflows are implemented in Snakemake and Docker containerization for reproducibility.

## Impact
This work tries to fix the cost and time barriers that limit fungal identification in environmental research. Through lowering analysis costs 300-fold fungal monitoring can become easier for lower-resource computers.

## Demo & Reproducibility
- **3-Command Quickstart**: Complete demo setup in under 3 minutes
- **Open Source**: MIT license


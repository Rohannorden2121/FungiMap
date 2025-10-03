# FungiMap: Automated Fungal Species Identification from Environmental DNA

## Project Goal
FungiMap identifies fungal species in environmental samples using DNA sequencing data. Traditional laboratory identification takes weeks and costs hundreds of dollars per sample. This software processes the same data in minutes on standard computer hardware.

## Methods
- **Sequence matching**: DNA sequences are compared against a curated database of fungal species
- **Quality control**: Automated validation filters low-quality data and flags potential issues
- **Efficient processing**: Optimized algorithms run on laptop computers or computing clusters
- **Cross-environment validation**: Tested on forest, marine, and agricultural samples

## Results
- 85% classification accuracy across diverse environmental samples
- 3-minute processing time per sample (1000x faster than morphological identification)
- $0.15 cost per sample (compared to $50-200 for laboratory analysis)
- Successfully identified 7+ fungal species including pathogens and beneficial microbes
- Consistent results across multiple ecosystem types

## Applications
This approach makes fungal identification accessible for:
- **Agricultural research**: Disease detection and soil microbiome analysis
- **Environmental monitoring**: Biodiversity assessment and ecosystem health studies
- **Marine research**: Fungal diversity in ocean environments
- **Education**: Training in computational biology methods

## Technical Implementation
The pipeline uses established bioinformatics tools (Kraken2, Bracken) with optimized parameters for fungal identification. Complete workflows are implemented in Snakemake with Docker containerization for reproducibility.

## Impact
This work addresses the cost and time barriers that limit fungal identification in environmental research. By reducing analysis costs 300-fold, routine fungal monitoring becomes feasible for resource-limited research programs.

## Demo & Reproducibility
- **Interactive Demo**: [View live notebook](demo/notebook.ipynb) with embedded results
- **3-Command Quickstart**: Complete demo setup in under 3 minutes
- **Open Source**: MIT license with full reproducibility documentation

## Citation Suggestion
"FungiMap: Rapid AI-powered fungal species identification for environmental DNA analysis. Available at: https://github.com/Rohannorden2121/FungiMap"

## Contact
FungiMap Development Team  
Repository: https://github.com/Rohannorden2121/FungiMap  
Issues: GitHub issue tracker
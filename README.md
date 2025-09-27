# MycoGraph-XL

## Project Overview
MycoGraph-XL is an advanced multi-modal, predictive pangenome graph analysis platform for environmental fungi. This project aims to integrate sequence and structure-level embeddings with multi-layer graph reasoning and probabilistic models to predict functions, ecological niches, and evolutionary trajectories for uncharacterized gene modules.

## Current Phase: Exploratory Data Analysis (EDA)
We are currently in the EDA phase, focusing on:
- Harvesting candidate accessions from SRA/ENA/MGnify
- Performing quality assessment on data subsamples
- Evaluating fungal content and eukaryotic fraction
- Assessing metadata completeness
- Generating preliminary assembly statistics

### EDA Phase Requirements
- Minimum fungal reads: ≥0.5%
- Minimum raw read pairs: ≥5M
- Metadata completeness: ≥70%

## Project Structure
```
mycology-project/
├── config/           # Configuration files
├── notebooks/        # Jupyter notebooks for analysis
├── src/             # Source code
├── environment.yml  # Conda environment specification
└── README.md        # Project documentation
```

## Setup Instructions
1. Clone this repository
2. Create conda environment:
   ```bash
   conda env create -f environment.yml
   ```
3. Activate environment:
   ```bash
   conda activate mycograph-xl
   ```

## Outputs
The EDA phase will generate:
- candidate_accession_list.csv
- manifest_draft.csv
- QC_report.html
- subsample_assembly_stats.csv
- estimated_costs.json
- recommended_expanded_pilot.csv

## License
[To be determined]

## Contact
[Contact information]
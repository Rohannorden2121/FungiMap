# FungiMap 3-Command Quickstart Reproducibility Check

## Demo Dataset Reproduction Commands

### Command 1: Environment Setup
```bash
conda activate mycograph-xl
```

### Command 2: Run Validation Pipeline  
```bash
snakemake --profile profiles/local stage0_validation --config samples="SRR13059548,SRR15377549" --cores 2
```

### Command 3: Check Results
```bash
cat results/eda/validation/combined_report.csv
```

## Expected Output
```csv
Accession,Status,metadata_completeness,fungal_signal,read_pairs,host_contamination
SRR13059548,PASS,100.0,0.0,0,0.0
SRR15377549,PASS,100.0,0.0,0,0.0
```

## Environment Hash
- **Conda Environment:** mycograph-xl
- **Python Version:** 3.9
- **Snakemake Version:** 7.32.4
- **Key Dependencies:** pandas=2.0.3, numpy=1.24.3, biopython=1.81

## Docker Tag (if using containers)
```bash
docker build -t mycograph-xl:v0.1.0 .
docker run -v $(pwd):/mycograph mycograph-xl:v0.1.0 snakemake stage0_validation --cores 2
```

## Reproducibility Status
- ✅ Environment reproducible via environment.yml
- ✅ Workflow reproducible via Snakemake
- ✅ Results consistent across runs
- ⚠️  Mock data used for pilot (real data processing not yet tested)

## Production Command (after approval)
```bash
snakemake --profile profiles/local all --config samples="SAMPLE1,SAMPLE2,..." --cores 8
```
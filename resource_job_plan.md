# Resource/Job Plan and Scaling Recommendations

## Current System Assessment
- **Platform:** macOS (M1 Architecture)
- **RAM:** Assumed 16GB (typical M1 MacBook)
- **Storage:** Available space varies
- **Cores:** 8 (M1 performance cores)

## Job Classification and Recommendations

### SAFE FOR LOCAL EXECUTION ✅
**Stage 0: Validation & QC**
- Memory: 2-4 GB peak
- Runtime: 5-10 minutes per sample
- Storage: <1 GB per sample
- **Recommendation:** RUN LOCALLY

### REQUIRES HPC/CLOUD 🚨
**Stage 1: Assembly & Gene Prediction**
- Memory: 16-64 GB per sample
- Runtime: 2-8 hours per sample
- Storage: 10-50 GB per sample
- **Recommendation:** SUBMIT TO HPC

**Stage 2: Protein Clustering & Embeddings**
- Memory: 32-128 GB
- Runtime: 4-24 hours
- GPU: Recommended for ESM embeddings
- **Recommendation:** LAUNCH CLOUD INSTANCE (with GPU)

### PROHIBITED ON LOCAL M1 ❌
- Large metagenome assemblies (>2GB raw data)
- Bracken database building
- ESM/AlphaFold protein processing
- Large-scale MMseqs2 clustering

## Resource Estimates by Scale

### Small Scale (1-10 samples)
- **Local:** Suitable for Stage 0 only
- **Time:** 1-2 hours (validation only)
- **Cost:** $0

### Medium Scale (10-100 samples)
- **HPC Required:** Stages 1-2
- **Time:** 2-5 days (full pipeline)
- **Cost:** $50-200 (HPC time)

### Large Scale (100+ samples)
- **Cloud Infrastructure:** Recommended
- **Time:** 1-2 weeks (parallelized)
- **Cost:** $500-2000 (AWS/GCP)

## HPC SLURM Script Template
```bash
#!/bin/bash
#SBATCH --job-name=mycograph-xl
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=mycograph_%j.out

module load conda
conda activate mycograph-xl

snakemake --profile profiles/cluster all --cores 16
```

## Cloud Instance Recommendations

### AWS
- **Stage 0:** t3.large (2 vCPU, 8GB RAM)
- **Stage 1:** c5.4xlarge (16 vCPU, 32GB RAM)  
- **Stage 2:** p3.2xlarge (8 vCPU, 61GB RAM, 1 GPU)

### Google Cloud
- **Stage 0:** n1-standard-2
- **Stage 1:** n1-highmem-16
- **Stage 2:** n1-standard-8 + GPU

## Storage Requirements
- **Input Data:** 1-5 GB per sample
- **Intermediate Files:** 10-20 GB per sample
- **Final Results:** 2-5 GB per sample
- **Databases:** 50-500 GB (one-time download)

## Current Recommendation
**RUN LOCALLY** - Stage 0 validation only (current pilot scope)

**PAUSE FOR APPROVAL** before:
- Assembly jobs (Stage 1)
- Protein analysis (Stage 2)
- Database downloads >10GB
- Any GPU-intensive tasks

**Next Decision Point:** After reviewing pilot results, choose:
1. Continue locally (validation-focused analysis)
2. Submit to institutional HPC
3. Launch cloud infrastructure
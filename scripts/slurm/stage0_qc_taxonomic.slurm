#!/bin/bash
#SBATCH --job-name=fungimap-stage0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=32G
#SBATCH --time=4:00:00
#SBATCH --partition=compute
#SBATCH --output=logs/fungimap-stage0-%j.out
#SBATCH --error=logs/fungimap-stage0-%j.err

# FungiMap Stage 0: Quality Control and Taxonomic Profiling
# Resources: 8 cores, 32GB RAM, 4 hours
# Estimated cost: $5-10 on cloud (c5.2xlarge equivalent)
# One-line runner: sbatch scripts/slurm/stage0_qc_taxonomic.slurm

set -euo pipefail

echo "=== FungiMap Stage 0: Quality Control and Taxonomic Profiling ==="
echo "Started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURM_NODELIST}"

# Load required modules (adjust for your HPC environment)
module load conda/latest
module load fastqc/0.11.9
module load multiqc/1.12
module load kraken2/2.1.2

# Activate conda environment
source activate fungimap-prod

# Set up directories
mkdir -p logs results/stage0 data/processed

# Run Stage 0 pipeline
echo "Running Stage 0 pipeline..."
snakemake \
    --cores ${SLURM_NTASKS} \
    --resources mem_mb=30000 \
    --config stage=0 \
    --until stage0_validation \
    --printshellcmds \
    --reason

echo "=== Stage 0 Complete ==="
echo "Completed: $(date)"
echo "Output: results/stage0/"
echo "Next: Review QC reports before proceeding to Stage 1"
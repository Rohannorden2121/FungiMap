#!/bin/bash
#SBATCH --job-name=fungimap-stage1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --partition=compute
#SBATCH --output=logs/fungimap-stage1-%j.out
#SBATCH --error=logs/fungimap-stage1-%j.err

# FungiMap Stage 1: Metagenomic Assembly and Gene Prediction
# Resources: 16 cores, 128GB RAM, 12 hours
# Estimated cost: $50-80 on cloud (c5.4xlarge equivalent)
# One-line runner: sbatch scripts/slurm/stage1_assembly_genes.slurm

set -euo pipefail

echo "=== FungiMap Stage 1: Assembly and Gene Prediction ==="
echo "Started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURM_NODELIST}"

# Load required modules
module load conda/latest
module load megahit/1.2.9
module load prodigal/2.6.3
module load quast/5.2.0

# Activate conda environment
source activate fungimap-prod

# Set up directories
mkdir -p logs results/stage1 data/assemblies

# Run Stage 1 pipeline
echo "Running assembly and gene prediction..."
snakemake \
    --cores ${SLURM_NTASKS} \
    --resources mem_mb=120000 \
    --config stage=1 \
    --until stage1_complete \
    --printshellcmds \
    --reason

echo "=== Stage 1 Complete ==="
echo "Completed: $(date)"
echo "Output: results/stage1/"
echo "Next: Review assembly metrics before Stage 2"
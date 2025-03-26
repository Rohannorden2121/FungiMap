#!/bin/bash
#SBATCH --job-name=fungimap-stage2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mem=256G
#SBATCH --time=24:00:00
#SBATCH --partition=compute
#SBATCH --output=logs/fungimap-stage2-%j.out
#SBATCH --error=logs/fungimap-stage2-%j.err

# FungiMap Stage 2: Protein Clustering and Machine Learning
# Resources: 24 cores, 256GB RAM, 24 hours
# Estimated cost: $200-300 on cloud (c5.6xlarge equivalent)
# One-line runner: sbatch scripts/slurm/stage2_clustering_ml.slurm

set -euo pipefail

echo "=== FungiMap Stage 2: Protein Clustering and ML ==="
echo "Started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURM_NODELIST}"

# Load required modules
module load conda/latest
module load mmseqs2/13-45111
module load diamond/2.0.15

# Activate conda environment
source activate fungimap-prod

# Set up directories
mkdir -p logs results/stage2 data/protein_clusters models

# Run Stage 2 pipeline
echo "Running protein clustering and ML training..."
snakemake \
    --cores ${SLURM_NTASKS} \
    --resources mem_mb=240000 \
    --config stage=2 \
    --until stage2_complete \
    --printshellcmds \
    --reason

echo "=== Stage 2 Complete ==="
echo "Completed: $(date)"
echo "Output: results/stage2/"
echo "Models: models/"
echo "Next: Validate model performance before Stage 3"
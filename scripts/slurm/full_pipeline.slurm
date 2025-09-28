#!/bin/bash
#SBATCH --job-name=fungimap-full
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=64G
#SBATCH --time=8:00:00
#SBATCH --partition=compute
#SBATCH --output=logs/fungimap-full-%j.out
#SBATCH --error=logs/fungimap-full-%j.err

# FungiMap Full Pipeline: End-to-end processing with pre-trained models
# Resources: 8 cores, 64GB RAM, 8 hours
# Estimated cost: $20-30 on cloud (c5.2xlarge equivalent)
# One-line runner: sbatch scripts/slurm/full_pipeline.slurm

set -euo pipefail

echo "=== FungiMap Full Pipeline ==="
echo "Started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURM_NODELIST}"

# Load required modules
module load conda/latest

# Activate conda environment
source activate fungimap-prod

# Set up directories
mkdir -p logs results/full_pipeline

# Run full pipeline with pre-trained models
echo "Running full FungiMap pipeline..."
snakemake \
    --cores ${SLURM_NTASKS} \
    --resources mem_mb=60000 \
    --config use_pretrained=true \
    --until pipeline_complete \
    --printshellcmds \
    --reason

echo "=== Full Pipeline Complete ==="
echo "Completed: $(date)"
echo "Output: results/full_pipeline/"
echo "Reports: results/full_pipeline/fungimap_report.html"

# Generate summary
echo "Generating pipeline summary..."
python scripts/generate_summary.py \
    --input results/full_pipeline \
    --output results/full_pipeline/summary.json

echo "Pipeline Summary: results/full_pipeline/summary.json"
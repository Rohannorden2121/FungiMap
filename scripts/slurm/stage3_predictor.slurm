#!/bin/bash
#SBATCH --job-name=fungimap-stage3
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=512G
#SBATCH --time=48:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:4
#SBATCH --output=logs/fungimap-stage3-%j.out
#SBATCH --error=logs/fungimap-stage3-%j.err

# FungiMap Stage 3: Deep Learning Predictor Training
# Resources: 32 cores, 512GB RAM, 4x GPUs, 48 hours
# Estimated cost: $800-1200 on cloud (p3.8xlarge equivalent)
# One-line runner: sbatch scripts/slurm/stage3_predictor.slurm

set -euo pipefail

echo "=== FungiMap Stage 3: Deep Learning Predictor ==="
echo "Started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURM_NODELIST}"
echo "GPUs: ${CUDA_VISIBLE_DEVICES:-all}"

# Load required modules
module load conda/latest
module load cuda/11.8
module load pytorch/1.13.1

# Activate conda environment
source activate fungimap-prod

# Verify GPU availability
nvidia-smi

# Set up directories
mkdir -p logs results/stage3 models/fungimap-predictor

# Run Stage 3 pipeline
echo "Running deep learning predictor training..."
snakemake \
    --cores ${SLURM_NTASKS} \
    --resources mem_mb=480000 gpu=4 \
    --config stage=3 gpu_enabled=true \
    --until stage3_complete \
    --printshellcmds \
    --reason

echo "=== Stage 3 Complete ==="
echo "Completed: $(date)"
echo "Output: results/stage3/"
echo "Models: models/fungimap-predictor/"
echo "Next: Validate predictor performance and prepare deployment"
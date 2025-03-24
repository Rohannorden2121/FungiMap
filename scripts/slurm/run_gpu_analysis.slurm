#!/bin/bash
#SBATCH --job-name=mycograph-xl-gpu
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --gres=gpu:a100:1
#SBATCH --time=24:00:00
#SBATCH --output=logs/gpu_analysis_%j.out
#SBATCH --error=logs/gpu_analysis_%j.err

# MycoGraph-XL GPU-Accelerated Analysis
# Optimized for structure prediction and embedding generation
# Cost Estimate: ~$50-100 on cloud GPU instances

set -euo pipefail

echo "Starting GPU-accelerated MycoGraph-XL analysis"
echo "Job ID: ${SLURM_JOB_ID:-local}"
echo "GPU: $CUDA_VISIBLE_DEVICES"
echo "Start Time: $(date)"

# Load GPU modules
module load cuda/11.8
module load anaconda3/2023.03
source activate mycograph-xl-gpu

# Set GPU memory management
export CUDA_VISIBLE_DEVICES=${SLURM_LOCALID:-0}
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Stage 1: Protein Structure Prediction with ColabFold
echo "=== GPU Stage 1: Structure Prediction ==="
start_time=$(date +%s)

# Use pre-computed representative proteins
colabfold_batch results/protein_clusters/representatives.faa \
                results/models/colabfold_gpu/ \
                --num-models 5 \
                --num-recycle 3 \
                --use-gpu-relax \
                --amber \
                --templates

end_time=$(date +%s)
echo "Structure prediction completed in $((end_time - start_time)) seconds"

# Stage 2: Large Language Model Embeddings
echo "=== GPU Stage 2: Protein Embeddings ==="
start_time=$(date +%s)

# Generate embeddings with ESM-2 large model
python scripts/generate_embeddings_gpu.py \
       results/protein_clusters/representatives.faa \
       results/embeddings/esm2_large/ \
       --model-name facebook/esm2_t36_3B_UR50D \
       --batch-size 8 \
       --max-tokens 4096 \
       --device cuda:0

end_time=$(date +%s)
echo "Embedding generation completed in $((end_time - start_time)) seconds"

# Stage 3: Advanced Analysis with GPU Acceleration
echo "=== GPU Stage 3: Advanced Analysis ==="
start_time=$(date +%s)

# Protein family clustering with GPU-accelerated similarity
python scripts/gpu_protein_clustering.py \
       results/embeddings/esm2_large/ \
       results/analysis/gpu_clusters/ \
       --similarity-threshold 0.8 \
       --use-gpu

# Phylogenetic analysis with GPU-accelerated tree building
python scripts/gpu_phylogenetic_analysis.py \
       results/protein_clusters/representatives.faa \
       results/analysis/phylogeny/ \
       --bootstrap-replicates 1000 \
       --use-gpu

end_time=$(date +%s)
echo "Advanced analysis completed in $((end_time - start_time)) seconds"

echo "=== GPU Pipeline Completed ==="
echo "Results saved to results/models/ and results/analysis/"
echo "End time: $(date)"
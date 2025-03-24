#!/bin/bash
# HPC Deployment Script - Production Scale Launch
# Based on approved HPC_CLOUD_PLAN.md

set -euo pipefail

echo "🚀 MycoGraph-XL Production Deployment Starting..."
echo "Timestamp: $(date)"

# Environment setup
export SNAKEMAKE_PROFILE="profiles/hpc"
export CONDA_ENV="mycograph-xl"

# Validate HPC environment
echo "📋 Validating HPC environment..."
if ! command -v sbatch &> /dev/null; then
    echo "❌ ERROR: SLURM not available. This script requires HPC with SLURM."
    exit 1
fi

if ! command -v mamba &> /dev/null; then
    echo "⚠️  WARNING: mamba not found, using conda"
    export CONDA_FRONTEND="conda"
fi

# Create necessary directories
echo "📂 Creating HPC directory structure..."
mkdir -p logs/cluster
mkdir -p results/assemblies
mkdir -p results/gene_predictions
mkdir -p results/protein_clusters
mkdir -p results/embeddings
mkdir -p results/models

# Activate conda environment
echo "🐍 Activating conda environment..."
conda activate $CONDA_ENV

# Production sample configuration
SAMPLE_COUNT=${1:-50}  # Default to 50 samples
STAGE=${2:-"all"}      # Default to all stages

echo "🎯 Configuration:"
echo "  - Samples to process: $SAMPLE_COUNT"
echo "  - Pipeline stage: $STAGE"
echo "  - HPC profile: $SNAKEMAKE_PROFILE"

# Launch production pipeline
echo "🚀 Launching production pipeline..."

case $STAGE in
    "stage0"|"validation")
        echo "Running Stage 0: Validation and QC"
        snakemake --profile $SNAKEMAKE_PROFILE \
                  stage0_validation \
                  --config max_samples=$SAMPLE_COUNT \
                  --rerun-incomplete
        ;;
    "stage1"|"assembly")
        echo "Running Stage 1: Assembly"
        snakemake --profile $SNAKEMAKE_PROFILE \
                  stage1_assembly \
                  --config max_samples=$SAMPLE_COUNT \
                  --rerun-incomplete
        ;;
    "stage2"|"annotation")
        echo "Running Stage 2: Gene Prediction"
        snakemake --profile $SNAKEMAKE_PROFILE \
                  stage2_annotation \
                  --config max_samples=$SAMPLE_COUNT \
                  --rerun-incomplete
        ;;
    "stage3"|"ml")
        echo "Running Stage 3: ML Analysis"
        snakemake --profile $SNAKEMAKE_PROFILE \
                  stage3_ml \
                  --config max_samples=$SAMPLE_COUNT \
                  --rerun-incomplete
        ;;
    "all")
        echo "Running ALL stages sequentially"
        snakemake --profile $SNAKEMAKE_PROFILE \
                  all_stages \
                  --config max_samples=$SAMPLE_COUNT \
                  --rerun-incomplete
        ;;
    *)
        echo "❌ Unknown stage: $STAGE"
        echo "Available stages: stage0, stage1, stage2, stage3, all"
        exit 1
        ;;
esac

echo "✅ Production deployment launched successfully!"
echo "📊 Monitor progress with: squeue -u $USER"
echo "📁 Results will be in: results/"
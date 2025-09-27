#!/bin/bash
#SBATCH --job-name=mycograph-xl-production
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=48:00:00
#SBATCH --output=logs/mycograph_%j.out
#SBATCH --error=logs/mycograph_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=user@institution.edu

# MycoGraph-XL Production Pipeline
# Estimated Resources: 32 cores, 128GB RAM, 48 hours
# Cost Estimate: ~$150-250 on AWS/GCP for full run

set -euo pipefail

# Job configuration
export SLURM_JOB_ID=${SLURM_JOB_ID:-"local"}
export PIPELINE_START_TIME=$(date +%s)

# Resource monitoring
echo "Starting MycoGraph-XL Production Pipeline"
echo "Job ID: $SLURM_JOB_ID"
echo "Allocated CPUs: $SLURM_CPUS_PER_TASK"
echo "Allocated Memory: ${SLURM_MEM_PER_NODE}MB"
echo "Start Time: $(date)"

# Load modules (adjust for your HPC environment)
module load anaconda3/2023.03
module load sra-toolkit/3.0.7
module load kraken2/2.1.2
module load bracken/2.8
module load spades/3.15.5
module load megahit/1.2.9
module load alphafold/2.3.2
module load colabfold/1.5.2

# Activate conda environment
source activate mycograph-xl

# Set resource limits
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MALLOC_ARENA_MAX=8

# Pipeline directories
export WORK_DIR="/scratch/$SLURM_JOB_ID/mycograph-xl"
export OUTPUT_DIR="/projects/mycology/results/run_$SLURM_JOB_ID"
export LOG_DIR="$OUTPUT_DIR/logs"

mkdir -p $WORK_DIR $OUTPUT_DIR $LOG_DIR

# Copy pipeline to scratch
cp -r $SLURM_SUBMIT_DIR/* $WORK_DIR/
cd $WORK_DIR

echo "Working directory: $WORK_DIR"
echo "Output directory: $OUTPUT_DIR"

# Stage 1: Data Download and QC (4-8 hours)
echo "=== Stage 1: Data Download and Quality Control ==="
seff_start=$(date +%s)

# Process sample manifest
while IFS=',' read -r sample_id accession; do
    if [[ "$sample_id" != "sample_id" ]]; then
        echo "Processing sample: $sample_id ($accession)"
        
        # Download SRA data
        prefetch $accession --output-directory data/sra-cache/
        fasterq-dump data/sra-cache/$accession --outdir data/sra-cache/ --threads 8
        gzip data/sra-cache/${accession}.fastq
        
        # Quality control
        fastqc data/sra-cache/${accession}.fastq.gz --outdir results/eda/fastqc/ --threads 4
        
        # Optional: fastp trimming for low-quality samples
        fastp -i data/sra-cache/${accession}.fastq.gz \
              -o data/sra-cache/${accession}_trimmed.fastq.gz \
              --thread 4 --html results/eda/fastp/${accession}_fastp.html
    fi
done < workflow/manifest.csv

# Aggregate QC reports
multiqc results/eda/fastqc/ results/eda/fastp/ --outdir results/eda/ --filename multiqc_production_report

seff_end=$(date +%s)
echo "Stage 1 completed in $((seff_end - seff_start)) seconds"

# Stage 2: Taxonomic Classification (6-12 hours)
echo "=== Stage 2: Taxonomic Classification ==="
seff_start=$(date +%s)

# Kraken2 classification with full database
for fastq in data/sra-cache/*.fastq.gz; do
    sample=$(basename $fastq .fastq.gz)
    echo "Classifying $sample with Kraken2"
    
    kraken2 --db data/kraken2-db/standard \
            --threads $SLURM_CPUS_PER_TASK \
            --report results/eda/kraken2/${sample}_report.txt \
            --output results/eda/kraken2/${sample}_output.txt \
            $fastq
    
    # Bracken abundance estimation
    bracken -d data/kraken2-db/standard \
            -i results/eda/kraken2/${sample}_report.txt \
            -o results/eda/bracken/${sample}_bracken.txt \
            -w results/eda/bracken/${sample}_bracken_report.txt \
            -r 150 -l S -t 10
done

seff_end=$(date +%s)
echo "Stage 2 completed in $((seff_end - seff_start)) seconds"

# Stage 3: Genome Assembly (12-24 hours)
echo "=== Stage 3: Genome Assembly ==="
seff_start=$(date +%s)

# metaSPAdes assembly for high-coverage samples
for fastq in data/sra-cache/*_trimmed.fastq.gz; do
    sample=$(basename $fastq _trimmed.fastq.gz)
    coverage=$(grep -m1 "$sample" results/eda/read_stats.txt | awk '{print $3}')
    
    if (( $(echo "$coverage > 10" | bc -l) )); then
        echo "Assembling $sample with metaSPAdes (coverage: $coverage)"
        spades.py --meta \
                  -s $fastq \
                  -o results/assemblies/${sample}_spades \
                  --threads $SLURM_CPUS_PER_TASK \
                  --memory $(($SLURM_MEM_PER_NODE / 1024))
    else
        echo "Assembling $sample with MEGAHIT (low coverage: $coverage)"
        megahit -r $fastq \
                -o results/assemblies/${sample}_megahit \
                --num-cpu-threads $SLURM_CPUS_PER_TASK \
                --memory 0.8
    fi
done

seff_end=$(date +%s)
echo "Stage 3 completed in $((seff_end - seff_start)) seconds"

# Stage 4: Gene Prediction and Functional Analysis (8-16 hours)
echo "=== Stage 4: Gene Prediction and Functional Analysis ==="
seff_start=$(date +%s)

# Gene prediction with Prodigal
for assembly_dir in results/assemblies/*/; do
    sample=$(basename $assembly_dir)
    assembly_file=$(find $assembly_dir -name "*.fasta" -o -name "contigs.fa" | head -1)
    
    if [[ -f "$assembly_file" ]]; then
        echo "Predicting genes for $sample"
        prodigal -i $assembly_file \
                 -o results/gene_predictions/${sample}_genes.gbk \
                 -a results/gene_predictions/${sample}_proteins.faa \
                 -d results/gene_predictions/${sample}_genes.fna \
                 -p meta
    fi
done

# Protein clustering with CD-HIT
cat results/gene_predictions/*_proteins.faa > results/protein_clusters/all_proteins.faa
cd-hit -i results/protein_clusters/all_proteins.faa \
       -o results/protein_clusters/clustered_proteins.faa \
       -c 0.95 -n 5 -T $SLURM_CPUS_PER_TASK -M $(($SLURM_MEM_PER_NODE * 800))

seff_end=$(date +%s)
echo "Stage 4 completed in $((seff_end - seff_start)) seconds"

# Stage 5: Structure Prediction (12-36 hours - most resource intensive)
echo "=== Stage 5: Structure Prediction ==="
seff_start=$(date +%s)

# ColabFold batch prediction for representative proteins
python scripts/select_representative_proteins.py \
       results/protein_clusters/clustered_proteins.faa \
       results/protein_clusters/representatives.faa \
       --max-proteins 1000

# Run ColabFold (requires GPU nodes for optimal performance)
colabfold_batch results/protein_clusters/representatives.faa \
                results/models/colabfold/ \
                --num-models 5 \
                --num-recycle 3 \
                --num-relax 1

seff_end=$(date +%s)
echo "Stage 5 completed in $((seff_end - seff_start)) seconds"

# Stage 6: Embedding Generation and Analysis (4-8 hours)
echo "=== Stage 6: Embedding Generation and Analysis ==="
seff_start=$(date +%s)

# Generate protein embeddings with ESM-2
python scripts/generate_embeddings.py \
       results/protein_clusters/representatives.faa \
       results/embeddings/ \
       --model-name facebook/esm2_t33_650M_UR50D \
       --batch-size 32 \
       --device cuda

# Analyze taxonomic patterns
python scripts/analyze_taxonomic_patterns.py \
       results/eda/kraken2/ \
       results/eda/bracken/ \
       results/embeddings/ \
       results/analysis/

seff_end=$(date +%s)
echo "Stage 6 completed in $((seff_end - seff_start)) seconds"

# Final cleanup and archival preparation
echo "=== Pipeline Cleanup and Archival ==="
pipeline_end_time=$(date +%s)
total_runtime=$((pipeline_end_time - PIPELINE_START_TIME))

# Copy results to permanent storage
rsync -av results/ $OUTPUT_DIR/
rsync -av logs/ $OUTPUT_DIR/logs/

# Generate final report
python scripts/generate_final_report.py \
       $OUTPUT_DIR \
       --job-id $SLURM_JOB_ID \
       --runtime $total_runtime \
       --output $OUTPUT_DIR/final_report.html

# Cleanup scratch directory
rm -rf $WORK_DIR

echo "=== Pipeline Completed Successfully ==="
echo "Total runtime: $total_runtime seconds ($(($total_runtime / 3600)) hours)"
echo "Results saved to: $OUTPUT_DIR"
echo "End time: $(date)"

# Resource usage summary
seff $SLURM_JOB_ID > $OUTPUT_DIR/resource_usage_summary.txt 2>&1
# FungiMap Quick Start Guide

**Lightweight fungal metagenomics pipeline for quality control and taxonomic profiling**

## 🚀 Quick Demo (5 minutes)

### Prerequisites
- MacOS/Linux with 8GB+ RAM
- Conda/Mamba installed
- 2GB free disk space

### One-Line Demo
```bash
# Clone and run demo
git clone https://github.com/username/mycograph-xl.git
cd mycograph-xl
conda env create -f environment.yml
conda activate mycograph-xl
snakemake --cores 2 demo_pipeline
```

### Expected Outputs
- `results/demo/multiqc_report.html` - Quality control summary
- `results/demo/eda_summary.csv` - Sample statistics
- `results/demo/eda_report.txt` - Analysis report
- `results/demo/kraken2/` - Taxonomic classifications

### Demo Dataset
- 2 samples (SRR13059548, SRR15377549)
- 500k reads each (~100MB total)
- Fungal-enriched sequences

## 📋 Full Pipeline Capabilities

### Stage 0: Quality Control & Validation ✅ (Demo Included)
- FastQC quality assessment
- Taxonomic profiling (Kraken2 + MiniKraken2)
- Sample validation and filtering
- MultiQC aggregated reporting

### Stage 1: Assembly (HPC Required)
- MEGAHIT metagenomic assembly
- QUAST quality assessment
- Contamination screening

### Stage 2: Gene Prediction (HPC Required)  
- Prodigal gene calling
- HMMER functional annotation
- InterProScan domain analysis

### Stage 3: ML Analysis (GPU Required)
- ESM protein embeddings
- Hierarchical clustering
- Classification modeling

## 🖥️ System Requirements

### Local Demo (This Repo)
- **CPU:** 2-4 cores
- **Memory:** 4-8GB RAM
- **Disk:** 2GB free space
- **Time:** 5-15 minutes

### Production Scale (University HPC)
- **CPU:** 16-32 cores per job
- **Memory:** 32-128GB RAM
- **GPU:** Optional (Stage 3 only)
- **Time:** Hours to days
- **Cost:** $200-400 per 50 samples

## 📦 Installation

### Option 1: Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate mycograph-xl
```

### Option 2: Docker
```bash
docker build -t mycograph-xl .
docker run -v $(pwd):/workspace mycograph-xl snakemake demo_pipeline
```

## 🔬 Running Analysis

### Demo (Local)
```bash
# Quick demo with provided data
snakemake --cores 2 demo_pipeline

# Monitor progress
snakemake --cores 2 demo_pipeline --reason
```

### Custom Data (Local - Light Analysis Only)
```bash
# Edit config/demo_config.yaml with your sample IDs
snakemake --cores 2 stage0_validation --config samples="YOUR_SRR_ID"
```

### Production Scale (HPC)
```bash
# Submit to SLURM cluster (not run locally)
sbatch scripts/submit_production.sh
```

## 📊 Interpreting Results

### Quality Control
- **MultiQC Report:** `results/demo/multiqc_report.html`
  - Per-base quality scores
  - GC content distribution
  - Adapter contamination

### Taxonomic Profile
- **Kraken2 Reports:** `results/demo/kraken2/*.txt`
  - Species-level classifications
  - Abundance estimates
  - Confidence scores

### Sample Summary
- **EDA Summary:** `results/demo/eda_summary.csv`
  - Read counts, quality metrics
  - Taxonomic composition
  - Pass/fail validation status

## 🚨 Important Notes

### Local Limitations
This repository is designed for **demonstration and light analysis only**. Heavy computations including:
- Large-scale assemblies (MEGAHIT/metaSPAdes)
- Protein embeddings (ESM models)
- Full Bracken abundance estimation
- Database building

**Are intended for university HPC systems, not local machines.**

### Memory Usage
The demo is designed to stay under 4GB RAM usage. If you encounter memory issues:
```bash
# Reduce thread count
snakemake --cores 1 demo_pipeline

# Monitor memory usage
snakemake --cores 2 demo_pipeline --resources mem_mb=3000
```

## 🐛 Troubleshooting

### Common Issues
1. **Out of memory:** Reduce `--cores` to 1
2. **Missing database:** Demo uses MiniKraken2 (included)
3. **Slow download:** Pre-cached demo data included

### Getting Help
- Check logs in `logs/` directory
- Review `results/demo/eda_report.txt` for analysis summary
- Submit issues on GitHub

## 📚 Citation

If you use FungiMap in your research, please cite:
```
FungiMap: Scalable fungal metagenomics predictor
[DOI pending]
```

## 🤝 Contributing

1. Fork the repository
2. Run the demo to verify setup
3. Make changes to demo-compatible components only
4. Submit pull request

---

**⚡ Get started with the demo in under 5 minutes!**
# Data Setup Instructions

## Required Data Files

This predictor requires several large data files that are not included in the repository. Here's how to obtain and set up each component:

### 1. Kraken2 Database (Required)
We use the MiniKraken2 v2 8GB database (April 2019 version):
```bash
# Create database directory
mkdir -p data/kraken2-db
cd data/kraken2-db

# Download MiniKraken2 v2 8GB
wget https://ccb.jhu.edu/software/kraken2/dl/minikraken2_v2_8GB_201904.tgz

# Extract the database
tar xzf minikraken2_v2_8GB_201904.tgz
```

### 2. Sequence Data (Optional)
The analysis was performed on the following SRA accessions:
- SRR13059548 (Agricultural soil sample)
- SRR15377549 (Marine sediment sample)

To download these samples:
```bash
# Set up SRA cache directory
mkdir -p data/sra-cache

# Download using SRA toolkit
prefetch SRR13059548 SRR15377549 --output-directory data/sra-cache
fasterq-dump --outdir data/sra-cache --skip-technical --split-files SRR13059548 SRR15377549
```

### 3. Directory Structure
After setup, your data directory should look like this:
```
data/
├── kraken2-db/
│   └── minikraken2_v2_8GB_201904_UPDATE/
│       ├── database100mers.kmer_distrib
│       ├── database150mers.kmer_distrib
│       ├── database200mers.kmer_distrib
│       ├── hash.k2d
│       ├── opts.k2d
│       └── taxo.k2d
└── sra-cache/
    ├── SRR13059548.fastq.gz
    └── SRR15377549.fastq.gz
```

## Storage Requirements
- Kraken2 database: ~8GB (compressed), ~8GB (uncompressed)
- Sequence data: ~1GB total for both samples
- Total storage needed: ~20GB including working space

## Notes
- The Kraken2 database is updated periodically. While we use the April 2019 version for reproducibility, newer versions are available.
- Sequence data can be downloaded on-demand using the provided accession numbers.
- All data downloads and processing scripts will automatically create the necessary directories.
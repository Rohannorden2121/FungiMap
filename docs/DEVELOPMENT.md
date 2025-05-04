# FungiMap Development Guide

## Architecture Overview

FungiMap has Snakemake as the workflow management system.

## Directory

```
mycology-predictor/
├── workflow/                 # Snakemake workflow
│   ├── Snakefile            # Main workflow definition
│   ├── scripts/             # Pipeline scripts
│   ├── envs/               # Conda environments
│   └── config.yaml         # Workflow configuration
├── config/                 # Configuration files
│   ├── pipeline_config.json # Main pipeline settings
│   └── multiqc_config.yaml # MultiQC configuration
├── profiles/              # Execution profiles
│   ├── local/            # Local execution
│   └── cluster/          # Cluster execution
├── src/                  # Source code modules
├── tests/               # Unit tests
├── docs/               # Documentation
└── results/            # Pipeline outputs
```


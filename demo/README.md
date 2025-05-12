# FungiMap Demo

## Quick Start

Run the demo locally using precomputed results:

```bash
# 1. Set up demo environment
conda env create -f demo/environment-demo.yml && conda activate fungimap-demo

# 2. Launch demo notebook  
jupyter notebook demo/notebook.ipynb

# 3. View results summary (optional)
python demo/view_results.py
```

## Command Details

**Command 1:** Creates a conda environment with packages needed for the demo (pandas, matplotlib, jupyter). No bioinformatics tools or databases required.

**Command 2:** Opens the demo notebook in Jupyter. The notebook contains precomputed outputs and displays results without executing computations.

**Command 3:** (Optional) Prints demo results to the terminal for quick viewing without Jupyter.

## What You'll See

- Complete analysis workflow
- Species classification
- Performance metrics/QC stats  
- Basic interpretations of findings
- 

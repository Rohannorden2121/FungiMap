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

**Command 1:** Creates conda environment with packages needed for demo (pandas, matplotlib, jupyter). No bioinformatics tools or databases are needed for this.

**Command 2:** Opens the demo notebook in Jupyter. The notebook has precomputed outputs and displays results w/out doing any computations.

**Command 3:** (Optional) Prints demo results to terminal for quick viewing without needing Jupyter.

## What You'll See

- Analysis workflow
- Species classification
- Performance metrics/QC stats  
- Basic findings explanations

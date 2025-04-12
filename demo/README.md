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

## System Requirements

- **Memory:** 1-2 GB RAM (demo data only)
- **Storage:** <100 MB (lightweight dependencies)
- **Time:** <3 minutes to set up environment
- **Internet:** Required for initial conda package downloads

## What You'll See

- Complete analysis workflow from input samples to final results
- Interactive visualizations showing species classification
- Performance metrics and quality control statistics  
- Plain-language interpretations of findings

## Notes

- ✅ **No GPU required** - demo uses precomputed outputs only
- ✅ **No large downloads** - all heavy databases are referenced, not included
- ✅ **Laptop friendly** - designed for standard development environments
- ✅ **Immediate results** - all outputs embedded in notebook for instant viewing

---

**Alternative:** If you prefer not to install anything, the notebook renders directly on GitHub with all outputs visible.
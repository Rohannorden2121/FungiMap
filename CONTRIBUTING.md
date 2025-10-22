# Contributing to FungiMap

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and test them
4. Commit with messages: `git commit -m "feat: add new feature"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a pull request
   
## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/mycology-project.git
cd mycology-project

# Create development environment
conda env create -f environment.yml
conda activate mycograph-xl-demo

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run demo to verify setup
python scripts/create_demo_data.py
bash src/run_eda_pipeline.sh
```

Thank you for helping make FungiMap better!

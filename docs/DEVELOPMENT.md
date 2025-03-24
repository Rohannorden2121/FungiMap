# FungiMap Development Guide

## Architecture Overview

FungiMap is built using Snakemake as the workflow management system, with modular components for different analysis stages.

## Directory Structure

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

## Core Components

### 1. Sample Validator (`workflow/scripts/sample_validator_fixed.py`)
- **Purpose**: Validates samples against quality criteria
- **Key Features**:
  - Metadata completeness assessment
  - Sequence quality analysis (FastQC integration)
  - Taxonomic composition analysis (Kraken2/Bracken)
  - Resource estimation
- **Configuration**: Uses `pipeline_config.json` for validation criteria

### 2. Workflow Definition (`workflow/Snakefile`)
- **Structure**: Modular rules organized by pipeline stages
- **Features**:
  - Conda environment management
  - Dynamic sample processing
  - Resource allocation
  - Error handling and logging

### 3. Environment Management (`workflow/envs/`)
- Separate conda environments for each pipeline stage
- Isolated dependencies to prevent conflicts
- Reproducible execution across systems

## Development Workflow

### 1. Setting Up Development Environment
```bash
# Clone repository
git clone <repository-url>
cd mycology-predictor

# Create development environment
conda env create -f environment.yml
conda activate mycograph-xl

# Install development dependencies
pip install -e .
pip install pytest pytest-asyncio black isort mypy
```

### 2. Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_validator.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 3. Code Quality
```bash
# Format code
black src/ workflow/scripts/
isort src/ workflow/scripts/

# Type checking
mypy src/

# Lint Snakemake workflow
snakemake --lint
```

## Adding New Components

### 1. Adding a New Pipeline Stage

1. **Create Rule in Snakefile**:
```python
rule new_analysis:
    input:
        "results/previous_stage/{sample}.txt"
    output:
        "results/new_stage/{sample}_analysis.txt"
    conda:
        "envs/new_analysis.yaml"
    log:
        "logs/new_analysis/{sample}.log"
    shell:
        "python workflow/scripts/new_analysis.py {input} {output}"
```

2. **Create Conda Environment** (`workflow/envs/new_analysis.yaml`):
```yaml
name: new_analysis
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.9
  - specific-tools=1.0
```

3. **Implement Script** (`workflow/scripts/new_analysis.py`):
```python
#!/usr/bin/env python3
import sys
import logging

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Implementation here
    
if __name__ == "__main__":
    main()
```

### 2. Adding New Validation Criteria

Extend the `SampleValidator` class:

```python
async def _new_validation_check(self, accession: str) -> Dict[str, float]:
    """Implement new validation logic"""
    metrics = {}
    
    # Add validation logic
    
    return metrics
```

Update validation in `validate_sample()` method to include new check.

### 3. Adding Configuration Options

1. **Update `config/pipeline_config.json`**:
```json
{
  "new_feature": {
    "parameter1": "value1",
    "parameter2": 42
  }
}
```

2. **Access in Scripts**:
```python
config = self._load_config(config_path)
param = config["new_feature"]["parameter1"]
```

## Testing Strategy

### 1. Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Use pytest fixtures for setup

### 2. Integration Tests
- Test complete workflows
- Use test data in `tests/data/`
- Validate pipeline outputs

### 3. Performance Tests
- Monitor resource usage
- Test with various data sizes
- Benchmark critical components

## Debugging

### 1. Snakemake Debugging
```bash
# Dry run to check workflow
snakemake -n

# Debug specific rule
snakemake --debug rule_name

# Keep temporary files
snakemake --notemp

# Detailed logging
snakemake --verbose
```

### 2. Component Debugging
```bash
# Enable debug logging in Python scripts
export PYTHONPATH=$PWD:$PYTHONPATH
python -m pdb workflow/scripts/sample_validator_fixed.py
```

### 3. Resource Monitoring
```bash
# Monitor during execution
python workflow/scripts/monitor.py &
snakemake --cores 4

# Check resource logs
cat logs/resource_usage.json
```

## Contributing Guidelines

### 1. Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings for all functions/classes
- Keep functions focused and testable

### 2. Commit Messages
```
feat: add new validation metric for read quality
fix: resolve memory leak in sequence processing
docs: update installation instructions
test: add unit tests for validator class
```

### 3. Pull Request Process
1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit PR with clear description

### 4. Release Process
1. Update version numbers
2. Update CHANGELOG.md
3. Create release tag
4. Update documentation

## Performance Considerations

### 1. Memory Usage
- Stream large files when possible
- Use generators for data processing
- Monitor memory usage with `psutil`

### 2. CPU Usage
- Leverage multiprocessing where appropriate
- Use efficient algorithms
- Profile CPU-intensive operations

### 3. I/O Optimization
- Minimize file operations
- Use compression for intermediate files
- Implement caching for expensive operations

## Deployment

### 1. Local Deployment
- Use conda environments
- Configure local profile
- Monitor resource usage

### 2. Cluster Deployment
- Configure cluster profile
- Set up job scheduling
- Handle distributed storage

### 3. Cloud Deployment
- Use container images
- Configure cloud storage
- Implement auto-scaling

## Troubleshooting Development Issues

### Common Problems

1. **Import Errors**
   - Check PYTHONPATH
   - Verify conda environment
   - Check for circular imports

2. **Snakemake Rule Errors**
   - Validate file paths
   - Check wildcard constraints
   - Verify input/output relationships

3. **Memory Issues**
   - Profile memory usage
   - Use streaming where possible
   - Optimize data structures

4. **Performance Issues**
   - Profile code execution
   - Optimize bottlenecks
   - Consider parallelization

## Future Development

### Planned Features
- Advanced taxonomic classification
- Machine learning integration
- Cloud-native execution
- Real-time monitoring dashboard

### Extension Points
- Plugin system for custom analyzers
- REST API for remote execution
- Integration with external databases
- Enhanced visualization capabilities
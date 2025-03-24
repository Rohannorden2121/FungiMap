#!/bin/bash
# MycoGraph-XL CI Smoke Test
# Tests basic pipeline functionality with minimal resources

set -euo pipefail

echo "=== MycoGraph-XL CI Smoke Test ==="
echo "Started: $(date)"

# Test 1: Environment validation
echo "Test 1: Environment validation..."
if conda env list | grep -q mycograph-xl; then
    echo "✅ Conda environment exists"
else
    echo "❌ Conda environment missing"
    exit 1
fi

# Test 2: Configuration validation
echo "Test 2: Configuration validation..."
if [[ -f "config/pipeline_config.json" ]]; then
    echo "✅ Pipeline configuration exists"
else
    echo "❌ Pipeline configuration missing"
    exit 1
fi

# Test 3: Snakemake dry run
echo "Test 3: Snakemake workflow validation..."
if conda run -n mycograph-xl snakemake -n --quiet stage0_validation --config samples="TEST001" > /dev/null 2>&1; then
    echo "✅ Snakemake workflow validates"
else
    echo "❌ Snakemake workflow validation failed"
    exit 1
fi

# Test 4: Validator script execution
echo "Test 4: Validator script test..."
if python workflow/scripts/sample_validator_fixed.py --help > /dev/null 2>&1; then
    echo "✅ Validator script functional"
else
    echo "❌ Validator script issues"
    exit 1
fi

# Test 5: Required directories
echo "Test 5: Directory structure..."
required_dirs=("workflow" "config" "profiles" "results" "data")
for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "✅ Directory $dir exists"
    else
        echo "❌ Directory $dir missing"
        exit 1
    fi
done

echo "=== All tests passed! ==="
echo "Completed: $(date)"
echo "Pipeline ready for execution"
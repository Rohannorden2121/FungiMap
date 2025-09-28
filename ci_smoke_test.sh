#!/bin/bash
# MycoGraph-XL CI Smoke Test
# Tests basic pipeline functionality with minimal resources

set -euo pipefail

echo "=== MycoGraph-XL CI Smoke Test ==="
echo "Started: $(date)"

# Test 1: Environment validation
echo "Test 1: Environment validation..."
if conda env list | grep -q fungimap-test; then
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
if conda run -n fungimap-test snakemake -n stage0_validation 2>&1 | grep -q "This was a dry-run"; then
    echo "✅ Snakemake workflow validates"
else
    echo "❌ Snakemake workflow validation failed"
    exit 1
fi

# Test 4: Demo data generation
echo "Test 4: Demo data generation test..."
if python scripts/create_demo_data.py > /dev/null 2>&1; then
    echo "✅ Demo data generation works"
else
    echo "❌ Demo data generation failed"
    exit 1
fi

# Test 5: Required directories
echo "Test 5: Directory structure..."
required_dirs=("workflow" "config" "results" "data")
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
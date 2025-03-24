#!/bin/bash
set -euo pipefail

# Enhanced EDA Pipeline Script for MycoGraph-XL
# Author: MycoGraph-XL Team
# Version: 1.1.0

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly DATA_DIR="${PROJECT_ROOT}/data"
readonly RESULTS_DIR="${PROJECT_ROOT}/results/eda"
readonly KRAKEN_DB="${DATA_DIR}/kraken2-db/minikraken2_v2_8GB_201904_UPDATE"
readonly MAX_SPOTS=500000
readonly THREADS=6
readonly CONDA_ENV="mycology-xl"

# Logging configuration
readonly LOG_FILE="${RESULTS_DIR}/pipeline.log"
readonly ERROR_LOG="${RESULTS_DIR}/pipeline.error.log"
mkdir -p "$(dirname "${LOG_FILE}")"

# Logging function
log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $*" | tee -a "${LOG_FILE}"
}

# Error handling
error() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] ERROR: $*" | tee -a "${ERROR_LOG}"
    exit 1
}

# Function to activate conda environment
setup_environment() {
    log "Setting up conda environment..."
    
    # Initialize conda
    if ! eval "$(conda shell.bash hook)"; then
        error "Failed to initialize conda"
    fi
    
    # Activate environment
    if ! conda activate "${CONDA_ENV}"; then
        error "Failed to activate conda environment: ${CONDA_ENV}"
    fi
    
    log "Conda environment activated: ${CONDA_ENV}"
}

# Function to check required tools
check_dependencies() {
    local missing_tools=()
    
    for tool in fastq-dump fastqc kraken2 bracken multiqc python; do
        if ! command -v "${tool}" &> /dev/null; then
            missing_tools+=("${tool}")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        error "Missing required tools: ${missing_tools[*]}"
    fi
    
    log "All required tools are available"
}

# Function to validate database
validate_kraken_db() {
    if [[ ! -d "${KRAKEN_DB}" ]]; then
        error "Kraken2 database not found at ${KRAKEN_DB}"
    fi
    
    local required_files=("hash.k2d" "opts.k2d" "taxo.k2d")
    for file in "${required_files[@]}"; do
        if [[ ! -f "${KRAKEN_DB}/${file}" ]]; then
            error "Missing required database file: ${file}"
        fi
    done
    
    log "Kraken2 database validated"
}

# Function to initialize results directory
initialize_results_dir() {
    log "Initializing results directory structure..."
    
    local dirs=(
        "${RESULTS_DIR}/fastqc"
        "${RESULTS_DIR}/kraken2"
        "${RESULTS_DIR}/bracken"
        "${RESULTS_DIR}/multiqc"
        "${RESULTS_DIR}/plots"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "${dir}"
    done
    
    log "Results directory structure initialized"
}

# Function to process a single sample
process_sample() {
    local accession="$1"
    local output_dir="${RESULTS_DIR}"
    
    log "Processing sample: ${accession}"
    
    if ! "${SCRIPT_DIR}/process_sample.sh" "${accession}"; then
        error "Failed to process sample: ${accession}"
    fi
}

# Function to run MultiQC
run_multiqc() {
    log "Running MultiQC analysis..."
    
    if ! multiqc "${RESULTS_DIR}/fastqc" \
                 "${RESULTS_DIR}/kraken2" \
                 -f -o "${RESULTS_DIR}/multiqc" \
                 -n "multiqc_report.html"; then
        error "MultiQC analysis failed"
    fi
    
    log "MultiQC analysis complete"
}

# Function to generate final reports
generate_reports() {
    log "Generating final reports..."
    
    # Run Python analysis script
    if ! python "${SCRIPT_DIR}/analyze_eda_results.py"; then
        error "Failed to generate analysis reports"
    fi
    
    log "Report generation complete"
}

# Main execution
main() {
    log "=== Starting MycoGraph-XL EDA Pipeline ==="
    
    # Setup environment
    setup_environment
    
    # Check dependencies
    check_dependencies
    
    # Validate database
    validate_kraken_db
    
    # Initialize results directory
    initialize_results_dir
    
    # Process each sample from manifest
    while IFS=, read -r accession biome source size url checksum; do
        if [[ "${accession}" != "accession" ]]; then  # Skip header
            process_sample "${accession}"
        fi
    done < "${RESULTS_DIR}/manifest.csv"
    
    # Run MultiQC
    run_multiqc
    
    # Generate reports
    generate_reports
    
    log "=== Pipeline completed successfully ==="
    log "Results available in: ${RESULTS_DIR}"
    log "MultiQC report: ${RESULTS_DIR}/multiqc/multiqc_report.html"
}

# Execute main function
main "$@"
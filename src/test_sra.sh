#!/bin/bash
set -euo pipefail

# Enhanced SRA Toolkit Test Script
# Author: MycoGraph-XL Team
# Version: 1.1.0

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly TEST_ACC="ERR2036629"  # Small fungal metagenome sample
readonly OUTDIR="${PROJECT_ROOT}/data/sra-cache"
readonly LOG_FILE="${OUTDIR}/test_sra.log"

# Logging setup
mkdir -p "${OUTDIR}"

# Logging function
log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $*" | tee -a "${LOG_FILE}"
}

# Error handling
error() {
    log "ERROR: $*"
    exit 1
}

# Function to check SRA toolkit installation
check_sra_toolkit() {
    log "Checking SRA toolkit installation..."
    
    if ! command -v fasterq-dump &> /dev/null; then
        error "fasterq-dump not found. Please install SRA toolkit"
    fi
    
    if ! command -v vdb-config &> /dev/null; then
        error "vdb-config not found. Please install SRA toolkit"
    fi
    
    log "SRA toolkit installation verified"
}

# Function to validate output directory
validate_outdir() {
    log "Validating output directory..."
    
    if [[ ! -d "${OUTDIR}" ]]; then
        mkdir -p "${OUTDIR}"
    fi
    
    if [[ ! -w "${OUTDIR}" ]]; then
        error "Output directory is not writable: ${OUTDIR}"
    fi
    
    log "Output directory validated"
}

# Function to test download
test_download() {
    log "Testing SRA toolkit with ${TEST_ACC}..."
    
    # Clean up any previous test files
    rm -f "${OUTDIR}/${TEST_ACC}"*
    
    # Try download with progressbar
    if ! fasterq-dump --split-spot \
                      --split-files \
                      --skip-technical \
                      --threads 6 \
                      --progress \
                      --outdir "${OUTDIR}" \
                      --maxspots 500000 \
                      "${TEST_ACC}"; then
        error "Failed to download test accession"
    fi
    
    # Verify downloaded files
    if ! ls "${OUTDIR}/${TEST_ACC}"* &> /dev/null; then
        error "No output files found"
    fi
    
    log "Download test successful"
}

# Function to validate downloaded files
validate_files() {
    log "Validating downloaded files..."
    
    local files=("${OUTDIR}/${TEST_ACC}"*)
    
    for file in "${files[@]}"; do
        if [[ ! -s "${file}" ]]; then
            error "Empty or missing file: ${file}"
        fi
        
        # Check if file is valid FASTQ
        if zcat < "${file}" | head -n 4 | grep -q "^@.*"; then
            log "Validated FASTQ file: ${file}"
        else
            error "Invalid FASTQ format: ${file}"
        fi
    done
    
    log "File validation complete"
}

# Function to clean up
cleanup() {
    log "Cleaning up test files..."
    rm -f "${OUTDIR}/${TEST_ACC}"*
    log "Cleanup complete"
}

# Main execution
main() {
    log "=== Starting SRA toolkit test ==="
    
    # Check SRA toolkit installation
    check_sra_toolkit
    
    # Validate output directory
    validate_outdir
    
    # Run download test
    test_download
    
    # Validate downloaded files
    validate_files
    
    # Clean up
    cleanup
    
    log "=== All tests completed successfully ==="
}

# Execute main function
main "$@"
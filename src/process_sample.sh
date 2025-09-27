#!/bin/bash
set -euo pipefail

# Enhanced sample processing script with improved error handling and logging
# Author: MycoGraph-XL Team
# Version: 1.1.0

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly CACHE_DIR="${PROJECT_ROOT}/data/sra-cache"
readonly RESULTS_DIR="${PROJECT_ROOT}/results/eda"
readonly KRAKEN_DB="${PROJECT_ROOT}/data/kraken2-db/minikraken2_v2_8GB_201904_UPDATE"
readonly MAX_SPOTS=500000
readonly THREADS=6

# Logging configuration
readonly LOG_FILE="${RESULTS_DIR}/pipeline.log"
mkdir -p "$(dirname "${LOG_FILE}")"

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

# Function to check required tools
check_dependencies() {
    local missing_tools=()
    
    for tool in fastq-dump fastqc kraken2 bracken; do
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

# Function to download from ENA
download_from_ena() {
    local accession="$1"
    local output_file="${CACHE_DIR}/${accession}.fastq.gz"
    
    log "Downloading ${accession}..."
    
    # Get download URL from ENA API
    local url
    url=$(curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=${accession}&result=read_run&fields=fastq_ftp&format=tsv" | tail -n1 | cut -f2)
    
    if [[ -z "${url}" ]]; then
        error "Could not get download URL for ${accession}"
    fi
    
    # Download with retry logic
    local max_retries=3
    local retry_count=0
    
    while [[ ${retry_count} -lt ${max_retries} ]]; do
        if wget --quiet --tries=3 --timeout=60 "ftp://${url}" -O "${output_file}"; then
            if [[ -s "${output_file}" ]]; then
                log "Download successful: ${output_file}"
                return 0
            fi
        fi
        
        log "Retry ${retry_count} of ${max_retries}..."
        ((retry_count++))
        sleep 5
    done
    
    error "Download failed for ${accession} after ${max_retries} attempts"
}

# Function to run FastQC
run_fastqc() {
    local input_file="$1"
    local output_dir="${RESULTS_DIR}/fastqc"
    mkdir -p "${output_dir}"
    
    log "Running FastQC on ${input_file}..."
    if ! fastqc -o "${output_dir}" -t "${THREADS}" "${input_file}"; then
        error "FastQC failed for ${input_file}"
    fi
    
    log "FastQC analysis complete"
}

# Function to run Kraken2 and Bracken
run_taxonomic_profiling() {
    local input_file="$1"
    local output_prefix="$2"
    
    log "Running Kraken2 analysis..."
    if ! kraken2 --db "${KRAKEN_DB}" \
                 --threads "${THREADS}" \
                 --confidence 0.05 \
                 --report "${output_prefix}_report.txt" \
                 --output "${output_prefix}_output.txt" \
                 "${input_file}"; then
        error "Kraken2 analysis failed for ${input_file}"
    fi
    
    log "Running Bracken abundance estimation..."
    if ! bracken -d "${KRAKEN_DB}" \
                 -i "${output_prefix}_report.txt" \
                 -o "${output_prefix}_bracken.txt" \
                 -w "${output_prefix}_bracken.report" \
                 -r 150 -l S; then
        error "Bracken analysis failed for ${input_file}"
    fi
    
    log "Taxonomic profiling complete"
}

# Function to calculate basic statistics
calculate_stats() {
    local input_file="$1"
    local output_file="${RESULTS_DIR}/read_stats.txt"
    
    log "Calculating read statistics..."
    
    # Get basic stats using zcat and awk
    local total_reads
    total_reads=$(zcat < "${input_file}" | awk 'END{print NR/4}')
    
    local avg_length
    avg_length=$(zcat < "${input_file}" | awk 'NR%4==2{sum+=length($0); count++}END{print sum/count}')
    
    # Append to stats file
    printf "%s\t%d\t%.1f\n" "$(basename "${input_file}")" "${total_reads}" "${avg_length}" >> "${output_file}"
    
    log "Statistics calculated and saved"
}

# Main processing function
process_sample() {
    local accession="$1"
    local fastq_path="${CACHE_DIR}/${accession}.fastq.gz"
    local output_prefix="${RESULTS_DIR}/kraken2/${accession}"
    
    mkdir -p "${CACHE_DIR}" "${RESULTS_DIR}/kraken2"
    
    log "Processing ${accession}..."
    
    # Download data
    download_from_ena "${accession}"
    
    # Run QC
    run_fastqc "${fastq_path}"
    
    # Run taxonomic profiling
    run_taxonomic_profiling "${fastq_path}" "${output_prefix}"
    
    # Calculate statistics
    calculate_stats "${fastq_path}"
    
    log "Sample ${accession} processing complete"
}

# Main execution
main() {
    if [[ $# -ne 1 ]]; then
        error "Usage: $0 <accession>"
    fi
    
    local accession="$1"
    
    log "=== Starting sample processing pipeline ==="
    log "Project root: ${PROJECT_ROOT}"
    log "Sample: ${accession}"
    
    # Check dependencies
    check_dependencies
    
    # Validate database
    validate_kraken_db
    
    # Process sample
    process_sample "${accession}"
    
    log "=== Pipeline completed successfully ==="
}

# Execute main function
main "$@"
# Dockerfile for MycoGraph-XL Demo
# Lightweight container for demonstration and CI testing

FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /workspace

# Copy environment file
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml && \
    conda clean -a -y && \
    rm -rf /opt/conda/pkgs/*

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "mycograph-xl-demo", "/bin/bash", "-c"]

# Copy source code
COPY . .

# Create results directory
RUN mkdir -p results/demo logs

# Set environment variables for resource limits
ENV MALLOC_ARENA_MAX=2
ENV OMP_NUM_THREADS=2
ENV OPENBLAS_NUM_THREADS=2

# Default command runs demo pipeline
CMD ["conda", "run", "-n", "mycograph-xl-demo", "snakemake", "--cores", "2", "demo_pipeline"]

# Metadata
LABEL maintainer="MycoGraph-XL Team"
LABEL version="0.1.0-demo"
LABEL description="Lightweight fungal metagenomics pipeline demo"
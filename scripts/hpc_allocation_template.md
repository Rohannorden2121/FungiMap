# HPC Allocation Request Template

**Subject**: HPC Resource Request - FungiMap Fungal Metagenomics Pipeline

## Project Overview

**Project Title**: FungiMap - Comprehensive Fungal Metagenomics Analysis  
**Principal Investigator**: [Your Name]  
**Institution**: [Your Institution]  
**Department**: [Your Department]  
**Grant/Funding**: [Grant number if applicable]  

## Scientific Justification

FungiMap is a computational pipeline for large-scale fungal metagenomics analysis, requiring high-performance computing resources for metagenomic assembly, gene prediction, and machine learning analysis. This work will advance understanding of fungal communities in [your specific research context].

## Resource Requirements Summary

### Stage 0: Quality Control & Validation
- **Purpose**: FastQC, MultiQC, sample validation
- **Resources**: 4 cores, 8GB RAM, 2 hours
- **Cost Estimate**: $5-10 per batch
- **Local Alternative**: Can run on laptop (demo available)

### Stage 1: Metagenomic Assembly  
- **Purpose**: MEGAHIT assembly, QUAST assessment
- **Resources**: 32 cores, 64GB RAM, 12-24 hours
- **Storage**: 100GB temporary, 20GB permanent
- **Cost Estimate**: $50-80 per batch (50 samples)
- **Critical Path**: Yes - requires HPC

### Stage 2: Gene Prediction & Annotation
- **Purpose**: Prodigal gene calling, HMMER annotation
- **Resources**: 16 cores, 32GB RAM, 6-12 hours  
- **Storage**: 50GB temporary, 10GB permanent
- **Cost Estimate**: $200-300 per batch
- **Dependencies**: Stage 1 assembly outputs

### Stage 3: Machine Learning Analysis
- **Purpose**: ESM protein embeddings, clustering
- **Resources**: 8 cores, 32GB RAM, 1x GPU (A100/V100), 4-8 hours
- **Storage**: 200GB temporary, 50GB permanent  
- **Cost Estimate**: $800-1200 per batch
- **Special Requirements**: GPU acceleration essential

### Full Pipeline
- **Purpose**: Complete analysis workflow
- **Resources**: Variable based on stages selected
- **Duration**: 24-48 hours total
- **Cost Estimate**: $20-30 per sample for full analysis

## Detailed Resource Specifications

### Compute Requirements
```bash
# Stage 1: Assembly
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=64GB
#SBATCH --time=24:00:00
#SBATCH --partition=compute

# Stage 2: Gene Prediction  
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=32GB
#SBATCH --time=12:00:00
#SBATCH --partition=compute

# Stage 3: ML Analysis
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=32GB
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00
#SBATCH --partition=gpu
```

### Storage Requirements
- **Input Data**: ~10GB per sample (FASTQ files)
- **Intermediate Files**: ~50GB per sample (assemblies, annotations)
- **Final Results**: ~5GB per sample (compressed outputs)
- **Database Storage**: 500GB (shared Kraken2/Bracken databases)
- **Total Project Storage**: 2-10TB depending on sample count

### Software Environment
- **Container**: Docker/Singularity support preferred
- **Conda**: Miniconda3 with environment specification provided
- **Dependencies**: Complete list in `environment.yml`
- **Databases**: Kraken2, Bracken, UniProt, Pfam

## Scaling and Batch Processing

### Sample Throughput
- **Small Scale**: 1-10 samples (development/testing)
- **Medium Scale**: 11-50 samples (typical study)
- **Large Scale**: 51-200 samples (population study)
- **Batch Processing**: Samples processed in parallel where possible

### Resource Scaling
| Sample Count | Total CPU Hours | Total GPU Hours | Storage (TB) | Estimated Cost |
|--------------|-----------------|-----------------|--------------|----------------|
| 1-10         | 100-500         | 20-40          | 0.5-1        | $200-500       |
| 11-50        | 500-2000        | 100-200        | 1-5          | $800-2000      |
| 51-200       | 2000-8000       | 400-800        | 5-20         | $3000-8000     |

## Timeline and Milestones

### Phase 1: Setup and Validation (Week 1-2)
- Environment setup and database installation
- Test runs with demo data
- Pipeline validation with small sample set

### Phase 2: Production Analysis (Week 3-8)  
- Full sample processing
- Quality control and validation
- Assembly and annotation

### Phase 3: Analysis and Results (Week 9-12)
- Machine learning analysis
- Result compilation and visualization
- Report generation and publication preparation

## Data Management Plan

### Input Data Sources
- **Public Repositories**: SRA/ENA accession numbers
- **Local Data**: Institutional sequencing facilities
- **Collaboration**: Partner institution data sharing

### Output Data Storage
- **Tier 1**: Essential results (permanent storage, 10+ years)
- **Tier 2**: Intermediate files (medium-term, 5-7 years)  
- **Tier 3**: Raw processing files (short-term, 1-2 years)

### Data Sharing
- **Publications**: Key results deposited in public repositories
- **Collaboration**: Controlled access for approved researchers
- **Archival**: Long-term preservation in institutional repositories

## Technical Support Needs

### Expertise Required
- **Bioinformatics**: Pipeline optimization and troubleshooting
- **HPC**: Job scheduling and resource optimization
- **Storage**: Data management and archival strategies

### Training and Documentation
- **User Training**: Pipeline usage and best practices
- **Documentation**: Comprehensive guides and troubleshooting
- **Support**: Ongoing technical assistance during project

## Expected Outcomes and Impact

### Scientific Deliverables
- **Publications**: 2-3 peer-reviewed manuscripts
- **Software**: Open-source pipeline with academic licensing
- **Data**: Public datasets for community use
- **Methods**: Standardized protocols for fungal metagenomics

### Broader Impact
- **Community Resource**: Pipeline available for other researchers
- **Educational Value**: Training materials and workshops
- **Collaboration**: Multi-institutional research network
- **Innovation**: Advanced methods for mycological research

## Budget Justification

### Cost-Benefit Analysis
- **HPC Costs**: $[X] for complete analysis
- **Alternative Costs**: $[Y] for cloud computing
- **Personnel Time**: Significant savings through automation
- **Scientific Value**: Enables research not possible otherwise

### Funding Sources
- **Grant Funding**: [Grant details]
- **Institutional Support**: [Department/university funding]
- **Collaboration**: Shared costs with partner institutions

---

## Contact Information

**Principal Investigator**: [Your Name]  
**Email**: [your.email@institution.edu]  
**Phone**: [Your Phone]  
**Institution**: [Your Institution]  
**Department**: [Your Department]  

**Technical Contact**: [Technical Lead Name]  
**Email**: [tech.contact@institution.edu]  

---

**Ready to submit**: Please modify this template with your specific details and submit to your HPC allocation committee.

*For technical questions about FungiMap, see documentation at [repository-url] or contact the development team.*
# FungiMap Data Archival and Preservation Plan

## Overview
This document outlines the comprehensive data archival strategy for FungiMap pipeline outputs, ensuring long-term preservation, accessibility, and compliance with FAIR (Findable, Accessible, Interoperable, Reusable) data principles.

## Archival Strategy

### Zenodo Integration
**Primary Repository**: Zenodo (zenodo.org)
- **Advantages**: 
  - Free for academic use (up to 50GB per dataset)
  - Persistent DOI assignment
  - CERN-backed infrastructure
  - Integration with GitHub releases
  - Version control for datasets
  - CC license support

**Large Dataset Strategy**:
- **Core Results Package** (<50GB): Direct Zenodo upload
- **Raw Data Archive** (>50GB): Split into logical chunks
- **Database Files**: Separate Zenodo records with cross-references

### Alternative Repositories
**Secondary Options**:
1. **Dryad** (datadryad.org): $120 per dataset, unlimited size
2. **Figshare** (figshare.com): 20GB free, institutional accounts
3. **OSF** (osf.io): Unlimited free storage for research
4. **NCBI SRA**: For raw sequencing data only

## Data Classification and Retention

### Tier 1: Essential Results (Permanent Archive)
**Contents**:
- Final taxonomic classifications
- Assembly statistics and quality metrics
- Protein structure predictions (representative set)
- Core embeddings and phylogenetic trees
- Analysis reports and visualizations

**Storage**: Zenodo with DOI
**Retention**: Permanent (10+ years)
**Size Estimate**: 10-50 GB per project

### Tier 2: Intermediate Data (Medium-term Archive)
**Contents**:
- Raw assembly contigs
- Full protein sequence sets
- Detailed quality control outputs
- Intermediate analysis files

**Storage**: Institutional repository + cloud backup
**Retention**: 5-7 years
**Size Estimate**: 100-500 GB per project

### Tier 3: Raw Data (Short-term Cache)
**Contents**:
- SRA FASTQ files
- Database downloads
- Temporary processing files
- Log files and debugging output

**Storage**: Local/cloud cache with periodic cleanup
**Retention**: 1-2 years
**Size Estimate**: 1-10 TB per project

## Zenodo Workflow

### 1. Automated Zenodo Upload Script
```bash
#!/bin/bash
# scripts/upload_to_zenodo.py

import requests
import json
import hashlib
import os
from pathlib import Path

def create_zenodo_record(access_token, metadata):
    """Create new Zenodo record with metadata"""
    headers = {"Content-Type": "application/json"}
    
    # Create deposition
    r = requests.post(
        'https://zenodo.org/api/deposit/depositions',
        params={'access_token': access_token},
        json={},
        headers=headers
    )
    
    deposition_id = r.json()['id']
    
    # Add metadata
    data = {
        'metadata': metadata
    }
    
    r = requests.put(
        f'https://zenodo.org/api/deposit/depositions/{deposition_id}',
        params={'access_token': access_token},
        data=json.dumps(data),
        headers=headers
    )
    
    return deposition_id

def upload_file_to_zenodo(access_token, deposition_id, file_path):
    """Upload file to Zenodo deposition"""
    bucket_url = f'https://zenodo.org/api/deposit/depositions/{deposition_id}/files'
    
    with open(file_path, 'rb') as fp:
        r = requests.put(
            f'{bucket_url}/{os.path.basename(file_path)}',
            params={'access_token': access_token},
            data=fp
        )
    
    return r.json()

def publish_zenodo_record(access_token, deposition_id):
    """Publish Zenodo record"""
    r = requests.post(
        f'https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish',
        params={'access_token': access_token}
    )
    
    return r.json()['doi']
```

### 2. Metadata Template
```json
{
    "title": "MycoGraph-XL: Comprehensive Mycological Genomics Analysis - Run {{DATE}}",
    "upload_type": "dataset",
    "description": "Complete results from MycoGraph-XL pipeline analysis including taxonomic classifications, genome assemblies, protein predictions, and phylogenetic reconstructions of mycological samples.",
    "creators": [
        {
            "name": "{{RESEARCHER_NAME}}",
            "affiliation": "{{INSTITUTION}}",
            "orcid": "{{ORCID_ID}}"
        }
    ],
    "keywords": [
        "mycology",
        "metagenomics",
        "fungi",
        "taxonomic classification",
        "genome assembly",
        "protein structure prediction",
        "phylogenetics"
    ],
    "license": "CC-BY-4.0",
    "access_right": "open",
    "language": "eng",
    "related_identifiers": [
        {
            "identifier": "https://github.com/{{USERNAME}}/mycology-predictor",
            "relation": "isSupplementTo",
            "resource_type": "software"
        }
    ],
    "grants": [
        {
            "id": "{{GRANT_ID}}"
        }
    ]
}
```

### 3. GitHub Release Integration
```yaml
# .github/workflows/zenodo-release.yml
name: Zenodo Archive Release

on:
  release:
    types: [published]

jobs:
  zenodo-upload:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Create Release Archive
      run: |
        tar -czf mycograph-xl-${{ github.event.release.tag_name }}.tar.gz \
          --exclude='.git' \
          --exclude='data/sra-cache' \
          --exclude='results/assemblies' \
          .
    
    - name: Upload to Zenodo
      env:
        ZENODO_TOKEN: ${{ secrets.ZENODO_TOKEN }}
      run: |
        python scripts/upload_to_zenodo.py \
          --file mycograph-xl-${{ github.event.release.tag_name }}.tar.gz \
          --title "MycoGraph-XL Pipeline Release ${{ github.event.release.tag_name }}" \
          --version ${{ github.event.release.tag_name }}
```

## Data Management Lifecycle

### Phase 1: Active Research (0-6 months)
- **Storage**: High-performance local/cloud storage
- **Backup**: Daily automated backups
- **Access**: Full read/write for research team
- **Monitoring**: Resource usage and cost tracking

### Phase 2: Analysis Complete (6-12 months)
- **Preparation**: Clean and organize results
- **Documentation**: Complete metadata and README files
- **Validation**: Verify data integrity and completeness
- **Initial Archive**: Upload core results to Zenodo

### Phase 3: Publication (12-24 months)
- **Peer Review**: Ensure data supports published claims
- **DOI Assignment**: Finalize Zenodo DOI for citations
- **Public Release**: Make data publicly accessible
- **Promotion**: Share via social media and conferences

### Phase 4: Long-term Preservation (2+ years)
- **Migration**: Move raw data to cold storage
- **Monitoring**: Check data integrity annually
- **Updates**: Version control for corrections or additions
- **Reuse**: Support other researchers accessing data

## Technical Implementation

### Checksum Verification
```bash
# Generate checksums for all archived files
find results/ -type f -exec sha256sum {} \; > checksums.sha256

# Verify checksums after transfer
sha256sum -c checksums.sha256
```

### Compression Strategy
```bash
# Optimal compression for different file types
tar -czf assemblies.tar.gz results/assemblies/          # General compression
xz -9 -T 0 large_database.sql                         # Maximum compression
pigz -9 -p 8 protein_sequences.fasta                  # Parallel compression
```

### Metadata Extraction
```python
# scripts/extract_metadata.py
import json
import os
from datetime import datetime

def extract_pipeline_metadata(results_dir):
    """Extract comprehensive metadata from pipeline results"""
    metadata = {
        "generation_date": datetime.now().isoformat(),
        "pipeline_version": "1.0.0",
        "sample_count": len(os.listdir(f"{results_dir}/eda/fastqc")),
        "total_size_gb": get_directory_size(results_dir) / (1024**3),
        "file_inventory": generate_file_inventory(results_dir),
        "software_versions": extract_software_versions(),
        "compute_resources": extract_resource_usage()
    }
    
    return metadata
```

## Compliance and Legal Considerations

### Data Protection
- **GDPR Compliance**: Ensure no personal data in biological samples
- **Export Control**: Verify no restricted computational methods
- **Institutional Policies**: Follow university data management requirements

### Intellectual Property
- **Copyright**: Clearly define ownership of generated data
- **Patents**: Consider patent implications of novel discoveries
- **Licensing**: Use permissive CC licenses for maximum reuse

### International Sharing
- **Nagoya Protocol**: Comply with access and benefit-sharing requirements
- **CITES**: Check restrictions on endangered species data
- **Dual Use**: Consider biosecurity implications of synthetic biology applications

## Quality Assurance

### Pre-Archive Checklist
- [ ] All result files present and complete
- [ ] Checksums generated and verified
- [ ] Metadata complete and accurate
- [ ] Documentation comprehensive
- [ ] File formats standardized and open
- [ ] Sensitive data removed or anonymized
- [ ] License and terms of use specified
- [ ] DOI reservation confirmed

### Post-Archive Validation
- [ ] Download test successful
- [ ] Metadata searchable in repository
- [ ] DOI resolves correctly
- [ ] Files accessible without errors
- [ ] Documentation renders properly
- [ ] Contact information current
- [ ] Backup copies verified

## Cost Estimation

### Zenodo (Free Tier)
- **Storage**: 50 GB per dataset (free)
- **Bandwidth**: Unlimited downloads (free)
- **DOI**: Included (free)
- **Maintenance**: CERN-supported (free)

### Institutional Repository
- **Setup**: $2,000-5,000 one-time
- **Annual**: $1,000-3,000 per year
- **Storage**: $50-100 per TB per year
- **Support**: Included with institutional membership

### Commercial Cloud Archive
- **AWS Glacier Deep Archive**: $1 per TB per month
- **GCP Coldline**: $4 per TB per month
- **Azure Archive**: $2 per TB per month
- **Retrieval**: $10-100 per TB (rare events)

## Success Metrics

### Technical Metrics
- **Uptime**: >99.9% availability
- **Download Speed**: >10 MB/s average
- **Error Rate**: <0.1% failed downloads
- **Response Time**: <5 seconds for metadata queries

### Usage Metrics
- **Citations**: Track papers citing the dataset DOI
- **Downloads**: Monitor access patterns and peak usage
- **Reuse**: Document secondary analyses using the data
- **Community**: Measure engagement and feedback

### Impact Metrics
- **Research Acceleration**: Time saved by other researchers
- **Cost Avoidance**: Resources not duplicated by others
- **Innovation**: New discoveries enabled by data reuse
- **Collaboration**: International partnerships formed
# FungiMap Archival Plan

## Overview
This document outlines the long-term data preservation and archival strategy for the FungiMap project, ensuring reproducibility, accessibility, and compliance with FAIR data principles (Findable, Accessible, Interoperable, Reusable).

## Archival Objectives
- **Preserve software versions and dependencies** for reproducibility
- **Archive research data and results** for future reference
- **Maintain accessible documentation** for long-term understanding
- **Ensure legal compliance** with institutional and funding requirements
- **Enable future research** through well-organized, discoverable data

## Repository Archival Strategy

### Code Repository
- **Primary Archive**: GitHub repository with comprehensive version history
- **Secondary Archive**: Zenodo software deposit with DOI assignment
- **Version Control**: Tagged releases with semantic versioning (v1.0.0, v1.1.0, etc.)
- **Documentation**: Comprehensive README, API docs, and usage examples
- **Dependencies**: environment.yml and requirements.txt for reproducibility

### Long-term Preservation
- **Institutional Repository**: Deposit in university/institutional archive
- **Software Heritage**: Automatic archival through GitHub integration
- **National Archives**: Consider deposit in relevant national scientific archives
- **Retention Period**: Minimum 10 years post-publication, indefinite for major versions

## Data Archival Framework

### Research Data Categories

#### 1. Input Datasets
- **Type**: Raw metagenomic sequences, reference genomes
- **Format**: FASTQ, FASTA files with standardized naming
- **Size**: ~100GB-1TB per study
- **Archive Location**: NCBI SRA, ENA, institutional data repository
- **Retention**: Indefinite (follows database policies)

#### 2. Intermediate Results
- **Type**: Quality control reports, assemblies, gene predictions
- **Format**: HTML reports, FASTA files, structured text
- **Size**: ~50-500GB per analysis
- **Archive Location**: Institutional repository, cloud storage
- **Retention**: 5 years active, 10 years archive

#### 3. Final Outputs
- **Type**: Species predictions, confidence scores, analysis reports
- **Format**: JSON, CSV, HTML reports
- **Size**: ~1-10GB per analysis
- **Archive Location**: Primary and secondary repositories
- **Retention**: Indefinite

#### 4. Machine Learning Models
- **Type**: Trained predictors, embeddings, model weights
- **Format**: PyTorch .pth, .pkl files, metadata JSON
- **Size**: ~1-50GB per model
- **Archive Location**: Model registry, versioned storage
- **Retention**: Indefinite for published models

### Metadata Standards
- **Dublin Core**: Basic bibliographic metadata
- **DataCite**: DOI-compatible metadata schema
- **FAIR Metrics**: Compliance with findability and accessibility
- **Domain-specific**: Bioinformatics metadata standards (e.g., MIAPPE)

## Storage Infrastructure

### Primary Storage Locations

#### Institutional Repository
- **Purpose**: Long-term preservation, institutional compliance
- **Provider**: University library/research office
- **Features**: Persistent URLs, metadata harvesting, backup systems
- **Cost**: Usually free for affiliated researchers
- **Example**: DSpace, Fedora, Samvera repositories

#### Cloud Storage Archives
- **AWS Glacier Deep Archive**: $1/TB/month, 12-hour retrieval
- **Google Cloud Archive**: $1.20/TB/month, 12-hour retrieval  
- **Azure Archive**: $1.00/TB/month, 15-hour retrieval
- **Purpose**: Cost-effective long-term storage for large datasets

#### Scientific Data Repositories
- **Zenodo**: Free, DOI assignment, EU-funded infrastructure
- **Figshare**: Academic data sharing, versioning, metrics
- **Dryad**: Curated data repository, peer review process
- **Domain-specific**: NCBI, ENA, JGI for genomic data

### Backup and Redundancy
- **3-2-1 Rule**: 3 copies, 2 different media types, 1 offsite
- **Geographic Distribution**: Multiple data centers/institutions
- **Integrity Checking**: Regular checksum verification
- **Recovery Testing**: Annual restore procedures

## Data Lifecycle Management

### Active Phase (0-2 years)
- **Storage**: High-performance local/cloud storage
- **Access**: Direct API access, web interfaces
- **Backup**: Daily incremental, weekly full backups
- **Monitoring**: Active health checks, performance metrics

### Archive Phase (2-10 years)  
- **Storage**: Standard cloud storage, institutional archives
- **Access**: Request-based retrieval, moderate latency
- **Backup**: Monthly verification, annual integrity checks
- **Documentation**: Maintained and updated as needed

### Deep Archive Phase (10+ years)
- **Storage**: Cold storage (Glacier, tape archives)
- **Access**: Scheduled retrieval, high latency acceptable
- **Backup**: Annual integrity verification
- **Documentation**: Frozen with format migration as needed

## Legal and Compliance Framework

### Data Ownership and Rights
- **Software License**: MIT License for open-source distribution
- **Data Rights**: Follow original data provider terms
- **Attribution**: Proper citation requirements in metadata
- **Derivative Works**: Clear licensing for processed outputs

### Privacy and Security
- **Data Classification**: Public, restricted, or confidential
- **Access Controls**: Role-based permissions, audit logging
- **De-identification**: Remove personal identifiers where required
- **Encryption**: At-rest and in-transit encryption for sensitive data

### Regulatory Compliance
- **GDPR**: European data protection (if applicable)
- **HIPAA**: Healthcare data (if applicable)
- **Institutional Policies**: IRB, data governance requirements
- **Funding Requirements**: NIH, NSF, other agency mandates

## Format Preservation Strategy

### File Format Migration
- **Current Formats**: FASTQ, FASTA, JSON, HTML, PyTorch models
- **Preservation Formats**: Open, standardized formats preferred
- **Migration Timeline**: Every 5-10 years or upon format obsolescence
- **Validation**: Ensure data integrity through migration process

### Software Dependencies
- **Container Images**: Docker containers for complete environment
- **Virtual Machines**: VM snapshots for full system preservation
- **Documentation**: Detailed installation and configuration guides
- **Version Pinning**: Exact dependency versions recorded

## Access and Discovery

### Metadata Cataloging
- **Search Keywords**: Fungi, metagenomics, machine learning, taxonomy
- **Subject Classification**: Bioinformatics, computational biology
- **Persistent Identifiers**: DOIs for datasets and software versions
- **API Access**: Programmatic metadata discovery

### User Access Patterns
- **Researchers**: Direct download, API access, cloud computing
- **Students**: Educational datasets, tutorial materials
- **Industry**: Licensed access to proprietary extensions
- **General Public**: Summary results, visualization tools

### Documentation Preservation
- **User Guides**: Step-by-step tutorials with examples
- **API Documentation**: Complete interface specifications
- **Technical Papers**: Published manuscripts, preprints
- **Video Tutorials**: Archived with closed captions

## Quality Assurance

### Data Validation
- **Checksum Verification**: SHA-256 for all archived files
- **Format Validation**: Automated checking of file structures
- **Content Review**: Periodic manual inspection of key datasets
- **Link Checking**: Ensure persistent URLs remain functional

### Recovery Testing
- **Annual Testing**: Restore representative data samples
- **Documentation Updates**: Fix any identified issues
- **Access Testing**: Verify all access methods function properly
- **Performance Benchmarks**: Monitor retrieval times and success rates

## Cost Management

### Storage Cost Projections
| Storage Tier | Data Type | Volume | Annual Cost |
|--------------|-----------|---------|-------------|
| Active | Working data | 1TB | $240 |
| Standard | Results | 5TB | $600 |
| Cold | Raw data | 50TB | $600 |
| Deep Archive | Historical | 100TB | $1200 |
| **Total** | | **156TB** | **$2640** |

### Cost Optimization
- **Lifecycle Policies**: Automatic tiering based on age/access
- **Compression**: Reduce storage footprint without data loss
- **Deduplication**: Eliminate redundant copies
- **Grant Funding**: Seek dedicated archival funding in proposals

## Implementation Timeline

### Phase 1: Foundation (Months 1-3)
- [ ] Establish institutional repository account
- [ ] Configure Zenodo deposit workflows
- [ ] Implement checksum verification system
- [ ] Create metadata templates

### Phase 2: Active Archival (Months 4-6)
- [ ] Begin systematic data cataloging
- [ ] Configure automated backup systems
- [ ] Establish access control procedures
- [ ] Train team on archival procedures

### Phase 3: Long-term Operations (Ongoing)
- [ ] Regular integrity checks and migrations
- [ ] Annual access testing and documentation updates
- [ ] Policy reviews and compliance audits
- [ ] Community feedback integration

## Success Metrics

### Accessibility Metrics
- **Discovery Rate**: Monthly searches/downloads of archived data
- **User Satisfaction**: Feedback scores on data access experience
- **Citation Impact**: Academic citations of archived datasets
- **Compliance Rate**: Successful completion of required archival processes

### Technical Metrics
- **Data Integrity**: 99.99% checksum validation success rate
- **Availability**: 99.9% uptime for access systems
- **Recovery Success**: 100% successful restoration from backups
- **Format Migration**: 100% successful format conversions

### Cost Efficiency
- **Storage Costs**: Maintain <$3000/year for standard research outputs
- **Staff Time**: <20 hours/month for archival maintenance
- **Access Costs**: Minimize charges for legitimate research access
- **Recovery Costs**: Budget for disaster recovery scenarios

## Contact and Governance

### Data Stewardship Team
- **Principal Investigator**: Overall responsibility and policy decisions
- **Data Manager**: Day-to-day operations and technical implementation
- **IT Support**: Infrastructure maintenance and security
- **Legal Counsel**: Compliance and rights management

### Review and Updates
- **Annual Review**: Policy effectiveness and cost analysis
- **Technology Updates**: Migration to new platforms/formats as needed
- **Stakeholder Feedback**: Input from users and institutional partners
- **Best Practices**: Adoption of evolving community standards

---

*This archival plan should be reviewed annually and updated as needed to reflect changing technologies, institutional policies, and community standards.*
# HPC/CLOUD SCALING PLAN - INSTANCE RECOMMENDATIONS & COST ESTIMATES
**Generated:** September 27, 2025  
**Phase:** Pre-Production Approval

## EXECUTIVE SUMMARY

### Scaling Recommendation: **HPC FIRST, CLOUD SECONDARY**
- **Rationale:** Cost-effective for academic/research use
- **Fallback:** Cloud for peak capacity or missing HPC access
- **Local Limit:** Stage 0 validation only (current pilot scope)

---

## DETAILED RESOURCE REQUIREMENTS BY STAGE

### STAGE 0: Validation & QC (CURRENT - LOCAL OK ✅)
| Resource | Requirement | Local Capacity | Status |
|----------|-------------|----------------|---------|
| **CPU** | 2-4 cores | 8 cores available | ✅ Sufficient |
| **Memory** | 2-4 GB | 16 GB available | ✅ Sufficient |
| **Storage** | 1-2 GB/sample | SSD available | ✅ Sufficient |
| **Runtime** | 5-10 min/sample | Acceptable | ✅ Suitable |

**Local Recommendation:** Continue current execution ✅

### STAGE 1: Assembly & Gene Prediction (REQUIRES HPC/CLOUD ❌)
| Resource | Requirement | Local Capacity | Status |
|----------|-------------|----------------|---------|
| **CPU** | 16-32 cores | 8 cores available | ❌ Insufficient |
| **Memory** | 32-128 GB | 16 GB available | ❌ Insufficient |
| **Storage** | 50-200 GB/sample | Limited | ❌ Insufficient |
| **Runtime** | 4-24 hours/sample | Too long | ❌ Impractical |

**Scaling Required:** HPC or Cloud infrastructure mandatory

### STAGE 2: Protein Analysis & ML (REQUIRES GPU CLOUD ❌)
| Resource | Requirement | Local Capacity | Status |
|----------|-------------|----------------|---------|
| **CPU** | 32+ cores | 8 cores available | ❌ Insufficient |
| **Memory** | 64-256 GB | 16 GB available | ❌ Insufficient |
| **GPU** | NVIDIA V100/A100 | None available | ❌ Missing |
| **Storage** | 100-500 GB | Limited | ❌ Insufficient |

**Scaling Required:** GPU-enabled cloud instances mandatory

---

## HPC CLUSTER RECOMMENDATIONS (PRIMARY CHOICE)

### Recommended HPC Configuration
```bash
#!/bin/bash
#SBATCH --job-name=mycograph-xl
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128G
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1  # For Stage 2 only
#SBATCH --output=mycograph_%j.out
#SBATCH --error=mycograph_%j.err

module load conda/latest
conda activate mycograph-xl

# Stage 1: Assembly (CPU-intensive)
snakemake --profile profiles/cluster stage1_assembly --cores 32

# Stage 2: Protein analysis (GPU-accelerated)  
snakemake --profile profiles/cluster stage2_analysis --cores 32
```

### HPC Cost Estimates (Academic Rates)
| Scale | Samples | Walltime | CPU Hours | Est. Cost |
|-------|---------|----------|-----------|----------|
| **Small** | 10 | 24 hours | 768 | $50-100 |
| **Medium** | 50 | 5 days | 3,840 | $200-400 |
| **Large** | 200 | 3 weeks | 15,360 | $800-1,500 |

**Advantages:**
- Lowest cost for academic users
- No data egress fees
- Existing institutional access
- Optimized for batch processing

---

## CLOUD INFRASTRUCTURE RECOMMENDATIONS (SECONDARY CHOICE)

### AWS Instance Recommendations

#### Stage 1: Assembly
- **Instance Type:** `c5.9xlarge` (36 vCPU, 72 GB RAM)
- **Storage:** 1 TB GP3 SSD
- **Runtime:** 8-12 hours per 50 samples
- **Cost:** $1.53/hour + storage

#### Stage 2: Protein Analysis  
- **Instance Type:** `p3.2xlarge` (8 vCPU, 61 GB RAM, 1 V100 GPU)
- **Storage:** 500 GB GP3 SSD  
- **Runtime:** 12-24 hours per 50 samples
- **Cost:** $3.06/hour + storage

### AWS Cost Breakdown (50 samples)
| Component | Hours | Rate | Cost |
|-----------|-------|------|------|
| **c5.9xlarge** | 12 | $1.53 | $18.36 |
| **p3.2xlarge** | 24 | $3.06 | $73.44 |
| **Storage (1.5TB)** | 720 hrs | $0.10/GB/mo | $15.00 |
| **Data Transfer** | 100 GB | $0.09/GB | $9.00 |
| **Total** | | | **$115.80** |

### Google Cloud Platform Alternative
| Instance Type | Purpose | vCPU | RAM | GPU | Cost/Hour |
|---------------|---------|------|-----|-----|-----------|
| **n2-highmem-32** | Assembly | 32 | 256 GB | - | $2.91 |
| **n1-standard-8** | Analysis | 8 | 30 GB | 1x V100 | $2.48 |

---

## SCALING TIMELINE & COST PROJECTIONS

### Phase 1: Small Scale (10-20 samples)
- **Timeline:** 1 week setup + 2 weeks processing
- **HPC Cost:** $100-200
- **Cloud Cost:** $250-500
- **Recommendation:** HPC preferred

### Phase 2: Medium Scale (50-100 samples)  
- **Timeline:** 2 weeks setup + 1 month processing
- **HPC Cost:** $400-800
- **Cloud Cost:** $1,000-2,000
- **Recommendation:** HPC with cloud burst

### Phase 3: Large Scale (200+ samples)
- **Timeline:** 1 month setup + 2 months processing  
- **HPC Cost:** $1,500-3,000
- **Cloud Cost:** $4,000-8,000
- **Recommendation:** Hybrid HPC/Cloud

---

## STORAGE REQUIREMENTS & COSTS

### Data Storage Needs
| Stage | Input | Intermediate | Output | Total/Sample |
|-------|-------|--------------|--------|--------------|
| **Stage 0** | 1 GB | 0.5 GB | 0.1 GB | 1.6 GB |
| **Stage 1** | 1 GB | 20 GB | 5 GB | 26 GB |
| **Stage 2** | 5 GB | 50 GB | 10 GB | 65 GB |

### Storage Cost Estimates (100 samples)
| Provider | Capacity | Cost/Month | Annual Cost |
|----------|----------|------------|-------------|
| **HFS Scratch** | 6.5 TB | $0 | $0 |
| **AWS S3** | 6.5 TB | $150 | $1,800 |
| **GCP Storage** | 6.5 TB | $130 | $1,560 |
| **Local** | 6.5 TB | $200 (one-time) | $200 |

---

## RECOMMENDED SCALING STRATEGY

### **TIER 1: HPC-First Approach** (RECOMMENDED)
1. **Setup Phase** (2 weeks)
   - Configure institutional HPC access
   - Deploy conda environments on cluster
   - Test with 5-10 samples

2. **Production Phase** (4-8 weeks)
   - Process full sample set on HPC
   - Use cloud for overflow/peak capacity
   - Maintain local for Stage 0 validation

3. **Monitoring Phase** (ongoing)
   - Track resource usage and costs
   - Optimize batch sizes and scheduling
   - Scale resources based on demand

### **TIER 2: Cloud-Native Approach** (if HPC unavailable)
1. **Infrastructure as Code** (1 week)
   - Deploy Terraform/CloudFormation
   - Set up auto-scaling groups
   - Configure monitoring and alerting

2. **Batch Processing** (2-4 weeks)
   - Use spot instances for cost savings
   - Implement checkpoint/restart capability
   - Monitor costs and optimize

### **TIER 3: Hybrid Approach** (for large scale)
- **Local:** Stage 0 validation and QC
- **HPC:** CPU-intensive assembly work
- **Cloud:** GPU-accelerated protein analysis
- **Cold Storage:** Long-term result archival

---

## IMMEDIATE NEXT STEPS (POST-APPROVAL)

### Week 1: Infrastructure Setup
- [ ] Secure HPC account/allocation  
- [ ] Configure cloud credentials
- [ ] Deploy cluster profiles
- [ ] Test with 2-3 samples

### Week 2: Pipeline Validation
- [ ] Run end-to-end test
- [ ] Validate resource usage
- [ ] Benchmark performance
- [ ] Document any issues

### Week 3: Production Launch
- [ ] Process full sample set
- [ ] Monitor resource utilization
- [ ] Generate comprehensive reports
- [ ] Plan next scaling phase

---

## FINAL RECOMMENDATION

### **PRIMARY: Submit to HPC** 🎯
- **Cost:** Lowest for academic users
- **Timeline:** 2-4 weeks for 50-100 samples
- **Risk:** Low, institutional support available

### **SECONDARY: Launch Cloud Instance** ☁️
- **Cost:** Higher but predictable
- **Timeline:** 1-2 weeks for setup + processing
- **Risk:** Medium, requires cloud expertise

### **CURRENT: Continue Local** 💻  
- **Cost:** $0
- **Timeline:** Immediate
- **Scope:** Stage 0 validation only (sufficient for current pilot)

**DECISION POINT:** Awaiting your approval to proceed with HPC/Cloud scaling for Stages 1-2.
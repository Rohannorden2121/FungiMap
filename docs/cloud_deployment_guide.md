# FungiMap Cloud Deployment Guide

## Resource Requirements and Cost Estimates

### Minimum Production Requirements
- **CPU**: 32 cores
- **Memory**: 128 GB RAM
- **Storage**: 2 TB SSD
- **Runtime**: 24-48 hours for full pipeline
- **GPU**: Optional but recommended for structure prediction (A100 or V100)

### Cloud Platform Comparisons

#### AWS EC2 Instances
**Recommended Instance**: `c5n.8xlarge` (32 vCPU, 72 GB RAM)
- **Hourly Cost**: ~$1.70/hour
- **48-hour Cost**: ~$82
- **Storage**: EBS gp3 2TB (~$200/month)
- **Total Estimated Cost**: $250-350 per full run

**GPU Instance**: `p3.2xlarge` (8 vCPU, 61 GB RAM, 1x V100)
- **Hourly Cost**: ~$3.06/hour
- **24-hour Cost**: ~$73
- **Use Case**: Structure prediction and embedding generation

#### Google Cloud Platform
**Recommended Instance**: `c2-standard-30` (30 vCPU, 120 GB RAM)
- **Hourly Cost**: ~$1.42/hour
- **48-hour Cost**: ~$68
- **Storage**: Persistent SSD 2TB (~$340/month)
- **Total Estimated Cost**: $200-300 per full run

**GPU Instance**: `a2-highgpu-1g` (12 vCPU, 85 GB RAM, 1x A100)
- **Hourly Cost**: ~$3.67/hour
- **24-hour Cost**: ~$88
- **Use Case**: Advanced structure prediction

#### Azure
**Recommended Instance**: `Standard_F32s_v2` (32 vCPU, 64 GB RAM)
- **Hourly Cost**: ~$1.34/hour
- **48-hour Cost**: ~$64
- **Storage**: Premium SSD 2TB (~$307/month)
- **Total Estimated Cost**: $180-280 per full run

### HPC Centers (Academic/Research)
**XSEDE/ACCESS Allocation Request**:
- **Compute Hours**: 2,000-4,000 SU (Service Units)
- **Storage**: 5-10 TB predictor allocation
- **Typical Grant**: $10,000-50,000 worth of compute time
- **Best Value**: Stampede2, Bridges-2, Expanse

**National Lab Resources**:
- **NERSC**: 50,000-200,000 core-hours/year
- **ALCF**: GPU allocations for AI/ML workflows
- **OLCF**: Summit supercomputer for large-scale analysis

## Deployment Scripts

### AWS Deployment
```bash
# Launch EC2 instance with appropriate IAM roles
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type c5n.8xlarge \
    --key-name mycograph-xl-key \
    --security-group-ids sg-12345678 \
    --subnet-id subnet-12345678 \
    --user-data file://cloud-init.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Predictor,Value=FungiMap}]'
```

### Docker Deployment
```bash
# Build production container
docker build -t mycograph-xl:production -f docker/Dockerfile.production .

# Run with resource limits
docker run -d \
    --name mycograph-xl-production \
    --cpus="32" \
    --memory="128g" \
    --volume $(pwd)/data:/app/data \
    --volume $(pwd)/results:/app/results \
    mycograph-xl:production
```

### Kubernetes Deployment
```yaml
# kubernetes/production-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mycograph-xl-production
spec:
  template:
    spec:
      containers:
      - name: mycograph-xl
        image: mycograph-xl:production
        resources:
          requests:
            memory: "128Gi"
            cpu: "32"
          limits:
            memory: "128Gi"
            cpu: "32"
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: results-volume
          mountPath: /app/results
      restartPolicy: Never
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: mycograph-xl-data
      - name: results-volume
        persistentVolumeClaim:
          claimName: mycograph-xl-results
```

## Cost Optimization Strategies

### 1. Spot Instances
- **AWS Spot**: 60-70% cost reduction
- **GCP Preemptible**: 60-80% cost reduction
- **Risk**: Instance termination
- **Mitigation**: Checkpointing and restart capability

### 2. Reserved Instances
- **1-year commitment**: 30-40% discount
- **3-year commitment**: 50-60% discount
- **Best for**: Recurring analysis workflows

### 3. Hybrid Approach
- **CPU-intensive stages**: Standard compute instances
- **GPU stages**: Dedicated GPU instances
- **Storage**: Separate persistent storage service

### 4. Pipeline Optimization
- **Parallel processing**: Split large datasets
- **Incremental analysis**: Process only new samples
- **Caching**: Reuse database builds and reference data

## Monitoring and Logging

### CloudWatch/Stackdriver Integration
```bash
# Install monitoring agent
curl -sSO https://dl.google.com/cloudops/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh
sudo apt-get update
sudo apt-get install google-logging-agent

# Configure custom metrics
echo "monitor.mycograph-xl.memory_usage: $(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}')" | \
  logger -t mycograph-xl-metrics
```

### Cost Alerts
- Set up billing alerts at $100, $200, $300
- Monitor resource utilization
- Automatic shutdown for idle instances

## Data Management

### Input Data
- **SRA Downloads**: Use SRA Toolkit with aggressive caching
- **Reference Databases**: Pre-download and snapshot
- **Staging Area**: Fast SSD for active processing

### Output Data
- **Immediate Results**: High-performance storage
- **Archive Data**: Cold storage (S3 Glacier, GCS Nearline)
- **Sharing**: Public S3 buckets with CloudFront CDN

### Backup Strategy
- **3-2-1 Rule**: 3 copies, 2 different media, 1 offsite
- **Automated snapshots**: Daily incremental backups
- **Version control**: Git LFS for large reference files

## Security Considerations

### Network Security
- **VPC/VNet isolation**: Private subnets for compute
- **Security groups**: Minimal required ports
- **VPN access**: Secure researcher connections

### Data Security
- **Encryption at rest**: AES-256 for all storage
- **Encryption in transit**: TLS 1.3 for all transfers
- **Access control**: IAM roles with least privilege

### Compliance
- **GDPR**: Data processing agreements
- **HIPAA**: If human microbiome data
- **Export control**: No restricted algorithms or data
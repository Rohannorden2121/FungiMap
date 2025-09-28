# FungiMap Cloud Deployment Guide

## Recommended Cloud Instances

### AWS EC2 Instances

#### Stage 0: Quality Control & Taxonomic Profiling
- **Instance Type**: `c5.2xlarge`
- **Specifications**: 8 vCPUs, 16 GB RAM
- **Estimated Cost**: $5-10 per job (2-4 hours)
- **Storage**: 100GB EBS gp3 volume

#### Stage 1: Assembly & Gene Prediction  
- **Instance Type**: `c5.4xlarge`
- **Specifications**: 16 vCPUs, 32 GB RAM
- **Estimated Cost**: $50-80 per job (8-12 hours)
- **Storage**: 500GB EBS gp3 volume

#### Stage 2: Protein Clustering & ML
- **Instance Type**: `c5.6xlarge` 
- **Specifications**: 24 vCPUs, 48 GB RAM
- **Estimated Cost**: $200-300 per job (16-24 hours)
- **Storage**: 1TB EBS gp3 volume

#### Stage 3: Deep Learning Predictor
- **Instance Type**: `p3.8xlarge`
- **Specifications**: 32 vCPUs, 244 GB RAM, 4x V100 GPUs
- **Estimated Cost**: $800-1200 per job (24-48 hours)
- **Storage**: 2TB EBS gp3 volume

#### Full Pipeline (Pre-trained Models)
- **Instance Type**: `c5.2xlarge`
- **Specifications**: 8 vCPUs, 16 GB RAM
- **Estimated Cost**: $20-30 per job (4-8 hours)
- **Storage**: 200GB EBS gp3 volume

### Google Cloud Platform (GCP) Instances

#### Stage 0-1: Standard Processing
- **Machine Type**: `c2-standard-8`
- **Specifications**: 8 vCPUs, 32 GB RAM
- **Estimated Cost**: $40-60 per job

#### Stage 2: Intensive Clustering
- **Machine Type**: `c2-standard-16`
- **Specifications**: 16 vCPUs, 64 GB RAM
- **Estimated Cost**: $150-250 per job

#### Stage 3: GPU Training
- **Machine Type**: `a2-highgpu-4g`
- **Specifications**: 48 vCPUs, 340 GB RAM, 4x A100 GPUs
- **Estimated Cost**: $600-1000 per job

### Microsoft Azure Instances

#### General Processing
- **VM Size**: `Standard_D8s_v3`
- **Specifications**: 8 vCPUs, 32 GB RAM
- **Estimated Cost**: $35-55 per job

#### GPU Processing
- **VM Size**: `Standard_NC24s_v3`
- **Specifications**: 24 vCPUs, 448 GB RAM, 4x V100 GPUs
- **Estimated Cost**: $700-1100 per job

## Container Deployment

### Docker Images
```bash
# Pull FungiMap containers
docker pull fungimap/pipeline:latest
docker pull fungimap/predictor:latest-gpu

# Run with appropriate resources
docker run --rm -v $(pwd):/data fungimap/pipeline:latest \
    snakemake --cores 8 --resources mem_mb=32000
```

### Singularity/Apptainer (HPC)
```bash
# Convert Docker images
singularity pull fungimap-pipeline.sif docker://fungimap/pipeline:latest

# Run on HPC
singularity exec --bind /scratch:/data fungimap-pipeline.sif \
    snakemake --cores ${SLURM_NTASKS}
```

## Kubernetes Deployments

### Resource Specifications
```yaml
# fungimap-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: fungimap-pipeline
spec:
  template:
    spec:
      containers:
      - name: fungimap
        image: fungimap/pipeline:latest
        resources:
          requests:
            memory: "32Gi"
            cpu: "8"
          limits:
            memory: "64Gi"
            cpu: "16"
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: fungimap-data
      restartPolicy: Never
```

## Storage Requirements

### Minimum Storage by Stage
- **Stage 0**: 50GB (raw data + QC reports)
- **Stage 1**: 200GB (assemblies + gene predictions)
- **Stage 2**: 500GB (protein clusters + ML models)
- **Stage 3**: 1TB (deep learning models + embeddings)
- **Full Pipeline**: 100GB (final results only)

### Recommended Storage Configuration
- **Input Data**: S3/GCS/Azure Blob (cold storage)
- **Working Data**: NVMe SSD (high IOPS)
- **Results**: S3/GCS/Azure Blob (standard storage)
- **Models**: S3/GCS/Azure Blob (standard storage with versioning)

## Cost Optimization Strategies

### Spot/Preemptible Instances
- Use spot instances for Stages 0-2 (fault-tolerant)
- Avoid spot instances for Stage 3 (long-running GPU jobs)
- Expected savings: 50-70% on compute costs

### Auto-scaling Groups
```bash
# AWS Auto Scaling configuration
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name fungimap-workers \
    --instance-id i-1234567890abcdef0 \
    --min-size 0 \
    --max-size 10 \
    --desired-capacity 2
```

### Reserved Instances
- Purchase reserved instances for predictable workloads
- 1-year commitment: 30-40% savings
- 3-year commitment: 50-60% savings

## Networking Requirements

### Bandwidth
- **Stage 0**: 1-5 Mbps (data download)
- **Stage 1-3**: Minimal (local processing)
- **Results Upload**: 10-50 Mbps (depending on output size)

### Security Groups/Firewall Rules
```bash
# AWS Security Group
aws ec2 create-security-group \
    --group-name fungimap-compute \
    --description "FungiMap compute instances"

# Allow SSH access
aws ec2 authorize-security-group-ingress \
    --group-name fungimap-compute \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

## Monitoring and Logging

### CloudWatch/Stackdriver Metrics
- **CPU Utilization**: Target 70-90% during active processing
- **Memory Usage**: Monitor for OOM conditions
- **Disk I/O**: Track read/write patterns
- **Network**: Monitor data transfer costs

### Log Aggregation
```bash
# CloudWatch Logs agent configuration
[/var/log/fungimap/pipeline.log]
file = /var/log/fungimap/pipeline.log
log_group_name = /fungimap/pipeline
log_stream_name = {instance_id}
datetime_format = %Y-%m-%d %H:%M:%S
```

## Deployment Automation

### Terraform Configuration
```hcl
# main.tf
resource "aws_instance" "fungimap_compute" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2
  instance_type = var.instance_type
  key_name      = var.key_name
  
  user_data = file("${path.module}/scripts/setup.sh")
  
  tags = {
    Name = "FungiMap-${var.stage}"
    Project = "FungiMap"
  }
}
```

### AWS Batch
```json
{
  "jobDefinition": {
    "jobDefinitionName": "fungimap-pipeline",
    "type": "container",
    "containerProperties": {
      "image": "fungimap/pipeline:latest",
      "vcpus": 8,
      "memory": 32768,
      "jobRoleArn": "arn:aws:iam::123456789012:role/BatchJobRole"
    }
  }
}
```

## Data Management

### Input Data Staging
```bash
# AWS S3 sync
aws s3 sync s3://fungimap-input-data/ /data/input/ \
    --exclude "*.tmp" \
    --include "*.fastq.gz"
```

### Result Archival
```bash
# Compress and upload results
tar -czf results-${JOB_ID}.tar.gz results/
aws s3 cp results-${JOB_ID}.tar.gz s3://fungimap-results/
```

### Backup Strategy
- **Daily**: Incremental backups of active data
- **Weekly**: Full backups of completed results
- **Monthly**: Archive to glacier/coldline storage
- **Retention**: 90 days active, 1 year archive

## Performance Tuning

### Memory Optimization
- Use memory-mapped files for large datasets
- Configure swap space for memory-intensive stages
- Monitor memory fragmentation

### Disk I/O Optimization
- Use NVMe SSD for temporary files
- Configure appropriate block sizes
- Enable disk caching where beneficial

### Network Optimization
- Use placement groups for multi-instance jobs
- Configure enhanced networking
- Optimize data transfer patterns
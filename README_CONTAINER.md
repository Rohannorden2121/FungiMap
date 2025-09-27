# Container Usage Instructions

## Quick Start with Docker

1. Build the container:
```bash
docker-compose build
```

2. Run the pipeline:
```bash
docker-compose run pipeline snakemake --profile profiles/local
```

## Using Different Execution Profiles

### Local Execution
```bash
docker-compose run pipeline snakemake --profile profiles/local
```

### Cloud Execution
```bash
docker-compose run pipeline snakemake --profile profiles/cloud
```

## Development

To develop inside the container:
```bash
docker-compose run --service-ports pipeline bash
```

## Environment Variables

The following environment variables can be set:
- `MYCOGRAPH_CORES`: Number of cores to use (default: all)
- `MYCOGRAPH_MEM`: Memory limit in GB (default: 16)

## Data Volumes

The following volumes are mounted:
- `./data`: Input data directory
- `./results`: Pipeline results
- `./workflow`: Workflow definitions

## Distributed Execution

For distributed execution, ensure Redis is running:
```bash
docker-compose up -d redis
```
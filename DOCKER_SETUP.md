# Docker Setup Instructions for macOS

## 1. Install Docker Desktop

1. Download Docker Desktop for Mac from the official website:
   - Visit https://www.docker.com/products/docker-desktop
   - Click "Download for Mac"
   - Choose the appropriate version:
     * For Apple Silicon (M1/M2): Download "Apple Chip" version
     * For Intel: Download "Intel Chip" version

2. Install Docker Desktop:
   - Open the downloaded `.dmg` file
   - Drag Docker.app to your Applications folder
   - Double-click Docker.app to start Docker Desktop

3. Verify Installation:
   ```bash
   docker --version
   ```

## 2. Docker Compose Setup

Docker Compose comes bundled with Docker Desktop for Mac, but verify the installation:
```bash
docker compose version
```

## 3. Configure Docker Desktop

1. Open Docker Desktop
2. Go to Preferences (⚙️):
   - Resources > Advanced:
     * CPUs: Set to 8 (or half your system's cores)
     * Memory: Set to 16 GB (or half your system's RAM)
     * Swap: Set to 2 GB
   - Docker Engine:
     * Increase default ulimits if needed for pipeline

## 4. Test Installation

Run these commands to verify everything is working:
```bash
# Test Docker
docker run hello-world

# Test Docker Compose
docker compose version
```

## 5. Next Steps

Once Docker is installed:
1. Return to project directory:
   ```bash
   cd /Users/rohannorden/My Code/mycology-predictor
   ```

2. Build the pipeline container:
   ```bash
   docker compose build
   ```

## Troubleshooting

1. If Docker Desktop won't start:
   - Check System Preferences > Security & Privacy
   - Look for message about system software from "Docker, Inc."
   - Click "Allow"

2. If you get permissions errors:
   ```bash
   # Reset Docker Desktop to factory defaults
   docker system prune -a
   ```

3. For performance issues:
   - Adjust CPU/Memory allocation in Docker Desktop preferences
   - Check resource usage in Docker Desktop dashboard

## Notes

- Docker Desktop requires admin privileges for installation
- First build may take 10-15 minutes while downloading base images
- Container storage location can be changed in Docker Desktop preferences if needed

For any issues, consult:
- Docker Desktop documentation: https://docs.docker.com/desktop/mac/
- Docker Compose documentation: https://docs.docker.com/compose/
# FungiMap Release Checklist v0.1-demo

## ✅ Pre-Release Validation Complete

### Repository Cleanup
- [x] **Large files removed**: Files >100MB moved to manifest references
- [x] **Demo data optimized**: 2MB demo dataset in `data/demo/`
- [x] **Checksums verified**: All manifest entries validated with SHA-256
- [x] **Dependencies updated**: `.gitignore` cleaned and comprehensive

### Governance Files
- [x] **MIT License**: Professional open source license in place
- [x] **CITATION.md**: Complete academic citation format
- [x] **CONTRIBUTING.md**: Developer contribution guidelines
- [x] **CODE_OF_CONDUCT.md**: Community standards established

### Testing & Validation
- [x] **CI smoke test**: 5/5 tests passed successfully
- [x] **Demo functionality**: 3-command quickstart validated
- [x] **Environment setup**: Conda environment builds cleanly
- [x] **Docker readiness**: Dockerfile present (Docker not installed locally)

### Documentation
- [x] **README.md**: Professional project documentation
- [x] **README_QUICKSTART.md**: 3-command demo instructions
- [x] **DELIVERABLE_MANIFEST.md**: Complete deliverable catalog
- [x] **Technical docs**: Comprehensive user and developer guides

## 🚀 Release Preparation

### Version Information
- **Version**: v0.1-demo
- **Tag**: v0.1-demo
- **Type**: Draft release
- **Audience**: Demonstration and evaluation

### Release Assets (Source Only)
- [x] **Source tarball**: Automated GitHub generation
- [x] **Documentation**: All `.md` files included
- [x] **Configuration**: Demo-ready environment files
- [x] **Scripts**: Complete pipeline and utility scripts

### 3-Command Quickstart Demo
```bash
# Verified working commands:
conda activate fungimap-test
python scripts/create_demo_data.py  
bash src/run_eda_pipeline.sh
```
**Status**: ✅ PASS - All components functional

### CI/Testing Status
- **Smoke Test**: ✅ PASS (5/5 tests)
- **Environment**: ✅ PASS (conda environment verified)
- **Demo Data**: ✅ PASS (2MB dataset generated)
- **Docker**: ⚠️ SKIP (Docker not installed, Dockerfile ready)

## 📋 Commit-Ready Checklist

### Files to Commit
- [x] Updated `.gitignore` with comprehensive exclusions
- [x] `data/demo/` with optimized demo dataset (2MB)
- [x] All governance files (LICENSE, CITATION.md, etc.)
- [x] Updated checksums and manifest
- [x] Release preparation files

### Files to Exclude (Large/Generated)
- [x] Raw SRA data files (>100MB)
- [x] Kraken2 database files (>1GB)
- [x] Intermediate processing outputs
- [x] Git objects from large file history

### Repository State
- **Branch**: Ready for main/master merge
- **Size**: <50MB (excluding large data references)
- **Tests**: All passing
- **Documentation**: Complete and current

## 🎯 Final Actions Required

1. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: finalize demo-ready repository v0.1

   - Complete repository cleanup and optimization
   - Add comprehensive governance files
   - Validate 3-command quickstart demo
   - Prepare for public demonstration release"
   
   git push origin main
   ```

2. **Create Draft Release**
   - Tag: v0.1-demo
   - Title: "FungiMap v0.1-demo - Demonstration Release"
   - Assets: Source tarball + documentation only
   - Status: Draft (not published)

3. **Zenodo Deposit Draft**
   - Complete metadata with DELIVERABLE_MANIFEST.md reference
   - External data pointers (no large file uploads)
   - Academic citation format
   - Status: Draft (not published)

## ⚠️ Approval Gates

**HOLDS - Require explicit approval:**
- [ ] Publish GitHub release (APPROVE: publish release)
- [ ] Publish Zenodo DOI (APPROVE: publish DOI)  
- [ ] Run production HPC jobs (APPROVE: run <stage>)

**READY FOR COMMIT** - All validation complete, repository cleaned and tested.
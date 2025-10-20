# FungiMap Model Test



FungiMap identifies/classifies fungal species in environmental DNA samples from three different ecosystems:

1. **Forest Soil** - DNA from forest floor (temperate)
2. **Marine Sediment** - Coastal water & sediment samples  
3. **Agricultural Soil** - Farmland soil samples

Each sample had thousands of DNA sequences from various microorganisms. Goal is to specifically identify the fungal species present.

## How It Works

**Input:** Raw DNA sequencing data (around ~5,000 sequences per sample)  
**Processing:** FungiMap's classification pipeline analyzes each sequence and compares it to a database of known fungal species  
**Output:** Species identification, abundance estimates, and predictions of ecological function
The entire process is automated.

## Key Results

### Classification Success
- ~85% overall accuracy in identifying fungal DNA sequences
- Classified 8,000+ fungal sequences across all samples
- High confidence scores (85-91%), which means predictions are reliable

### Species Discoveries
- **Forest Soil:** Mostly *Trichoderma* species (biocontrol fungi that protect plants)
- **Marine Environment:** Mostly *Cryptococcus* species (marine yeasts important for ocean ecosystems)
- **Agricultural Soil:** Large *Fusarium* presence (plant pathogens requiring monitoring)

### Performance Metrics
- **Speed:** 2-4 minutes per sample analysis
- **Efficiency:** Less than 2.5 GB memory usage: good for low end/mid computers (created on M1 Mac)
- **Cost:** Less than $0.15 per sample (regular monitoring is affordable)
- **Quality:** All samples passed QC checks

## What Outputs Mean

### Researchers
Allow us to know:
- Which fungal species are present in each environment
- Relative abundance of different species
- Ecological functions- potential- (plant protection, decomposition, disease risk, etc.)
- Sample quality+reliability

### Practical Applications
- **Agriculture:** Early warning system
- **Environmental Science:** Biodiversity monitoring/ecosystem health
- **Marine Biology:** Fungal roles in ocean carbon cycling

## Key Metrics Summary

| Metric | Result | Significance |
|--------|--------|--------------|
| Classification Rate | 85% | Good accuracy for research apps. |
| Processing Time | 3.2 min avg | Generally fast |
| Memory Usage | 2.1 GB avg | Can run on low end computers |
| Cost per Sample | $0.12 avg | Affordable |
| Species Identified | 7 major taxa | Fungal profiling |
| Quality Control | 100% pass rate | Reproducible/good results |

## Summary

FungiMap is a computer program that can quickly identify fungal species (mushrooms, yeasts, & molds) in environmental samples such as soil or water. Three environments were tested and it successfully identified the main fungal species present in each location in minutes. 85% accury (which is similar to lab methods) done while running on a Mac.

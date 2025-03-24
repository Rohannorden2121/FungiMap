#!/usr/bin/env python3
"""
Create mock demo data for M1 Mac pilot testing
Generates small FASTQ files to test the pipeline without heavy downloads
"""

import random
import gzip
from pathlib import Path

def generate_mock_fastq(sample_name, num_reads=10000, output_dir="data/demo"):
    """Generate a small mock FASTQ file"""
    
    output_path = Path(output_dir) / f"{sample_name}_demo.fastq.gz"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # DNA bases
    bases = ['A', 'T', 'C', 'G']
    
    # Quality scores (Phred+33)
    qualities = [chr(i) for i in range(33, 75)]  # Quality 0-42
    
    print(f"Generating {num_reads} mock reads for {sample_name}...")
    
    with gzip.open(output_path, 'wt') as f:
        for i in range(num_reads):
            # Read ID
            f.write(f"@{sample_name}_read_{i:06d}\n")
            
            # Sequence (random 100bp with some fungal-like patterns)
            if i % 10 == 0:  # 10% fungal-like sequences
                seq = "ATCGATCGATCGATCG" + "".join(random.choices(bases, k=84))
            else:
                seq = "".join(random.choices(bases, k=100))
            f.write(seq + "\n")
            
            # Plus line
            f.write("+\n")
            
            # Quality scores (mostly good quality)
            qual = "".join(random.choices(qualities[-20:], k=100))  # High quality
            f.write(qual + "\n")
    
    print(f"✅ Created mock data: {output_path}")
    return output_path

if __name__ == "__main__":
    samples = ["SRR13059548", "SRR15377549"]
    
    for sample in samples:
        generate_mock_fastq(sample, num_reads=10000)
    
    print("🎉 Demo data generation complete!")
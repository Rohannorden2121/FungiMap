#!/usr/bin/env python3
"""
Protein embedding generation using ESM models for FungiMap Stage 3.
Generates protein embeddings for downstream ML analysis.
"""

import argparse
import h5py
import numpy as np
import torch
from pathlib import Path
from Bio import SeqIO
from transformers import EsmModel, EsmTokenizer
import logging
from typing import List, Dict
import time

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_esm_model(model_name: str, device: str = "cuda"):
    """Load ESM model and tokenizer."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Loading ESM model: {model_name}")
    tokenizer = EsmTokenizer.from_pretrained(f"facebook/{model_name}")
    model = EsmModel.from_pretrained(f"facebook/{model_name}")
    
    # Move to GPU if available
    if device == "cuda" and torch.cuda.is_available():
        model = model.to(device)
        logger.info(f"Model moved to GPU: {torch.cuda.get_device_name()}")
    else:
        device = "cpu"
        logger.info("Using CPU for inference")
    
    model.eval()
    return model, tokenizer, device

def process_proteins_batch(sequences: List[str], model, tokenizer, device: str, batch_size: int = 32):
    """Process protein sequences in batches."""
    logger = logging.getLogger(__name__)
    
    embeddings = []
    total_proteins = len(sequences)
    
    for i in range(0, total_proteins, batch_size):
        batch = sequences[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_proteins + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} proteins)")
        
        try:
            # Tokenize batch
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=1024)
            
            if device == "cuda":
                inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = model(**inputs)
                # Use mean pooling over sequence length
                batch_embeddings = outputs.last_hidden_state.mean(dim=1)
                
                if device == "cuda":
                    batch_embeddings = batch_embeddings.cpu()
                
                embeddings.extend(batch_embeddings.numpy())
        
        except Exception as e:
            logger.error(f"Error processing batch {batch_num}: {e}")
            # Add zero embeddings for failed batch
            embedding_dim = 1280 if "650M" in model.config.name_or_path else 640
            batch_embeddings = np.zeros((len(batch), embedding_dim))
            embeddings.extend(batch_embeddings)
    
    return np.array(embeddings)

def main():
    parser = argparse.ArgumentParser(description="Generate protein embeddings using ESM models")
    parser.add_argument("--input", required=True, help="Input FASTA file with protein sequences")
    parser.add_argument("--output", required=True, help="Output HDF5 file for embeddings")
    parser.add_argument("--model", default="esm2_t33_650M_UR50D", help="ESM model to use")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size for processing")
    parser.add_argument("--device", default="cuda", help="Device to use (cuda/cpu)")
    
    args = parser.parse_args()
    logger = setup_logging()
    
    start_time = time.time()
    
    # Load protein sequences
    logger.info(f"Loading protein sequences from {args.input}")
    sequences = []
    protein_ids = []
    
    try:
        for record in SeqIO.parse(args.input, "fasta"):
            sequences.append(str(record.seq))
            protein_ids.append(record.id)
    except Exception as e:
        logger.error(f"Error reading FASTA file: {e}")
        return 1
    
    logger.info(f"Loaded {len(sequences)} protein sequences")
    
    if len(sequences) == 0:
        logger.warning("No sequences found in input file")
        return 1
    
    # Load model
    try:
        model, tokenizer, device = load_esm_model(args.model, args.device)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return 1
    
    # Generate embeddings
    logger.info("Generating protein embeddings...")
    try:
        embeddings = process_proteins_batch(sequences, model, tokenizer, device, args.batch_size)
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return 1
    
    # Save embeddings
    logger.info(f"Saving embeddings to {args.output}")
    try:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        
        with h5py.File(args.output, 'w') as f:
            f.create_dataset('embeddings', data=embeddings)
            f.create_dataset('protein_ids', data=[id.encode('utf-8') for id in protein_ids])
            f.attrs['model'] = args.model
            f.attrs['n_proteins'] = len(sequences)
            f.attrs['embedding_dim'] = embeddings.shape[1]
            f.attrs['generation_time'] = time.time() - start_time
    
    except Exception as e:
        logger.error(f"Error saving embeddings: {e}")
        return 1
    
    end_time = time.time()
    logger.info(f"Embedding generation completed in {end_time - start_time:.2f} seconds")
    logger.info(f"Average time per protein: {(end_time - start_time) / len(sequences):.4f} seconds")
    
    return 0

if __name__ == "__main__":
    exit(main())
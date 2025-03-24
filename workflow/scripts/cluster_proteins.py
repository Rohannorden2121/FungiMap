#!/usr/bin/env python3
"""
Protein clustering script for FungiMap Stage 3.
Clusters protein embeddings for functional analysis.
"""

import argparse
import h5py
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import logging
from typing import List, Tuple
import time

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_embeddings(embedding_files: List[str]) -> Tuple[np.ndarray, List[str], List[str]]:
    """Load embeddings from multiple HDF5 files."""
    logger = logging.getLogger(__name__)
    
    all_embeddings = []
    all_protein_ids = []
    all_samples = []
    
    for file_path in embedding_files:
        logger.info(f"Loading embeddings from {file_path}")
        
        try:
            with h5py.File(file_path, 'r') as f:
                embeddings = f['embeddings'][:]
                protein_ids = [id.decode('utf-8') for id in f['protein_ids'][:]]
                
                # Extract sample name from file path
                sample_name = Path(file_path).parent.name
                
                all_embeddings.append(embeddings)
                all_protein_ids.extend(protein_ids)
                all_samples.extend([sample_name] * len(protein_ids))
                
                logger.info(f"Loaded {len(protein_ids)} proteins from {sample_name}")
        
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            continue
    
    if not all_embeddings:
        raise ValueError("No embeddings loaded successfully")
    
    # Concatenate all embeddings
    combined_embeddings = np.vstack(all_embeddings)
    logger.info(f"Total proteins: {len(all_protein_ids)}, embedding dimension: {combined_embeddings.shape[1]}")
    
    return combined_embeddings, all_protein_ids, all_samples

def perform_clustering(embeddings: np.ndarray, threshold: float = 0.8, max_clusters: int = 10000) -> np.ndarray:
    """Perform hierarchical clustering on protein embeddings."""
    logger = logging.getLogger(__name__)
    
    n_proteins = embeddings.shape[0]
    logger.info(f"Starting clustering of {n_proteins} proteins with threshold {threshold}")
    
    start_time = time.time()
    
    # Use AgglomerativeClustering with cosine distance
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=1-threshold,  # Convert similarity to distance
        linkage='average',
        metric='cosine'
    )
    
    try:
        cluster_labels = clustering.fit_predict(embeddings)
        n_clusters = len(np.unique(cluster_labels))
        
        # Calculate silhouette score for quality assessment
        if n_clusters > 1 and n_proteins < 10000:  # Skip for very large datasets
            silhouette = silhouette_score(embeddings, cluster_labels, metric='cosine')
            logger.info(f"Silhouette score: {silhouette:.3f}")
        
        clustering_time = time.time() - start_time
        logger.info(f"Clustering completed: {n_clusters} clusters in {clustering_time:.2f} seconds")
        
        return cluster_labels
    
    except Exception as e:
        logger.error(f"Clustering failed: {e}")
        # Return single cluster for all proteins as fallback
        logger.warning("Assigning all proteins to single cluster as fallback")
        return np.zeros(n_proteins, dtype=int)

def analyze_clusters(cluster_labels: np.ndarray, protein_ids: List[str], samples: List[str]) -> pd.DataFrame:
    """Analyze clustering results and create summary."""
    logger = logging.getLogger(__name__)
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'protein_id': protein_ids,
        'sample': samples,
        'cluster': cluster_labels
    })
    
    # Cluster statistics
    n_clusters = len(np.unique(cluster_labels))
    cluster_sizes = pd.Series(cluster_labels).value_counts().sort_values(ascending=False)
    
    logger.info(f"Clustering Analysis:")
    logger.info(f"  Total proteins: {len(protein_ids)}")
    logger.info(f"  Number of clusters: {n_clusters}")
    logger.info(f"  Largest cluster size: {cluster_sizes.iloc[0]}")
    logger.info(f"  Smallest cluster size: {cluster_sizes.iloc[-1]}")
    logger.info(f"  Average cluster size: {cluster_sizes.mean():.1f}")
    
    # Singletons (clusters with only one protein)
    singletons = len(cluster_sizes[cluster_sizes == 1])
    logger.info(f"  Singleton clusters: {singletons} ({singletons/n_clusters*100:.1f}%)")
    
    return results_df

def main():
    parser = argparse.ArgumentParser(description="Cluster protein embeddings")
    parser.add_argument("--embeddings", nargs='+', required=True, help="Input HDF5 embedding files")
    parser.add_argument("--output", required=True, help="Output CSV file for cluster assignments")
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold for clustering")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads (not used in current implementation)")
    
    args = parser.parse_args()
    logger = setup_logging()
    
    start_time = time.time()
    
    # Load embeddings
    try:
        embeddings, protein_ids, samples = load_embeddings(args.embeddings)
    except Exception as e:
        logger.error(f"Error loading embeddings: {e}")
        return 1
    
    # Perform clustering
    try:
        cluster_labels = perform_clustering(embeddings, args.threshold)
    except Exception as e:
        logger.error(f"Error during clustering: {e}")
        return 1
    
    # Analyze results
    try:
        results_df = analyze_clusters(cluster_labels, protein_ids, samples)
    except Exception as e:
        logger.error(f"Error analyzing clusters: {e}")
        return 1
    
    # Save results
    try:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(args.output, index=False)
        logger.info(f"Cluster results saved to {args.output}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        return 1
    
    total_time = time.time() - start_time
    logger.info(f"Protein clustering completed in {total_time:.2f} seconds")
    
    return 0

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
ML model training script for FungiMap Stage 3.
Trains classification models using protein clusters and validation data.
"""

import argparse
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging
import time


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def load_cluster_data(cluster_file: str) -> pd.DataFrame:
    """Load protein cluster assignments."""
    logger = logging.getLogger(__name__)

    logger.info(f"Loading cluster data from {cluster_file}")
    cluster_df = pd.read_csv(cluster_file)

    logger.info(f"Loaded {len(cluster_df)} protein cluster assignments")
    logger.info(f"Number of unique clusters: {cluster_df['cluster'].nunique()}")
    logger.info(f"Number of samples: {cluster_df['sample'].nunique()}")

    return cluster_df


def load_validation_data(validation_files: list) -> pd.DataFrame:
    """Load validation data from multiple CSV files."""
    logger = logging.getLogger(__name__)

    validation_data = []
    for file_path in validation_files:
        logger.info(f"Loading validation data from {file_path}")
        df = pd.read_csv(file_path)
        validation_data.append(df)

    combined_df = pd.concat(validation_data, ignore_index=True)
    logger.info(f"Loaded validation data for {len(combined_df)} samples")

    return combined_df


def prepare_features(cluster_df: pd.DataFrame, validation_df: pd.DataFrame) -> tuple:
    """Prepare feature matrix from cluster data."""
    logger = logging.getLogger(__name__)

    # Create sample-level cluster features
    logger.info("Creating sample-level cluster features...")

    # Count proteins per cluster per sample
    cluster_counts = (
        cluster_df.groupby(["sample", "cluster"]).size().reset_index(name="count")
    )

    # Pivot to create feature matrix (samples x clusters)
    feature_matrix = cluster_counts.pivot(
        index="sample", columns="cluster", values="count"
    )
    feature_matrix = feature_matrix.fillna(0)  # Fill missing clusters with 0

    logger.info(f"Feature matrix shape: {feature_matrix.shape}")

    # Match with validation data
    validation_df = validation_df.set_index("Accession")

    # Find common samples
    common_samples = set(feature_matrix.index) & set(validation_df.index)
    logger.info(
        f"Common samples between clusters and validation: {len(common_samples)}"
    )

    if len(common_samples) == 0:
        raise ValueError("No common samples found between cluster and validation data")

    # Filter to common samples
    X = feature_matrix.loc[list(common_samples)]
    y_data = validation_df.loc[list(common_samples)]

    # Create target variable (e.g., PASS/FAIL status)
    y = y_data["Status"]

    # Add additional features from validation data
    additional_features = [
        "metadata_completeness",
        "fungal_signal",
        "read_pairs",
        "host_contamination",
    ]
    for feature in additional_features:
        if feature in y_data.columns:
            X[feature] = y_data[feature]

    logger.info(f"Final feature matrix shape: {X.shape}")
    logger.info(f"Class distribution: {y.value_counts().to_dict()}")

    return X, y


def train_model(
    X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42
) -> dict:
    """Train and evaluate classification model."""
    logger = logging.getLogger(__name__)

    start_time = time.time()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Training set size: {len(X_train)}")
    logger.info(f"Test set size: {len(X_test)}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest model
    logger.info("Training Random Forest classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1,
    )

    rf_model.fit(X_train_scaled, y_train)

    # Evaluate model
    train_score = rf_model.score(X_train_scaled, y_train)
    test_score = rf_model.score(X_test_scaled, y_test)

    logger.info(f"Training accuracy: {train_score:.3f}")
    logger.info(f"Test accuracy: {test_score:.3f}")

    # Cross-validation
    cv_scores = cross_val_score(rf_model, X_train_scaled, y_train, cv=5)
    logger.info(
        f"Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})"
    )

    # Predictions and detailed evaluation
    y_pred = rf_model.predict(X_test_scaled)

    logger.info("\nClassification Report:")
    logger.info(f"\n{classification_report(y_test, y_pred)}")

    # Feature importance
    feature_importance = pd.DataFrame(
        {"feature": X.columns, "importance": rf_model.feature_importances_}
    ).sort_values("importance", ascending=False)

    logger.info("\nTop 10 Most Important Features:")
    for idx, row in feature_importance.head(10).iterrows():
        logger.info(f"  {row['feature']}: {row['importance']:.4f}")

    training_time = time.time() - start_time
    logger.info(f"\nModel training completed in {training_time:.2f} seconds")

    return {
        "model": rf_model,
        "scaler": scaler,
        "feature_names": list(X.columns),
        "train_score": train_score,
        "test_score": test_score,
        "cv_scores": cv_scores,
        "feature_importance": feature_importance,
        "training_time": training_time,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Train classification model from protein clusters"
    )
    parser.add_argument(
        "--clusters", required=True, help="Input CSV file with cluster assignments"
    )
    parser.add_argument(
        "--validation-data", nargs="+", required=True, help="Validation CSV files"
    )
    parser.add_argument(
        "--output", required=True, help="Output pickle file for trained model"
    )
    parser.add_argument(
        "--test-size", type=float, default=0.2, help="Test set size fraction"
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Random state for reproducibility"
    )
    parser.add_argument(
        "--threads", type=int, default=-1, help="Number of threads for model training"
    )

    args = parser.parse_args()
    logger = setup_logging()

    start_time = time.time()

    try:
        # Load data
        cluster_df = load_cluster_data(args.clusters)
        validation_df = load_validation_data(args.validation_data)

        # Prepare features
        X, y = prepare_features(cluster_df, validation_df)

        # Train model
        model_results = train_model(X, y, args.test_size, args.random_state)

        # Save model
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)

        with open(args.output, "wb") as f:
            pickle.dump(model_results, f)

        logger.info(f"Model saved to {args.output}")

        # Save feature importance
        importance_file = args.output.replace(".pkl", "_feature_importance.csv")
        model_results["feature_importance"].to_csv(importance_file, index=False)
        logger.info(f"Feature importance saved to {importance_file}")

    except Exception as e:
        logger.error(f"Error during model training: {e}")
        return 1

    total_time = time.time() - start_time
    logger.info(f"Model training pipeline completed in {total_time:.2f} seconds")

    return 0


if __name__ == "__main__":
    exit(main())

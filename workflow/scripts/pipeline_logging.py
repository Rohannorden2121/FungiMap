#!/usr/bin/env python3

import logging
import sys
from pathlib import Path


def setup_logger():
    """Configure logging for the pipeline."""
    logger = logging.getLogger("snakemake")
    logger.setLevel(logging.INFO)

    # Create log directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File handler
    fh = logging.FileHandler("logs/pipeline.log")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# Initialize logger
logger = setup_logger()

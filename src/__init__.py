"""
Source Machine Learning Operations Pipeline Package.
Provides core functions for data ingestion, clinical feature engineering, 
and model experimentation.
"""

from src.data_loader import fetch_uci_dataset
from src.feature_engineering import ClinicalFeatureBuilder, process_raw_data
from src.train import build_full_pipeline, execute_experimentation_suite

__all__ = [
    "fetch_uci_dataset",
    "ClinicalFeatureBuilder",
    "process_raw_data",
    "build_full_pipeline",
    "execute_experimentation_suite",
]
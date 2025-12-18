"""
Data processing package for GW Nashman Center website.
Provides utilities for data fetching, processing, and visualization.
"""

from .data_utils import DataProcessor, load_external_data
from .processors.metrics import MetricsProcessor
from .processors.geographic import GeographicProcessor

__all__ = [
    'DataProcessor',
    'load_external_data',
    'MetricsProcessor',
    'GeographicProcessor'
]

__version__ = '1.0.0'
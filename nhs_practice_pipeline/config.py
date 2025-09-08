#!/usr/bin/env python3
"""
NHS Practice Level Crosstabs Pipeline Configuration
===================================================

This module provides configuration management for the NHS practice level
appointment data analysis pipeline, including data source paths, processing
parameters, and output specifications.

The configuration follows NHS data processing standards and supports
flexible parameter adjustment for different analysis scenarios while
maintaining consistency with NHS reporting requirements.

Classes
-------
NHSPracticeAnalysisConfig
    Configuration class extending PipelineConfig with NHS-specific parameters

Notes
-----
Configuration parameters are organized into logical groups:
- Data source paths for raw, processed, and lookup data
- Analysis parameters including time periods and sample sizes
- Processing options for data quality and performance control
- Output specifications for reports, figures, and processed datasets

Examples
--------
>>> config = NHSPracticeAnalysisConfig()
>>> print(config.raw_data_dir)
'data/raw'
>>> config.sample_size = 50000  # Increase sample size
"""

from oops_its_a_pipeline import PipelineConfig


class NHSPracticeAnalysisConfig(PipelineConfig):
    """
    Configuration for NHS Practice Level Crosstabs analysis pipeline.

    This configuration class defines all parameters required for processing
    NHS practice level appointment data according to NHS standards and
    best practices for healthcare data analysis.

    Attributes
    ----------
    data_dir : str, default='data'
        Root directory for all data files and outputs.
    compressed_data_dir : str, default='data/compressed'
        Directory containing compressed data archives (zip files).
    raw_data_dir : str, default='data/raw'
        Directory for extracted CSV files with practice level crosstabs.
    processed_data_dir : str, default='data/processed'
        Directory for saving processed datasets and analysis outputs.
    lookup_data_dir : str, default='data/lookup'
        Directory containing mapping and reference data files.
    output_dir : str, default='data/processed'
        Primary output directory for analysis results and reports.
    figures_dir : str, default='figures'
        Directory for saving visualization outputs and charts.
    auto_extract_compressed : bool, default=True
        Whether to automatically extract compressed files before processing.
    compressed_file_pattern : str, default='*.zip'
        Glob pattern for finding compressed files to extract.
    csv_file_pattern : str, default='Practice_Level_Crosstab_*.csv'
        Glob pattern for finding CSV files to process.
    sample_size : int, default=10000
        Maximum number of rows to process from each source file for analysis.
    target_metrics : list
        List of key NHS performance metrics to calculate and report.

    Methods
    -------
    validate_paths()
        Validate that required data directories exist and are accessible.

    Notes
    -----
    The configuration supports both development and production environments
    through adjustable sample sizes and flexible path specifications.
    All paths use relative references to support portable deployments.

    For production analysis, increase sample_size or set to None for
    complete dataset processing. The default sample size enables rapid
    development and testing while maintaining analytical validity.

    The pipeline automatically discovers and extracts compressed data files,
    dynamically identifying available datasets rather than using hardcoded
    file lists for improved flexibility and maintainability.

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> config.sample_size = None  # Process complete datasets
    >>> config.csv_file_pattern = "*.csv"  # Change file pattern
    """

    data_dir: str = "data"
    compressed_data_dir: str = "data/compressed"
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    lookup_data_dir: str = "data/lookup"
    output_dir: str = "data/processed"
    figures_dir: str = "figures"

    # Dynamic file discovery settings
    auto_extract_compressed: bool = True
    compressed_file_pattern: str = "*.zip"
    csv_file_pattern: str = "Practice_Level_Crosstab_*.csv"

    sample_size: int = 10000

    target_metrics: list = [
        "total_appointments",
        "dna_rate",
        "completion_rate",
        "average_booking_time",
        "mode_distribution",
    ]

    # NHS performance targets
    target_dna_rate: float = 0.05  # Target: <5% did not attend rate
    target_completion_rate: float = 0.85  # Target: >85% completion rate

    # Output file configuration
    combined_data_filename: str = "combined_practice_data.csv"
    summary_stats_filename: str = "practice_summary_statistics.csv"
    monthly_summary_filename: str = "monthly_appointments_summary.csv"
    hcp_summary_filename: str = "hcp_type_summary.csv"
    mode_summary_filename: str = "appointment_mode_summary.csv"
    regional_summary_filename: str = "regional_summary.csv"
    booking_time_summary_filename: str = "booking_time_summary.csv"

    # Figure configuration
    figure_format: str = "png"
    figure_dpi: int = 300
    figure_bbox_inches: str = "tight"

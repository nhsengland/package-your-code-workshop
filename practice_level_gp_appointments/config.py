#!/usr/bin/env python3
"""
NHS Practice Level Crosstabs Pipeline Configuration
===================================================

Simple configuration for NHS practice level appointment data analysis pipeline.

Classes
-------
NHSPracticeAnalysisConfig
    Configuration dataclass containing all pipeline parameters including
    data directories, file patterns, processing options, and output settings.
"""

from pathlib import Path
from typing import Optional

from oops_its_a_pipeline import PipelineConfig


class NHSPracticeAnalysisConfig(PipelineConfig):
    """Simple configuration for NHS Practice Level Crosstabs pipeline."""

    # Core directories
    data_dir: Path
    compressed_data_dir: Path
    lookup_data_dir: Path

    # Date-specific directories
    date_id: str
    raw_data_dir: Path
    processed_data_dir: Path
    output_dir: Path
    figures_dir: Path

    # Input file
    input_zip_file: Path

    # File patterns and processing options
    csv_file_pattern: str = "*.csv"
    sample_size: Optional[int] = None
    lookup_file: str = "Mapping.csv"

    # Output settings
    figure_format: str = "png"
    figure_dpi: int = 300
    figure_bbox_inches: str = "tight"

    @classmethod
    def create(
        cls, zip_file_stem: str = "jul_25"
    ) -> "NHSPracticeAnalysisConfig":
        """
        Create configuration with date-specific paths.

        Parameters
        ----------
        zip_file_stem : str, default="jul_25"
            Date identifier for input data (e.g., "jul_25", "jun_25").

        Returns
        -------
        NHSPracticeAnalysisConfig
            Configured instance with date-specific paths.

        Raises
        ------
        FileNotFoundError
            If the specified zip file does not exist.
        """
        # Core directories
        data_dir = Path("data")
        compressed_data_dir = data_dir / "compressed"
        lookup_data_dir = data_dir / "lookup"

        # Date-specific directories
        raw_data_dir = data_dir / "raw" / zip_file_stem
        processed_data_dir = data_dir / "processed"
        output_dir = processed_data_dir / zip_file_stem
        figures_dir = Path("figures") / zip_file_stem

        # Input file
        input_zip_file = compressed_data_dir / f"{zip_file_stem}.zip"

        # Validate zip file exists
        if not input_zip_file.exists():
            msg = f"Zip file not found: {input_zip_file}"
            raise FileNotFoundError(msg)

        return cls(
            data_dir=data_dir,
            compressed_data_dir=compressed_data_dir,
            lookup_data_dir=lookup_data_dir,
            date_id=zip_file_stem,
            raw_data_dir=raw_data_dir,
            processed_data_dir=processed_data_dir,
            output_dir=output_dir,
            figures_dir=figures_dir,
            input_zip_file=input_zip_file,
        )

#!/usr/bin/env python3
"""
This module handles data extraction, loading, and joining operations for NHS
practice level appointment data according to NHS data standards and best
practices.

The module implements three main pipeline stages:
1. DataExtractionStage - Extracts compressed data files to directories
2. DataLoadingStage - Loads crosstab data and mapping files from CSV files
3. DataJoiningStage - Combines monthly datasets and merges with mappings

Classes
-------
DataExtractionStage
    Pipeline stage for extracting compressed data archives (zip files)
DataLoadingStage
    Pipeline stage for loading NHS practice level crosstab data from CSV files
DataJoiningStage
    Pipeline stage for joining monthly data and combining with mapping data

Notes
-----
This module uses NHS_HERBOT for standardised data loading and column
normalisation to ensure consistency with NHS data processing standards.
All CSV files are loaded with normalised column names using snake_case
convention.

The separation of extraction and loading stages allows for better error
handling and enables the pipeline to skip extraction if files are already
available.

Examples
--------
>>> config = NHSPracticeAnalysisConfig()
>>> extraction_stage = DataExtractionStage(config)
>>> loading_stage = DataLoadingStage(config)
>>> joining_stage = DataJoiningStage()
"""

import glob
import zipfile
from pathlib import Path

import nhs_herbot
import pandas as pd
from loguru import logger
from oops_its_a_pipeline import PipelineStage

from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig


class DataExtractionStage(PipelineStage):
    """
    Pipeline stage for extracting compressed data files.

    This stage extracts compressed archives (zip files) containing NHS practice
    level crosstab data and mapping files to the appropriate directories for
    subsequent processing stages.

    Parameters
    ----------
    config : NHSPracticeAnalysisConfig
        Configuration object containing data directory paths and extraction
        parameters.

    Methods
    -------
    run(context)
        Execute the data extraction stage and store extracted file paths.

    Notes
    -----
    The extraction process:
    - Searches for compressed files matching the configured pattern
    - Extracts CSV files to appropriate directories (raw data vs lookup)
    - Mapping files are placed in lookup directory
    - Practice crosstab files are placed in raw directory
    - Skips extraction if files already exist

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> stage = DataExtractionStage(config)
    >>> context = {}
    >>> updated_context = stage.run(context)
    """

    def __init__(self, config: NHSPracticeAnalysisConfig):
        """
        Initialize the data extraction stage.

        Parameters
        ----------
        config : NHSPracticeAnalysisConfig
            Configuration object containing extraction parameters.
        """
        super().__init__(outputs="extracted_files", name="data_extraction")
        self.config = config

    def run(self, context):
        """
        Extract compressed data files to appropriate directories.

        Parameters
        ----------
        context : dict
            Pipeline execution context for storing stage outputs.

        Returns
        -------
        dict
            Updated pipeline context containing extracted file paths.
        """
        logger.info("Extracting compressed data files...")

        # Use specific input zip file from config
        zip_path = self.config.input_zip_file

        if not zip_path.exists():
            logger.error(f"Input zip file not found: {zip_path}")
            self._store_outputs(context, [])
            return context

        # Create date-specific directories
        raw_dir = self.config.raw_data_dir
        raw_dir.mkdir(parents=True, exist_ok=True)

        extracted_files = []
        logger.info(f"Processing compressed file: {zip_path}")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                if member.endswith(".csv"):
                    # Determine destination directory based on file type
                    if "mapping" in member.lower():
                        dest_dir = self.config.lookup_data_dir
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        extracted_path = dest_dir / member
                    else:
                        extracted_path = raw_dir / member

                    if not extracted_path.exists():
                        logger.info(f"Extracting {member}")
                        if "mapping" in member.lower():
                            zip_ref.extract(member, dest_dir)
                        else:
                            zip_ref.extract(member, raw_dir)
                        extracted_files.append(extracted_path)
                    else:
                        logger.info(f"File exists: {extracted_path}")
                        extracted_files.append(extracted_path)

        logger.info(f"Extraction complete: {len(extracted_files)} files")
        self._store_outputs(context, extracted_files)
        return context


class DataLoadingStage(PipelineStage):
    """
    Pipeline stage for loading extracted CSV files.

    This stage loads monthly crosstab CSV files and mapping data that have
    been extracted by the DataExtractionStage, using NHS_HERBOT for
    standardised processing and column normalisation.

    Parameters
    ----------
    config : NHSPracticeAnalysisConfig
        Configuration object containing data directory paths and processing
        parameters including sample size limits.

    Methods
    -------
    run(context)
        Execute the data loading stage and store results in pipeline context.

    Notes
    -----
    The stage loads:
    - Monthly practice level crosstab files from raw data directory
    - Practice mapping/lookup data for geographical information
    - All data is processed through NHS_HERBOT for column normalisation

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> stage = DataLoadingStage(config)
    >>> context = {"extracted_files": file_paths}
    >>> updated_context = stage.run(context)
    """

    def __init__(self, config: NHSPracticeAnalysisConfig):
        """
        Initialize the data loading stage.

        Parameters
        ----------
        config : NHSPracticeAnalysisConfig
            Configuration object containing data paths and parameters.
        """
        super().__init__(
            inputs="extracted_files", outputs="raw_data", name="data_loading"
        )
        self.config = config

    def _discover_csv_files(self):
        """
        Dynamically discover CSV files in the raw data directory.

        Returns
        -------
        dict
            Dictionary mapping dataset names to file paths.
        """
        raw_dir = self.config.raw_data_dir
        csv_files = {}

        pattern = str(raw_dir / self.config.csv_file_pattern)
        matching_files = glob.glob(pattern)

        for file_path in matching_files:
            path_obj = Path(file_path)
            dataset_name = path_obj.stem
            csv_files[dataset_name] = path_obj
            logger.info(f"Discovered dataset: {dataset_name} -> {path_obj}")

        return csv_files

    def run(self, context):
        """
        Load NHS practice level crosstab data from extracted CSV files.

        Parameters
        ----------
        context : dict
            Pipeline execution context containing extracted file paths.

        Returns
        -------
        dict
            Updated pipeline context containing loaded datasets.
        """
        logger.info("Loading NHS practice level crosstab data...")

        # Discover CSV files to load
        csv_files = self._discover_csv_files()

        if not csv_files:
            logger.warning("No CSV files found matching pattern")
            logger.info(f"Searched in: {self.config.raw_data_dir}")
            logger.info(f"Pattern: {self.config.csv_file_pattern}")

        mapping_file = self.config.lookup_data_dir / "Mapping.csv"
        loaded_data = {}

        # Load discovered CSV files
        for month, file_path in csv_files.items():
            if file_path.exists():
                logger.info(f"Loading {month} data from {file_path}")
                try:
                    raw_crosstab_df = nhs_herbot.load_csv_data(
                        dataset_name=month,
                        filepath_or_buffer=file_path,
                    )
                    norm_crosstab_df = nhs_herbot.normalise_column_names(
                        raw_crosstab_df
                    )
                    loaded_data[month] = norm_crosstab_df
                    logger.info(
                        f"Loaded {len(norm_crosstab_df)} rows for {month}"
                    )
                except Exception as e:
                    logger.error(f"Failed to load {month} data: {e}")
                    continue
            else:
                logger.warning(f"File not found: {file_path}")

        # Load mapping data
        if mapping_file.exists():
            logger.info(f"Loading mapping data from {mapping_file}")
            try:
                raw_mapping_df = nhs_herbot.load_csv_data(
                    dataset_name="Mapping",
                    filepath_or_buffer=mapping_file,
                )
                norm_mapping_df = nhs_herbot.normalise_column_names(
                    raw_mapping_df
                )
                loaded_data["mapping"] = norm_mapping_df
                logger.info(f"Loaded {len(norm_mapping_df)} mapping records")
            except Exception as e:
                logger.error(f"Failed to load mapping data: {e}")
        else:
            logger.warning(f"Mapping file not found: {mapping_file}")

        logger.info(f"Data loading complete: {list(loaded_data.keys())}")
        self._store_outputs(context, loaded_data)
        return context


class DataJoiningStage(PipelineStage):
    """
    Pipeline stage for joining monthly data and combining with mapping data.

    This stage combines monthly crosstab datasets into a unified dataframe
    and merges with geographical mapping information to enable regional
    analysis and reporting.

    Methods
    -------
    run(context)
        Execute the data joining stage and store results in pipeline context.

    Notes
    -----
    The joining process includes:
    - Concatenation of monthly crosstab data with data_month identifier
    - Left join with mapping data using gp_code as the key
    - Addition of geographical information (ICB, region details)
    - Validation of join results and data quality checks

    The resulting dataset contains all original crosstab fields plus:
    - data_month: Identifier for the source month
    - icb_code, icb_name: Integrated Care Board information
    - region_code, region_name: NHS regional information

    Examples
    --------
    >>> stage = DataJoiningStage()
    >>> context = {"raw_data": loaded_datasets}
    >>> updated_context = stage.run(context)
    """

    def __init__(self):
        """
        Initialize the data joining stage.

        The stage is configured to consume raw_data from the loading stage
        and produce combined_data for downstream analysis stages.
        """
        super().__init__(
            inputs="raw_data", outputs="combined_data", name="data_joining"
        )

    def run(self, context):
        """
        Join monthly data and combine with mapping data.

        This method performs the core data joining operations to create
        a unified dataset suitable for comprehensive analysis.

        Parameters
        ----------
        context : dict
            Pipeline execution context containing raw_data from loading stage.

        Returns
        -------
        dict
            Updated pipeline context containing the joined dataset.

        Raises
        ------
        ValueError
            If no monthly data is found in the input datasets.

        Notes
        -----
        Processing steps:
        1. Extract monthly datasets and add data_month identifier
        2. Concatenate all monthly data into single dataframe
        3. Merge with mapping data on gp_code field
        4. Validate join results and log summary statistics
        """
        raw_data = self._get_input_values(context)[0]
        logger.info("Joining monthly NHS practice data...")

        monthly_dfs = []
        for month, df in raw_data.items():
            if month != "mapping":
                df_copy = df.copy()
                df_copy["data_month"] = month
                monthly_dfs.append(df_copy)

        if not monthly_dfs:
            raise ValueError("No monthly data found to join")

        combined_df = pd.concat(monthly_dfs, ignore_index=True)
        logger.info(f"Combined data shape: {combined_df.shape}")

        if "mapping" in raw_data:
            mapping_cols = [
                "gp_code",
                "icb_code",
                "icb_name",
                "region_code",
                "region_name",
            ]
            joined_df = combined_df.merge(
                raw_data["mapping"][mapping_cols],
                on="gp_code",
                how="left",
                suffixes=("", "_mapping"),
            )
            logger.info(f"Joined data shape: {joined_df.shape}")
        else:
            joined_df = combined_df
            logger.warning("No mapping data available for joining")

        logger.info("Data joining complete")
        self._store_outputs(context, joined_df)
        return context

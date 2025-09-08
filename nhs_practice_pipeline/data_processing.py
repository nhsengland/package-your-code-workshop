#!/usr/bin/env python3
"""
NHS Practice Level Data Processing Module
=========================================

This module handles data loading, cleaning, and joining operations for NHS
practice level appointment data according to NHS data standards and best practices.

The module implements two main pipeline stages:
1. DataLoadingStage - Loads crosstab data and mapping files from CSV sources
2. DataJoiningStage - Combines monthly datasets and merges with geographical mappings

Classes
-------
DataLoadingStage
    Pipeline stage for loading NHS practice level crosstab data from CSV files
DataJoiningStage
    Pipeline stage for joining monthly data and combining with mapping information

Notes
-----
This module uses NHS_HERBOT for standardized data loading and column normalization
to ensure consistency with NHS data processing standards. All CSV files are loaded
with normalized column names using snake_case convention.

Examples
--------
>>> config = NHSPracticeAnalysisConfig()
>>> loading_stage = DataLoadingStage(config)
>>> joining_stage = DataJoiningStage()
"""

from pathlib import Path
import pandas as pd
import nhs_herbot
from loguru import logger
from oops_its_a_pipeline import PipelineStage

from nhs_practice_pipeline.config import NHSPracticeAnalysisConfig


class DataLoadingStage(PipelineStage):
    """
    Pipeline stage for loading NHS practice level crosstab data.

    This stage loads monthly crosstab CSV files and mapping data from the
    configured data directories using NHS_HERBOT for standardized processing.

    Parameters
    ----------
    config : NHSPracticeAnalysisConfig
        Configuration object containing data directory paths and processing
        parameters including sample size limits.

    Attributes
    ----------
    config : NHSPracticeAnalysisConfig
        The configuration object passed during initialization.

    Methods
    -------
    run(context)
        Execute the data loading stage and store results in pipeline context.

    Notes
    -----
    The stage loads the following data:
    - Monthly practice level crosstab files (May, June, July 2025)
    - Practice mapping/lookup data for geographical information
    - All data is processed through NHS_HERBOT for column normalization

    Data files are expected in the following locations:
    - Raw data: {config.raw_data_dir}/Practice_Level_Crosstab_*.csv
    - Mapping data: {config.lookup_data_dir}/Mapping.csv

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> stage = DataLoadingStage(config)
    >>> context = {}
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
        super().__init__(outputs="raw_data", name="data_loading")
        self.config = config

    def run(self, context):
        """
        Load NHS practice level crosstab data from CSV files.

        This method loads monthly crosstab data and mapping files using
        NHS_HERBOT for standardized data processing and column normalization.

        Parameters
        ----------
        context : dict
            Pipeline execution context for storing stage outputs.

        Returns
        -------
        dict
            Updated pipeline context containing loaded datasets.

        Notes
        -----
        Loaded data includes:
        - Monthly crosstab data with normalized column names
        - Practice mapping data for geographical analysis
        - Error handling for missing files with appropriate warnings
        """
        logger.info("Loading NHS practice level crosstab data...")

        raw_dir = Path(self.config.raw_data_dir)
        csv_files = {
            "Practice_Level_Crosstab_May_25": (
                raw_dir / "Practice_Level_Crosstab_May_25.csv"
            ),
            "Practice_Level_Crosstab_Jun_25": (
                raw_dir / "Practice_Level_Crosstab_Jun_25.csv"
            ),
            "Practice_Level_Crosstab_Jul_25": (
                raw_dir / "Practice_Level_Crosstab_Jul_25.csv"
            ),
        }

        mapping_file = Path(self.config.lookup_data_dir) / "Mapping.csv"
        loaded_data = {}

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
                    logger.info(f"Loaded {len(norm_crosstab_df)} rows for {month}")
                except Exception as e:
                    logger.error(f"Failed to load {month} data: {e}")
                    continue
            else:
                logger.warning(f"File not found: {file_path}")

        if mapping_file.exists():
            logger.info(f"Loading mapping data from {mapping_file}")
            try:
                raw_mapping_df = nhs_herbot.load_csv_data(
                    dataset_name="Mapping",
                    filepath_or_buffer=mapping_file,
                )
                norm_mapping_df = nhs_herbot.normalise_column_names(raw_mapping_df)
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

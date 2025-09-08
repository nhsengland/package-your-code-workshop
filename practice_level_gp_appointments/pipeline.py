#!/usr/bin/env python3
"""
NHS Practice Level Crosstabs Analysis Pipeline
==============================================

This module implements the main pipeline orchestration for NHS practice level
appointment data analysis using the oops-its-a-pipeline framework.

The pipeline processes NHS practice level crosstab data through five stages:
1. Data loading from CSV files
2. Data joining and combination
3. Statistical summarisation
4. Data visualization and graphing
5. Output generation and reporting

Classes
-------
NHSPracticeAnalysisPipeline
    Main pipeline class that orchestrates the complete analysis workflow

Notes
-----
This module uses the oops-its-a-pipeline framework for stage management
and execution. Each stage is implemented as a separate PipelineStage class
with defined inputs and outputs.

Examples
--------
>>> config = NHSPracticeAnalysisConfig()
>>> pipeline = NHSPracticeAnalysisPipeline(config)
>>> exit_code = pipeline.run_analysis()
"""

from datetime import datetime

from loguru import logger
from oops_its_a_pipeline import Pipeline

from practice_level_gp_appointments.analytics import SummarisationStage
from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig
from practice_level_gp_appointments.data_processing import (
    DataExtractionStage,
    DataJoiningStage,
    DataLoadingStage,
)
from practice_level_gp_appointments.output import OutputStage
from practice_level_gp_appointments.visualization import GraphingStage

logger.level("START", no=25, color="<blue>")


class NHSPracticeAnalysisPipeline(Pipeline):
    """
    NHS Practice Level Crosstabs Analysis Pipeline.

    This pipeline processes NHS practice level appointment data through five
    sequential stages to produce comprehensive analysis outputs including
    summary statistics, visualizations, and reports.

    Parameters
    ----------
    config : NHSPracticeAnalysisConfig
        Configuration object containing data paths, processing parameters,
        and output specifications.

    Attributes
    ----------
    config : NHSPracticeAnalysisConfig
        The configuration object passed during initialisation.

    Methods
    -------
    run_analysis()
        Execute the complete pipeline and return exit code.

    Notes
    -----
    The pipeline stages are:
    1. Data Loading Stage - Load CSV files from raw data directory
    2. Data Joining Phase - Combine monthly data with mapping information
    3. Summarisation Stage - Generate statistical summaries and metrics
    4. Graphing Stage - Create visualizations and charts
    5. Output Stage - Save processed data, figures, and reports

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> pipeline = NHSPracticeAnalysisPipeline(config)
    >>> exit_code = pipeline.run_analysis()
    >>> print(f"Pipeline completed with exit code: {exit_code}")
    """

    def __init__(self, config: NHSPracticeAnalysisConfig):
        """
        Initialize the NHS Practice Analysis Pipeline.

        Parameters
        ----------
        config : NHSPracticeAnalysisConfig
            Configuration object containing all pipeline parameters.
        """
        stages = [
            DataExtractionStage(config),
            DataLoadingStage(config),
            DataJoiningStage(),
            SummarisationStage(config),
            GraphingStage(config),
            OutputStage(config),
        ]
        super().__init__(config, stages)

    def run_analysis(self):
        """
        Run the complete NHS practice level analysis pipeline.

        This method orchestrates the execution of all pipeline stages,
        handles validation, error management, and logging.

        Returns
        -------
        int
            Exit code: 0 for success, 1 for failure.

        Raises
        ------
        Exception
            Any unhandled exception during pipeline execution will be
            caught and logged, returning exit code 1.

        Notes
        -----
        The method performs the following operations:
        - Validates pipeline configuration and stages
        - Generates unique run identifier with timestamp
        - Executes all pipeline stages in sequence
        - Handles errors and provides appropriate logging
        """
        logger.log("START", "NHS Practice Level Crosstabs Analysis Pipeline")

        try:
            self.validate()
            logger.success("Pipeline validation successful")
        except Exception as e:
            logger.error(f"Pipeline validation failed: {e}")
            return 1

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            run_id = f"nhs_practice_analysis_{timestamp}"
            self.run(run_id)
            return 0
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return 1

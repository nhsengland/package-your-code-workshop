"""
NHS Practice Level Crosstabs Analysis Pipeline - Main Entry Point
=================================================================

This module provides the main entry point for executing the NHS practice level
appointment data analysis pipeline. It handles initialization, execution
coordination, and error management for the complete analytical workflow.

The module can be executed directly as a script or imported and called
programmatically, supporting both command-line usage and integration
into larger data processing systems.

Functions
---------
main()
    Initialize and execute the complete NHS practice analysis pipeline

Notes
-----
The main function orchestrates the following operations:
- Configuration initialization with NHS-specific parameters
- Pipeline creation and stage setup
- Complete workflow execution with error handling
- Result validation and success/failure reporting

Exit codes follow standard conventions:
- 0: Successful completion
- 1: Error during execution

Examples
--------
Command line execution:
    $ python -m nhs_practice_pipeline

Programmatic usage:
    >>> from nhs_practice_pipeline.__main__ import main
    >>> exit_code = main()
    >>> print(f"Pipeline completed with code: {exit_code}")
"""

import sys
from loguru import logger

from nhs_practice_pipeline.config import NHSPracticeAnalysisConfig
from nhs_practice_pipeline.pipeline import NHSPracticeAnalysisPipeline


def main():
    """
    Main entry point for the NHS practice pipeline.

    This function initializes the pipeline configuration, creates the
    pipeline instance, and executes the complete analysis workflow
    with comprehensive error handling and logging.

    Returns
    -------
    int
        Exit code: 0 for successful completion, 1 for errors.

    Raises
    ------
    Exception
        Any unhandled exceptions during pipeline execution are caught
        and logged appropriately before returning error exit code.

    Notes
    -----
    The function performs the following operations:
    1. Initialize NHS-specific configuration parameters
    2. Create pipeline instance with all required stages
    3. Execute complete analysis workflow
    4. Handle errors and provide appropriate user feedback
    5. Return standardized exit codes for process monitoring

    All stages of the pipeline are executed in sequence with validation
    and error checking at each step to ensure data quality and process
    reliability.
    """
    try:
        config = NHSPracticeAnalysisConfig()
        pipeline = NHSPracticeAnalysisPipeline(config)
        pipeline.run_analysis()
        logger.success("Pipeline completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

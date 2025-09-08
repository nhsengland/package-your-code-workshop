"""
NHS Practice Level Crosstabs Analysis Pipeline Entry Point.

This module serves as the main entry point for the NHS Practice Level Crosstabs
analysis pipeline. It provides command-line interface functionality and
orchestrates the execution of the complete analysis workflow.

The module handles:
- Command-line argument parsing for pipeline configuration
- Pipeline initialization and execution
- Error handling and logging
- Exit code management for integration with external systems

Functions
---------
practice_level_gp_appointments_main : function
    Core pipeline execution function that configures and runs the analysis.
main : function
    CLI entry point that handles argument parsing and delegates to the main
    pipeline function.

Examples
--------
Run the pipeline with default settings:
    $ python -m practice_level_gp_appointments

Run the pipeline with custom date identifier:
    $ python -m practice_level_gp_appointments --zip-file-stem "aug_25"

Notes
-----
This module is designed to be executed as a script or imported for
programmatic use.
The pipeline configuration is based on date identifiers for data selection.
"""

import argparse
import sys

from loguru import logger

from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig
from practice_level_gp_appointments.pipeline import NHSPracticeAnalysisPipeline


def practice_level_gp_appointments_main(zip_file_stem: str = "jul_25"):
    """
    Run the NHS Practice Level Crosstabs analysis pipeline.

    Parameters
    ----------
    zip_file_stem : str, default="jul_25"
        Date identifier for input data (e.g., "jul_25", "jun_25").
        Future: This will be configurable via CLI arguments.
    """
    try:
        # Configure pipeline
        config = NHSPracticeAnalysisConfig.create(zip_file_stem)
        pipeline = NHSPracticeAnalysisPipeline(config)

        # Execute analysis
        exit_code = pipeline.run_analysis()

        if exit_code == 0:
            logger.success("Pipeline completed successfully")
        else:
            logger.error("Pipeline failed")

        return exit_code

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        return 1


def main():
    """
    Main entry point for NHS Practice Level Crosstabs analysis pipeline.

    Future: This will handle CLI arguments for pipeline selection and
    configuration overrides.
    """
    parser = argparse.ArgumentParser(
        description="NHS Practice Level Crosstabs Analysis Pipeline"
    )
    parser.add_argument(
        "--zip-file-stem",
        default="jul_25",
        help="Date identifier for input data (e.g., 'jul_25', 'jun_25')",
    )

    args = parser.parse_args()
    zip_file_stem = args.zip_file_stem
    return practice_level_gp_appointments_main(zip_file_stem)


if __name__ == "__main__":
    sys.exit(main())

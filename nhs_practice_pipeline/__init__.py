#!/usr/bin/env python3
"""
NHS Practice Pipeline Package

A comprehensive NHS practice level crosstabs data processing pipeline
built with the oops-its-a-pipeline framework.
"""

__version__ = "0.1.0"
__author__ = "NHS Practice Analysis Team"

# Make key classes available at package level
from nhs_practice_pipeline.config import NHSPracticeAnalysisConfig
from nhs_practice_pipeline.data_processing import (
    DataLoadingStage,
    DataJoiningStage,
)
from nhs_practice_pipeline.analytics import SummarisationStage
from nhs_practice_pipeline.visualization import GraphingStage
from nhs_practice_pipeline.output import OutputStage
from nhs_practice_pipeline.pipeline import NHSPracticeAnalysisPipeline

__all__ = [
    "NHSPracticeAnalysisConfig",
    "DataLoadingStage",
    "DataJoiningStage",
    "SummarisationStage",
    "GraphingStage",
    "OutputStage",
    "NHSPracticeAnalysisPipeline",
]

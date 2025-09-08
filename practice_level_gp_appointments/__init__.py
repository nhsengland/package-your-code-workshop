#!/usr/bin/env python3
"""
NHS Practice Pipeline Package

A comprehensive NHS practice level crosstabs data processing pipeline
built with the oops-its-a-pipeline framework.
"""

__version__ = "0.1.0"
__author__ = "NHS Practice Analysis Team"

# Make key classes available at package level
from practice_level_gp_appointments.analytics import SummarisationStage
from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig
from practice_level_gp_appointments.data_processing import (
    DataJoiningStage,
    DataLoadingStage,
)
from practice_level_gp_appointments.output import OutputStage
from practice_level_gp_appointments.pipeline import NHSPracticeAnalysisPipeline
from practice_level_gp_appointments.visualization import GraphingStage

__all__ = [
    "NHSPracticeAnalysisConfig",
    "DataLoadingStage",
    "DataJoiningStage",
    "SummarisationStage",
    "GraphingStage",
    "OutputStage",
    "NHSPracticeAnalysisPipeline",
]

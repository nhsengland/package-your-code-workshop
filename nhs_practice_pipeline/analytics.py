#!/usr/bin/env python3
"""
NHS Practice Level Analytics Module
===================================

This module calculates NHS performance metrics and creates comprehensive
summary statistics for practice level appointment data analysis.

The module implements statistical analysis and metric calculation including:
- Temporal analysis of appointment patterns by month and status
- Healthcare professional (HCP) type distribution analysis
- Appointment mode analysis (face-to-face, telephone, online)
- Regional and geographical performance comparisons
- Booking time analysis and access metrics
- Key NHS performance indicators (DNA rates, completion rates)

Classes
-------
SummarisationStage
    Pipeline stage for creating descriptive statistics and summary tables

Notes
-----
All metrics are calculated according to NHS performance monitoring standards
and include appropriate statistical measures (sum, mean, count) for different
data types. The module generates both detailed breakdowns and high-level
key performance indicators suitable for NHS reporting requirements.

Examples
--------
>>> config = NHSPracticeAnalysisConfig()
>>> stage = SummarisationStage(config)
>>> context = {"combined_data": joined_dataframe}
>>> results = stage.run(context)
"""

import pandas as pd
from loguru import logger
from oops_its_a_pipeline import PipelineStage

from nhs_practice_pipeline.config import NHSPracticeAnalysisConfig


class SummarisationStage(PipelineStage):
    """
    Pipeline stage for creating descriptive statistics and summary tables.

    This stage processes the combined appointment data to generate comprehensive
    statistical summaries and NHS performance metrics suitable for analysis
    and reporting purposes.

    Parameters
    ----------
    config : NHSPracticeAnalysisConfig
        Configuration object containing analysis parameters and specifications.

    Attributes
    ----------
    config : NHSPracticeAnalysisConfig
        The configuration object passed during initialisation.

    Methods
    -------
    run(context)
        Execute the summarisation stage and generate statistical summaries.

    Notes
    -----
    Generated summaries include:
    - Monthly appointment trends by status (attended, DNA, cancelled)
    - Healthcare professional type distribution and workload analysis
    - Appointment mode analysis (face-to-face, telephone, online)
    - Regional performance comparisons and geographical analysis
    - Booking time analysis and access pattern evaluation
    - Key NHS performance indicators and completion rates

    All metrics follow NHS performance monitoring standards and include
    appropriate statistical measures for different analytical purposes.

    Examples
    --------
    >>> config = NHSPracticeAnalysisConfig()
    >>> stage = SummarisationStage(config)
    >>> context = {"combined_data": dataframe}
    >>> results = stage.run(context)
    """

    def __init__(self, config: NHSPracticeAnalysisConfig):
        """
        Initialize the summarisation stage.

        Parameters
        ----------
        config : NHSPracticeAnalysisConfig
            Configuration object containing analysis parameters.
        """
        super().__init__(
            inputs="combined_data", outputs="summary_statistics", name="summarisation"
        )
        self.config = config

    def run(self, context):
        """
        Create descriptive statistics and summary tables.

        This method processes the combined appointment data to generate
        multiple summary tables and key performance indicators for NHS
        practice level analysis.

        Parameters
        ----------
        context : dict
            Pipeline execution context containing combined appointment data.

        Returns
        -------
        dict
            Updated pipeline context containing summary statistics and metrics.

        Notes
        -----
        The method generates seven main summary categories:
        1. Monthly trends by appointment status
        2. Healthcare professional type analysis
        3. Appointment mode temporal analysis
        4. Regional performance summaries
        5. Booking time access analysis
        6. Overall descriptive statistics
        7. Key NHS performance metrics (DNA rates, completion rates)
        """
        combined_data = self._get_input_values(context)[0]
        logger.info("Creating summary statistics...")

        df = combined_data
        summaries = {}

        monthly_summary = (
            df.groupby(["data_month", "appt_status"])["count_of_appointments"]
            .sum()
            .reset_index()
        )
        summaries["monthly_by_status"] = monthly_summary

        hcp_summary = (
            df.groupby("hcp_type")["count_of_appointments"]
            .agg(["sum", "mean", "count"])
            .reset_index()
        )
        hcp_summary.columns = [
            "hcp_type",
            "total_appointments",
            "mean_appointments",
            "number_of_records",
        ]
        summaries["hcp_type_summary"] = hcp_summary

        mode_summary = (
            df.groupby(["appt_mode", "data_month"])["count_of_appointments"]
            .sum()
            .reset_index()
        )
        summaries["mode_by_month"] = mode_summary

        if "region_name" in df.columns:
            regional_summary = (
                df.groupby("region_name")["count_of_appointments"]
                .agg(["sum", "mean"])
                .reset_index()
            )
            regional_summary.columns = [
                "region_name",
                "total_appointments",
                "mean_appointments",
            ]
            summaries["regional_summary"] = regional_summary

        booking_time_summary = (
            df.groupby("time_between_book_and_appt")["count_of_appointments"]
            .sum()
            .reset_index()
        )
        summaries["booking_time_summary"] = booking_time_summary

        numeric_cols = ["count_of_appointments"]
        desc_stats = df[numeric_cols].describe()
        summaries["descriptive_stats"] = desc_stats

        total_appointments = df["count_of_appointments"].sum()

        if "appt_status" in df.columns:
            dna_appointments = df[df["appt_status"] == "DNA"][
                "count_of_appointments"
            ].sum()
            attended_appointments = df[df["appt_status"] == "Attended"][
                "count_of_appointments"
            ].sum()
            dna_rate = (
                dna_appointments / total_appointments if total_appointments > 0 else 0
            )
            completion_rate = (
                attended_appointments / total_appointments
                if total_appointments > 0
                else 0
            )

            metrics_summary = pd.DataFrame(
                {
                    "metric": [
                        "total_appointments",
                        "dna_rate",
                        "completion_rate",
                        "dna_count",
                        "attended_count",
                    ],
                    "value": [
                        total_appointments,
                        dna_rate,
                        completion_rate,
                        dna_appointments,
                        attended_appointments,
                    ],
                }
            )
            summaries["key_metrics"] = metrics_summary

        logger.info(f"Created {len(summaries)} summary tables")
        self._store_outputs(context, summaries)
        return context

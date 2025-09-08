"""
NHS Practice Level Visualization Module
=======================================

This module creates graphs and visualizations for NHS practice level
appointment data analysis.

Classes
-------
SummarisationStage
    Pipeline stage for creating summary statistics and aggregated data views
GraphingStage
    Pipeline stage for generating visualizations including heatmaps,
    time series, and distribution plots using matplotlib and seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from oops_its_a_pipeline import PipelineStage

from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig


class GraphingStage(PipelineStage):
    """Stage for creating visualizations and graphs."""

    def __init__(self, config: NHSPracticeAnalysisConfig):
        super().__init__(
            inputs="summary_statistics", outputs="figures", name="graphing"
        )
        self.config = config

    def run(self, context):
        """Create visualizations and graphs."""
        summary_stats = self._get_input_values(context)[0]
        logger.info("Creating visualizations...")

        # Set up matplotlib style for NHS branding
        plt.style.use("default")
        sns.set_palette("husl")

        figures = {}

        # Figure 1: Monthly appointments by status
        if "monthly_by_status" in summary_stats:
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            monthly_pivot = (
                summary_stats["monthly_by_status"]
                .pivot(
                    index="data_month",
                    columns="appt_status",
                    values="count_of_appointments",
                )
                .fillna(0)
            )
            monthly_pivot.plot(kind="bar", ax=ax1, stacked=True)
            ax1.set_title(
                "Monthly Appointments by Status",
                fontsize=14,
                fontweight="bold",
            )
            ax1.set_xlabel("Month")
            ax1.set_ylabel("Number of Appointments")
            ax1.legend(
                title="Appointment Status",
                bbox_to_anchor=(1.05, 1),
                loc="upper left",
            )
            plt.xticks(rotation=45)
            plt.tight_layout()
            figures["monthly_appointments_by_status"] = fig1

        # Figure 2: HCP Type Distribution
        if "hcp_type_summary" in summary_stats:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            hcp_data = summary_stats["hcp_type_summary"].head(10)
            sns.barplot(
                data=hcp_data, x="total_appointments", y="hcp_type", ax=ax2
            )
            ax2.set_title(
                "Total Appointments by Healthcare Professional Type",
                fontsize=14,
                fontweight="bold",
            )
            ax2.set_xlabel("Total Appointments")
            ax2.set_ylabel("HCP Type")
            plt.tight_layout()
            figures["hcp_type_distribution"] = fig2

        # Figure 3: Appointment Mode Trends
        if "mode_by_month" in summary_stats:
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            mode_pivot = (
                summary_stats["mode_by_month"]
                .pivot(
                    index="data_month",
                    columns="appt_mode",
                    values="count_of_appointments",
                )
                .fillna(0)
            )
            mode_pivot.plot(kind="line", ax=ax3, marker="o")
            ax3.set_title(
                "Appointment Mode Trends Across Months",
                fontsize=14,
                fontweight="bold",
            )
            ax3.set_xlabel("Month")
            ax3.set_ylabel("Number of Appointments")
            ax3.legend(
                title="Appointment Mode",
                bbox_to_anchor=(1.05, 1),
                loc="upper left",
            )
            plt.xticks(rotation=45)
            plt.tight_layout()
            figures["appointment_mode_trends"] = fig3

        # Figure 4: Regional Distribution (if available)
        if "regional_summary" in summary_stats:
            fig4, ax4 = plt.subplots(figsize=(12, 8))
            regional_data = summary_stats["regional_summary"]
            sns.barplot(
                data=regional_data,
                x="total_appointments",
                y="region_name",
                ax=ax4,
            )
            ax4.set_title(
                "Total Appointments by Region", fontsize=14, fontweight="bold"
            )
            ax4.set_xlabel("Total Appointments")
            ax4.set_ylabel("Region")
            plt.tight_layout()
            figures["regional_distribution"] = fig4

        # Figure 5: Booking Time Analysis
        if "booking_time_summary" in summary_stats:
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            booking_data = summary_stats["booking_time_summary"]
            sns.barplot(
                data=booking_data,
                x="time_between_book_and_appt",
                y="count_of_appointments",
                ax=ax5,
            )
            ax5.set_title(
                "Appointments by Time Between Booking and Appointment",
                fontsize=14,
                fontweight="bold",
            )
            ax5.set_xlabel("Time Between Booking and Appointment")
            ax5.set_ylabel("Number of Appointments")
            plt.xticks(rotation=45)
            plt.tight_layout()
            figures["booking_time_analysis"] = fig5

        logger.info(f"Created {len(figures)} visualizations")
        self._store_outputs(context, figures)
        return context

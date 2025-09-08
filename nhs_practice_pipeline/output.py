#!/usr/bin/env python3
"""
NHS Practice Level Output Module

This module handles saving outputs including CSV files, figures, and reports.
"""

import json
from pathlib import Path
from loguru import logger
from oops_its_a_pipeline import PipelineStage

from nhs_practice_pipeline.config import NHSPracticeAnalysisConfig


class OutputStage(PipelineStage):
    """Stage for saving outputs (tables, figures, reports)."""

    def __init__(self, config: NHSPracticeAnalysisConfig):
        super().__init__(
            inputs=("combined_data", "summary_statistics", "figures"),
            outputs="output_files",
            name="output",
        )
        self.config = config

    def run(self, context):
        """Save outputs (tables, figures, reports)."""
        combined_data, summary_stats, figures = self._get_input_values(context)
        logger.info("Saving outputs...")

        # Create output directories
        processed_dir = Path(self.config.processed_data_dir)
        figures_dir = Path(self.config.figures_dir)
        processed_dir.mkdir(exist_ok=True)
        figures_dir.mkdir(exist_ok=True)

        outputs = {}

        # Save combined data
        combined_data_path = processed_dir / self.config.combined_data_filename
        combined_data.to_csv(combined_data_path, index=False)
        outputs["combined_data"] = str(combined_data_path)
        logger.info(f"Saved combined data: {combined_data_path}")

        # Save summary statistics
        for name, summary_df in summary_stats.items():
            if hasattr(summary_df, "to_csv"):  # Check if it's a DataFrame
                if name == "monthly_by_status":
                    filename = self.config.monthly_summary_filename
                elif name == "hcp_type_summary":
                    filename = self.config.hcp_summary_filename
                elif name == "mode_by_month":
                    filename = self.config.mode_summary_filename
                elif name == "regional_summary":
                    filename = self.config.regional_summary_filename
                elif name == "booking_time_summary":
                    filename = self.config.booking_time_summary_filename
                else:
                    filename = f"{name}.csv"

                output_path = processed_dir / filename
                summary_df.to_csv(output_path, index=False)
                outputs[f"summary_{name}"] = str(output_path)
                logger.info(f"Saved {name}: {output_path}")

        # Save figures
        for fig_name, fig in figures.items():
            output_path = figures_dir / f"{fig_name}.{self.config.figure_format}"
            fig.savefig(
                output_path,
                dpi=self.config.figure_dpi,
                bbox_inches=self.config.figure_bbox_inches,
            )
            outputs[f"figure_{fig_name}"] = str(output_path)
            logger.info(f"Saved figure: {output_path}")

        # Create a summary report
        report_path = processed_dir / "pipeline_report.txt"
        with open(report_path, "w") as f:
            f.write("NHS Practice Level Crosstabs Pipeline Report\n")
            f.write("=" * 50 + "\n\n")

            f.write("Data Summary:\n")
            f.write(f"- Total records processed: {len(combined_data):,}\n")
            f.write(f"- Data months: {combined_data['data_month'].unique()}\n")
            f.write(
                f"- Number of unique GP practices: {combined_data['gp_code'].nunique()}\n"
            )
            f.write(
                f"- Total appointments: {combined_data['count_of_appointments'].sum():,}\n\n"
            )

            f.write("Summary Tables Created:\n")
            for output_name in outputs.keys():
                if output_name.startswith("summary_"):
                    f.write(f"- {outputs[output_name]}\n")

            f.write("\nVisualizations Created:\n")
            for output_name in outputs.keys():
                if output_name.startswith("figure_"):
                    f.write(f"- {outputs[output_name]}\n")

        outputs["report"] = str(report_path)
        logger.info(f"Saved report: {report_path}")

        logger.info(f"Output stage complete: Saved {len(outputs)} outputs")
        self._store_outputs(context, outputs)
        return context

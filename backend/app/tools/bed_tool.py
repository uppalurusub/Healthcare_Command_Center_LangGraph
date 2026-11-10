"""
bed_tool.py

Healthcare Command Center AI

Bed Management Tool

Responsibilities
----------------
• Fetch bed occupancy
• ICU bed availability
• Isolation beds
• General beds
• Bed turnover
• Predict bed availability
"""

from datetime import datetime
from typing import Dict, Any

from langchain_core.tools import tool
from app.config.settings import settings
logger = settings.get_logger()


class BedManagementTool:

    def __init__(self):
        logger.info("Initializing Bed Management Tool")

    # ==========================================================
    # Fetch Bed Statistics
    # ==========================================================

    def get_bed_statistics(
        self,
        hospital_id: str
    ) -> Dict[str, Any]:

        logger.info(
            "Fetching Bed Statistics | Hospital={}",
            hospital_id
        )

        try:

            # --------------------------------------------------
            # Replace with Database/API Implementation
            # --------------------------------------------------

            result = {

                "hospital_id": hospital_id,

                "date": datetime.now().strftime("%Y-%m-%d"),

                "total_beds": 500,

                "occupied_beds": 432,

                "available_beds": 68,

                "icu_beds": 50,

                "icu_occupied": 44,

                "icu_available": 6,

                "general_beds": 400,

                "general_occupied": 345,

                "general_available": 55,

                "isolation_beds": 50,

                "isolation_occupied": 43,

                "isolation_available": 7,

                "expected_discharges_today": 31,

                "bed_turnover_rate": 2.8
            }

            logger.success(
                "Bed statistics retrieved successfully."
            )

            return result

        except Exception:

            logger.exception(
                "Failed to retrieve bed statistics."
            )

            raise

    # ==========================================================
    # Calculate KPIs
    # ==========================================================

    def calculate_bed_kpis(
        self,
        bed_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Calculating Bed KPIs")

        try:

            total = bed_data["total_beds"]

            occupied = bed_data["occupied_beds"]

            available = bed_data["available_beds"]

            icu_total = bed_data["icu_beds"]

            icu_available = bed_data["icu_available"]

            occupancy_rate = round(
                (occupied / total) * 100,
                2
            )

            availability_rate = round(
                (available / total) * 100,
                2
            )

            icu_utilization = round(
                ((icu_total - icu_available) / icu_total) * 100,
                2
            )

            pressure_level = "LOW"

            if occupancy_rate >= 90:
                pressure_level = "CRITICAL"
            elif occupancy_rate >= 80:
                pressure_level = "HIGH"
            elif occupancy_rate >= 70:
                pressure_level = "MEDIUM"

            kpis = {

                "occupancy_rate": occupancy_rate,

                "availability_rate": availability_rate,

                "icu_utilization": icu_utilization,

                "pressure_level": pressure_level
            }

            logger.success(
                "Bed KPIs calculated successfully."
            )

            return kpis

        except Exception:

            logger.exception(
                "Bed KPI calculation failed."
            )

            raise


# ==========================================================
# LangChain Tool
# ==========================================================

@tool
def bed_management_tool(
    hospital_id: str
) -> Dict[str, Any]:
    """
    Retrieve bed management statistics and KPIs.

    Args:
        hospital_id: Hospital Identifier

    Returns:
        Bed statistics and KPIs.
    """

    logger.info(
        "Executing Bed Management Tool | Hospital={}",
        hospital_id
    )

    tool_service = BedManagementTool()

    statistics = tool_service.get_bed_statistics(
        hospital_id
    )

    kpis = tool_service.calculate_bed_kpis(
        statistics
    )

    response = {

        "statistics": statistics,

        "kpis": kpis
    }

    logger.success(
        "Bed Management Tool execution completed."
    )

    return response
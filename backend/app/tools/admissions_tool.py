"""
admissions_tool.py

Healthcare Command Center AI

Admissions Tool

Responsibilities
----------------
• Fetch today's admissions
• Emergency admissions
• Scheduled admissions
• Waiting patients
• Predict next 24 hours
"""

from datetime import datetime
from typing import Dict, Any

from langchain_core.tools import tool
from app.config.settings import settings
logger = settings.get_logger()


class AdmissionsTool:

    def __init__(self):

        logger.info("Initializing Admissions Tool")

    def get_admission_statistics(
        self,
        hospital_id: str
    ) -> Dict[str, Any]:

        logger.info(
            "Fetching admission statistics | Hospital={}",
            hospital_id
        )

        try:

            # ----------------------------------------
            # Replace with actual DB/API implementation
            # ----------------------------------------

            result = {

                "hospital_id": hospital_id,

                "date": datetime.now().strftime("%Y-%m-%d"),

                "today_admissions": 128,

                "emergency_admissions": 36,

                "scheduled_admissions": 72,

                "pending_admissions": 18,

                "waiting_patients": 14,

                "predicted_next_24_hours": 146,

                "average_wait_time_minutes": 22,

                "average_length_of_stay": 4.8
            }

            logger.success(
                "Admission statistics retrieved successfully."
            )

            return result

        except Exception:

            logger.exception(
                "Failed to fetch admission statistics."
            )

            raise

    def calculate_admission_kpis(
        self,
        admission_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Calculating Admission KPIs")

        try:

            total = admission_data["today_admissions"]

            emergency = admission_data["emergency_admissions"]

            scheduled = admission_data["scheduled_admissions"]

            occupancy_pressure = round(
                (total / 150) * 100,
                2
            )

            emergency_percentage = round(
                (emergency / total) * 100,
                2
            ) if total else 0

            scheduled_percentage = round(
                (scheduled / total) * 100,
                2
            ) if total else 0

            kpis = {

                "occupancy_pressure": occupancy_pressure,

                "emergency_percentage": emergency_percentage,

                "scheduled_percentage": scheduled_percentage
            }

            logger.success("Admission KPIs calculated.")

            return kpis

        except Exception:

            logger.exception(
                "Admission KPI calculation failed."
            )

            raise


# ==========================================================
# LangChain Tool
# ==========================================================

@tool
def admissions_analysis_tool(
    hospital_id: str
) -> Dict[str, Any]:
    """
    Retrieve admission statistics and KPIs for a hospital.

    Args:
        hospital_id: Unique Hospital Identifier

    Returns:
        Dictionary containing admission metrics and KPIs.
    """

    logger.info(
        "Executing LangChain Admissions Tool | Hospital={}",
        hospital_id
    )

    service = AdmissionsTool()

    admission_data = service.get_admission_statistics(
        hospital_id
    )

    kpis = service.calculate_admission_kpis(
        admission_data
    )

    response = {

        "statistics": admission_data,

        "kpis": kpis
    }

    logger.success(
        "Admissions Tool execution completed."
    )

    return response
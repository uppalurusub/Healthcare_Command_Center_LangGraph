"""
icu_tool.py

Healthcare Command Center AI

ICU Management Tool

Responsibilities
----------------
• ICU Occupancy
• Critical Patients
• Ventilator Utilization
• Isolation ICU Beds
• Mortality Risk
• Predict ICU Demand
"""

from datetime import datetime
from typing import Dict, Any

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.tools import tool


class ICUTool:
    """
    ICU Tool
    """

    def __init__(self):
        logger.info("Initializing ICU Tool")

    # =====================================================
    # Fetch ICU Statistics
    # =====================================================

    def get_icu_statistics(
        self,
        hospital_id: str
    ) -> Dict[str, Any]:

        logger.info(
            "Fetching ICU Statistics | Hospital={}",
            hospital_id
        )

        try:

            # -------------------------------------------------
            # Replace with HIS / EHR / Database Implementation
            # -------------------------------------------------

            statistics = {

                "hospital_id": hospital_id,

                "date": datetime.now().strftime("%Y-%m-%d"),

                "total_icu_beds": 50,

                "occupied_icu_beds": 44,

                "available_icu_beds": 6,

                "critical_patients": 18,

                "high_risk_patients": 11,

                "ventilators_total": 20,

                "ventilators_in_use": 15,

                "isolation_icu_beds": 8,

                "isolation_occupied": 6,

                "average_length_of_stay": 5.4,

                "predicted_icu_admissions": 9
            }

            logger.success(
                "ICU statistics retrieved successfully."
            )

            return statistics

        except Exception:

            logger.exception(
                "Failed to retrieve ICU statistics."
            )

            raise

    # =====================================================
    # Calculate ICU KPIs
    # =====================================================

    def calculate_icu_kpis(
        self,
        icu_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Calculating ICU KPIs")

        try:

            occupancy_rate = round(

                (
                    icu_data["occupied_icu_beds"]
                    / icu_data["total_icu_beds"]
                ) * 100,

                2
            )

            ventilator_utilization = round(

                (
                    icu_data["ventilators_in_use"]
                    / icu_data["ventilators_total"]
                ) * 100,

                2
            )

            critical_percentage = round(

                (
                    icu_data["critical_patients"]
                    / icu_data["occupied_icu_beds"]
                ) * 100,

                2
            )

            pressure_level = "LOW"

            if occupancy_rate >= 95:

                pressure_level = "CRITICAL"

            elif occupancy_rate >= 85:

                pressure_level = "HIGH"

            elif occupancy_rate >= 70:

                pressure_level = "MEDIUM"

            mortality_risk = "LOW"

            if critical_percentage >= 60:

                mortality_risk = "HIGH"

            elif critical_percentage >= 40:

                mortality_risk = "MEDIUM"

            kpis = {

                "icu_occupancy_rate": occupancy_rate,

                "ventilator_utilization": ventilator_utilization,

                "critical_patient_percentage": critical_percentage,

                "pressure_level": pressure_level,

                "mortality_risk": mortality_risk
            }

            logger.success(
                "ICU KPIs calculated successfully."
            )

            return kpis

        except Exception:

            logger.exception(
                "ICU KPI calculation failed."
            )

            raise


# ==========================================================
# LangChain Tool
# ==========================================================

@tool
def icu_management_tool(
    hospital_id: str
) -> Dict[str, Any]:
    """
    Retrieve ICU statistics and KPIs.

    Args:
        hospital_id:
            Hospital Identifier

    Returns:
        ICU operational metrics.
    """

    logger.info(
        "Executing ICU Management Tool | Hospital={}",
        hospital_id
    )

    service = ICUTool()

    statistics = service.get_icu_statistics(
        hospital_id
    )

    kpis = service.calculate_icu_kpis(
        statistics
    )

    response = {

        "statistics": statistics,

        "kpis": kpis
    }

    logger.success(
        "ICU Management Tool execution completed."
    )

    return response
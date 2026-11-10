"""
finance_tool.py

Healthcare Command Center AI

Finance Tool

Responsibilities
----------------
• Daily Revenue
• Monthly Revenue
• Operating Cost
• Insurance Claims
• Outstanding Payments
• Profit Analysis
• Financial KPIs
"""

from datetime import datetime
from typing import Dict, Any

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.tools import tool


class FinanceTool:
    """
    Finance Tool
    """

    def __init__(self):
        logger.info("Initializing Finance Tool")

    # ==========================================================
    # Retrieve Financial Statistics
    # ==========================================================

    def get_financial_statistics(
        self,
        hospital_id: str
    ) -> Dict[str, Any]:

        logger.info(
            "Fetching Financial Statistics | Hospital={}",
            hospital_id
        )

        try:

            # --------------------------------------------------
            # Replace with Database / ERP / Billing System
            # --------------------------------------------------

            statistics = {

                "hospital_id": hospital_id,

                "date": datetime.now().strftime("%Y-%m-%d"),

                "today_revenue": 565000.00,

                "monthly_revenue": 14625000.00,

                "operating_cost": 11250000.00,

                "insurance_claims": 184,

                "approved_claims": 171,

                "pending_claims": 13,

                "outstanding_payments": 285000.00,

                "average_cost_per_patient": 4525.80,

                "predicted_month_end_revenue": 15800000.00
            }

            logger.success(
                "Financial statistics retrieved successfully."
            )

            return statistics

        except Exception:

            logger.exception(
                "Failed to retrieve financial statistics."
            )

            raise

    # ==========================================================
    # Calculate Financial KPIs
    # ==========================================================

    def calculate_financial_kpis(
        self,
        finance_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Calculating Financial KPIs")

        try:

            revenue = finance_data["monthly_revenue"]

            operating_cost = finance_data["operating_cost"]

            approved_claims = finance_data["approved_claims"]

            insurance_claims = finance_data["insurance_claims"]

            outstanding = finance_data["outstanding_payments"]

            profit = revenue - operating_cost

            profit_margin = round(
                (profit / revenue) * 100,
                2
            ) if revenue else 0

            claim_approval_rate = round(
                (approved_claims / insurance_claims) * 100,
                2
            ) if insurance_claims else 0

            financial_health = "GOOD"

            if profit_margin < 10:
                financial_health = "CRITICAL"

            elif profit_margin < 20:
                financial_health = "WARNING"

            kpis = {

                "profit": round(profit, 2),

                "profit_margin": profit_margin,

                "claim_approval_rate": claim_approval_rate,

                "financial_health": financial_health,

                "outstanding_receivables": outstanding
            }

            logger.success(
                "Financial KPIs calculated successfully."
            )

            return kpis

        except Exception:

            logger.exception(
                "Financial KPI calculation failed."
            )

            raise


# ==========================================================
# LangChain Tool
# ==========================================================

@tool
def finance_management_tool(
    hospital_id: str
) -> Dict[str, Any]:
    """
    Retrieve hospital financial statistics and KPIs.

    Args:
        hospital_id:
            Hospital Identifier

    Returns:
        Financial metrics and KPIs.
    """

    logger.info(
        "Executing Finance Management Tool | Hospital={}",
        hospital_id
    )

    service = FinanceTool()

    statistics = service.get_financial_statistics(
        hospital_id
    )

    kpis = service.calculate_financial_kpis(
        statistics
    )

    response = {

        "statistics": statistics,

        "kpis": kpis
    }

    logger.success(
        "Finance Management Tool execution completed."
    )

    return response
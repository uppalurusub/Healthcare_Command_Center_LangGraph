"""
finance_prompt.py

Finance Agent Prompt
Healthcare Command Center AI

Responsibilities
----------------
• Monitor hospital revenue
• Analyze operational costs
• Track insurance claims
• Monitor outstanding payments
• Forecast financial performance
• Recommend financial improvements
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class FinancePrompt:
    """
    Prompt template used by the Finance Agent.
    """

    PROMPT_VERSION = "1.0.0"

    def __init__(self):
        logger.info(
            "Initializing Finance Prompt Template | Version: {}",
            self.PROMPT_VERSION
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert Hospital Financial Analyst working inside an
AI-powered Healthcare Command Center.

Your responsibilities include:

• Monitor hospital revenue
• Analyze operational expenses
• Track insurance claims
• Monitor outstanding payments
• Evaluate financial performance
• Detect revenue leakage
• Forecast financial trends
• Recommend cost optimization strategies

Instructions

1. Analyze all available financial data.
2. Calculate key financial KPIs.
3. Identify revenue opportunities.
4. Detect financial risks or anomalies.
5. Forecast future financial performance where applicable.
6. Recommend actionable cost optimization strategies.
7. If information is insufficient, clearly explain what additional
   data is required.
8. Never fabricate financial values.
9. Return ONLY valid JSON.

Return your response in the following JSON format:

{{
    "summary": "...",

    "finance": {{
        "today_revenue": 0,
        "monthly_revenue": 0,
        "operating_cost": 0,
        "profit": 0,
        "insurance_claims": 0,
        "pending_claims": 0,
        "claim_approval_rate": 0,
        "outstanding_payments": 0,
        "average_cost_per_patient": 0,
        "predicted_month_end_revenue": 0
    }},

    "alerts": [],

    "recommendations": []
}}
"""
                ),
                (
                    "human",
                    """
Hospital ID:
{hospital_id}

Department:
{department}

Question:
{query}

Financial Data:
{finance_data}
"""
                ),
            ]
        )

        logger.success(
            "Finance Prompt Template initialized successfully."
        )

    def get_prompt(self):
        """
        Return the ChatPromptTemplate instance.
        """
        logger.debug("Returning Finance Prompt Template.")
        return self.prompt

    def format_prompt(
        self,
        hospital_id: str,
        department: str,
        query: str,
        finance_data: str,
    ):
        """
        Format the prompt with runtime values.
        """
        logger.info(
            "Formatting Finance Prompt | Hospital ID: {} | Department: {}",
            hospital_id,
            department,
        )

        try:
            messages = self.prompt.format_messages(
                hospital_id=hospital_id,
                department=department,
                query=query,
                finance_data=finance_data,
            )

            logger.success(
                "Finance Prompt formatted successfully."
            )

            return messages

        except Exception:
            logger.exception(
                "Failed to format Finance Prompt."
            )
            raise
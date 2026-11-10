"""
icu_prompt.py

ICU Agent Prompt
Healthcare Command Center AI

Responsibilities
----------------
• Monitor ICU occupancy
• Analyze critical patients
• Track ventilator utilization
• Detect high-risk patients
• Predict ICU demand
• Recommend operational actions
"""

from app.config.settings import settings
logger = settings.get_logger()
from langchain_core.prompts import ChatPromptTemplate


class ICUPrompt:
    """
    Prompt template used by the ICU Agent.
    """

    PROMPT_VERSION = "1.0.0"

    def __init__(self):
        logger.info(
            "Initializing ICU Prompt Template | Version: {}",
            self.PROMPT_VERSION
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert Intensive Care Unit (ICU) Coordinator working inside an
AI-powered Healthcare Command Center.

Your responsibilities include:

• Monitor ICU occupancy
• Monitor critical patients
• Track ventilator utilization
• Detect deteriorating patients
• Assess mortality risk
• Predict ICU demand
• Identify operational bottlenecks
• Recommend immediate actions

Instructions

1. Analyze all ICU-related data.
2. Calculate ICU utilization metrics.
3. Identify critically ill patients and resource shortages.
4. Detect operational risks.
5. Predict ICU demand when possible.
6. Recommend actionable interventions.
7. If data is insufficient, clearly state what information is missing.
8. Do not fabricate values.

Return your response ONLY in the following JSON format:

{{
  "summary": "...",

  "icu": {{
      "icu_patients": 0,
      "critical_patients": 0,
      "available_icu_beds": 0,
      "occupied_icu_beds": 0,
      "icu_occupancy_rate": 0,
      "ventilators_total": 0,
      "ventilators_in_use": 0,
      "ventilator_utilization": 0,
      "predicted_icu_admissions_24h": 0,
      "mortality_risk": "Low"
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

ICU Data:
{icu_data}
"""
                ),
            ]
        )

        logger.success("ICU Prompt Template initialized successfully.")

    def get_prompt(self):
        """
        Return the ChatPromptTemplate instance.
        """
        logger.debug("Returning ICU Prompt Template.")
        return self.prompt

    def format_prompt(
        self,
        hospital_id: str,
        department: str,
        query: str,
        icu_data: str,
    ):
        """
        Format the prompt with runtime values.
        """
        logger.info(
            "Formatting ICU Prompt | Hospital ID: {} | Department: {}",
            hospital_id,
            department,
        )

        try:
            messages = self.prompt.format_messages(
                hospital_id=hospital_id,
                department=department,
                query=query,
                icu_data=icu_data,
            )

            logger.success("ICU Prompt formatted successfully.")
            return messages

        except Exception:
            logger.exception("Failed to format ICU Prompt.")
            raise
"""
bed_prompt.py

Bed Management Agent Prompt
Healthcare Command Center AI

Responsibilities
----------------
• Monitor bed occupancy
• Track ICU and isolation beds
• Optimize patient allocation
• Predict bed availability
• Recommend operational actions
"""

from app.config.settings import settings
logger = settings.get_logger()
from langchain_core.prompts import ChatPromptTemplate


class BedManagementPrompt:
    """
    Prompt template used by the Bed Management Agent.
    """

    PROMPT_VERSION = "1.0.0"

    def __init__(self):
        logger.info(
            "Initializing Bed Management Prompt Template | Version: {}",
            self.PROMPT_VERSION
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert Hospital Bed Management Coordinator working inside an
AI-powered Healthcare Command Center.

Your responsibilities include:

• Monitor total bed occupancy
• Track ICU bed utilization
• Track isolation bed utilization
• Monitor available beds
• Predict bed availability
• Optimize patient allocation
• Detect occupancy bottlenecks
• Improve patient flow

Instructions

1. Analyze the provided bed management data.
2. Calculate occupancy metrics.
3. Identify operational bottlenecks.
4. Detect risks related to capacity.
5. Recommend actionable improvements.
6. Predict future bed availability when possible.
7. If information is insufficient, clearly state what is missing.
8. Do not fabricate values.

Return your response in the following JSON format:

{{
  "summary": "...",
  "bed_management": {{
      "total_beds": 0,
      "occupied_beds": 0,
      "available_beds": 0,
      "occupancy_rate": 0,
      "icu_beds": 0,
      "icu_available": 0,
      "isolation_beds": 0,
      "expected_discharges": 0
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

Bed Management Data:
{bed_data}
"""
                ),
            ]
        )

        logger.success(
            "Bed Management Prompt Template initialized successfully."
        )

    def get_prompt(self):
        """
        Returns the ChatPromptTemplate instance.
        """
        logger.debug("Returning Bed Management Prompt Template.")
        return self.prompt

    def format_prompt(
        self,
        hospital_id: str,
        department: str,
        query: str,
        bed_data: str,
    ):
        """
        Formats the prompt with runtime values.
        """
        logger.info(
            "Formatting Bed Management Prompt | Hospital ID: {} | Department: {}",
            hospital_id,
            department,
        )

        try:
            prompt = self.prompt.format_messages(
                hospital_id=hospital_id,
                department=department,
                query=query,
                bed_data=bed_data,
            )

            logger.success("Bed Management Prompt formatted successfully.")
            return prompt

        except Exception as ex:
            logger.exception("Failed to format Bed Management Prompt.")
            raise ex
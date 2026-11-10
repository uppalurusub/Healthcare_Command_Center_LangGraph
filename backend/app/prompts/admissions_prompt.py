"""
admissions_prompt.py

Admissions Agent Prompt
Healthcare Command Center AI

Responsibilities
----------------
• Analyze patient admissions
• Predict future admissions
• Monitor emergency queue
• Recommend operational actions
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class AdmissionsPrompt:
    """
    Prompt template used by the Admissions Agent.
    """

    def __init__(self):
        logger.info("Initializing Admissions Prompt Template.")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert Hospital Admissions Coordinator working inside an AI-powered
Healthcare Command Center.

Your responsibilities include:

• Monitor hospital admissions
• Analyze emergency department arrivals
• Track scheduled admissions
• Identify admission bottlenecks
• Forecast admissions for the next 24 hours
• Recommend operational improvements

Instructions

1. Carefully analyze all provided hospital data.
2. Calculate important admission metrics.
3. Identify abnormalities or operational risks.
4. Provide concise executive insights.
5. Recommend actionable next steps.
6. If data is insufficient, clearly state what information is missing.
7. Do not fabricate values.

Return your response in the following JSON format:

{{
  "summary": "...",
  "admissions": {{
      "today": 0,
      "emergency": 0,
      "scheduled": 0,
      "pending": 0,
      "waiting": 0,
      "predicted_next_24_hours": 0
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

Hospital Admission Data:
{admission_data}
"""
                ),
            ]
        )

        logger.success("Admissions Prompt Template created successfully.")

    def get_prompt(self):
        """
        Returns the ChatPromptTemplate instance.
        """
        logger.debug("Returning Admissions Prompt Template.")
        return self.prompt

    def format_prompt(
        self,
        hospital_id: str,
        department: str,
        query: str,
        admission_data: str,
    ):
        """
        Formats the prompt with runtime values.
        """
        logger.info(
            "Formatting Admissions Prompt | Hospital ID: {} | Department: {}",
            hospital_id,
            department,
        )

        try:
            prompt = self.prompt.format_messages(
                hospital_id=hospital_id,
                department=department,
                query=query,
                admission_data=admission_data,
            )

            logger.success("Admissions Prompt formatted successfully.")
            return prompt

        except Exception as ex:
            logger.exception("Failed to format Admissions Prompt.")
            raise ex
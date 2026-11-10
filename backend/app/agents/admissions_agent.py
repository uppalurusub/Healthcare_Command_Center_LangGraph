"""
admissions_agent.py

Enterprise Healthcare Command Center AI

Admissions Agent

Responsibilities
----------------
1. Retrieve admissions statistics from Tool
2. Build AI Prompt
3. Invoke LLM
4. Parse Structured Output
5. Return Statistics + AI Analysis
"""

from typing import Any, Dict

from langchain_core.output_parsers import JsonOutputParser

from app.config.settings import settings
logger = settings.get_logger()

from app.prompts.admissions_prompt import AdmissionsPrompt
from app.tools.admissions_tool import admissions_analysis_tool


class AdmissionsAgent:
    """
    Admissions Agent

    Workflow
    --------
    Tool
        ↓
    Prompt
        ↓
    LLM
        ↓
    JSON Parser
        ↓
    Structured Response
    """

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):

        logger.info(
            "Initializing Admissions Agent..."
        )

        try:

            # -----------------------------------------
            # LLM
            # -----------------------------------------

            self.llm = settings.get_model_client()

            logger.success(
                "LLM initialized."
            )

            # -----------------------------------------
            # Prompt
            # -----------------------------------------

            self.prompt = AdmissionsPrompt()

            logger.success(
                "Admissions Prompt initialized."
            )

            # -----------------------------------------
            # Output Parser
            # -----------------------------------------

            self.parser = JsonOutputParser()

            logger.success(
                "JSON Output Parser initialized."
            )

            # -----------------------------------------
            # Tool
            # -----------------------------------------

            self.tool = admissions_analysis_tool

            logger.success(
                "Admissions Tool initialized."
            )

            logger.success(
                "Admissions Agent initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Admissions Agent initialization failed: {}",
                ex
            )

            raise

    

    # ==========================================================
    # Execute Agent
    # ==========================================================

    def run(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        hospital_id = state["hospital_id"]

        query = state["query"]

        logger.info(
            "Admissions Agent Started | Hospital={}",
            hospital_id
        )

        try:

            # -----------------------------------------------------
            # Step 1 : Call Admissions Tool
            # -----------------------------------------------------

            logger.info(
                "Calling Admissions Analysis Tool..."
            )

            tool_result = self.tool.invoke(

                {
                    "hospital_id": hospital_id
                }

            )

            logger.success(
                "Admissions Tool completed successfully."
            )

            logger.debug(
                "Admissions Tool Result : {}",
                tool_result
            )

            # -----------------------------------------------------
            # Step 2 : Build Prompt
            # -----------------------------------------------------

            logger.info(
                "Formatting Admissions Prompt..."
            )

            messages = self.prompt.format_prompt(

                hospital_id=hospital_id,

                department="Admissions",

                query=query,

                admission_data=str(tool_result)

            )

            logger.success(
                "Admissions Prompt created."
            )

            # -----------------------------------------------------
            # Step 3 : Invoke LLM
            # -----------------------------------------------------

            logger.info(
                "Invoking Admissions LLM..."
            )

            response = self.llm.invoke(
                messages
            )

            logger.success(
                "LLM invocation completed."
            )

            logger.debug(
                "Raw LLM Response : {}",
                response.content
            )

            # -----------------------------------------------------
            # Step 4 : Parse JSON
            # -----------------------------------------------------

            logger.info(
                "Parsing Admissions JSON..."
            )

            parsed = self.parser.parse(
                response.content
            )

            logger.success(
                "Admissions JSON parsed successfully."
            )

            logger.debug(
                "Parsed AI Output : {}",
                parsed
            )

            # -----------------------------------------------------
            # Step 5 : Build Enterprise Response
            # -----------------------------------------------------

            result = {

                "statistics":

                    tool_result,

                "ai": {

                    "summary":

                        parsed.get(
                            "summary",
                            ""
                        ),

                    "risk":

                        parsed.get(
                            "risk",
                            "Low"
                        ),

                    "confidence_score":

                        parsed.get(
                            "confidence_score",
                            0.95
                        ),

                    "recommendations":

                        parsed.get(
                            "recommendations",
                            []
                        )

                },

                "recommendations":

                    parsed.get(
                        "recommendations",
                        []
                    )

            }

            logger.success(
                "Admissions Agent completed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "Admissions Agent execution failed : {}",
                ex
            )

            raise

    # ==========================================================
    # Build AI Response
    # ==========================================================

    def _build_ai_response(
        self,
        parsed: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Building AI response..."
        )

        ai = {

            "summary":

                parsed.get(
                    "summary",
                    ""
                ),

            "risk":

                parsed.get(
                    "risk",
                    "Low"
                ),

            "confidence_score":

                parsed.get(
                    "confidence_score",
                    0.95
                ),

            "recommendations":

                parsed.get(
                    "recommendations",
                    []
                )

        }

        logger.success(
            "AI response created."
        )

        return ai
"""
icu_agent.py

Enterprise Healthcare Command Center AI

ICU Agent

Responsibilities
----------------
1. Retrieve ICU statistics
2. Build AI Prompt
3. Invoke LLM
4. Parse Structured Output
5. Return Statistics + AI Analysis
"""

from typing import Any, Dict

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.output_parsers import JsonOutputParser


from app.prompts.icu_prompt import ICUPrompt
from app.tools.icu_tool import icu_management_tool


class ICUAgent:
    """
    Enterprise ICU Agent

    Workflow
    --------
        ICU Tool
            │
            ▼
        ICU Prompt
            │
            ▼
            LLM
            │
            ▼
        JSON Parser
            │
            ▼
    Structured Response
    """

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):

        logger.info(
            "Initializing ICU Agent..."
        )

        try:

            # --------------------------------------------------
            # Initialize LLM
            # --------------------------------------------------

            self.llm = settings.get_model_client()

            logger.success(
                "LLM initialized successfully."
            )

            # --------------------------------------------------
            # Initialize Prompt
            # --------------------------------------------------

            self.prompt = ICUPrompt()

            logger.success(
                "ICU Prompt initialized."
            )

            # --------------------------------------------------
            # Initialize JSON Parser
            # --------------------------------------------------

            self.parser = JsonOutputParser()

            logger.success(
                "JSON Output Parser initialized."
            )

            # --------------------------------------------------
            # Initialize Tool
            # --------------------------------------------------

            self.tool = icu_management_tool

            logger.success(
                "ICU Management Tool initialized."
            )

            logger.success(
                "ICU Agent initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Failed to initialize ICU Agent: {}",
                ex
            )

            raise

    # ==========================================================
    # Execute Agent
    # ==========================================================

        # ==========================================================
    # Execute ICU Agent
    # ==========================================================

    def run(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        hospital_id = state["hospital_id"]

        query = state["query"]

        logger.info(
            "ICU Agent Started | Hospital={}",
            hospital_id
        )

        try:

            # --------------------------------------------------
            # Step 1 : Retrieve ICU Statistics
            # --------------------------------------------------

            logger.info(
                "Calling ICU Management Tool..."
            )

            tool_result = self.tool.invoke(

                {
                    "hospital_id": hospital_id
                }

            )

            logger.success(
                "ICU Management Tool completed successfully."
            )

            logger.debug(
                "ICU Tool Result : {}",
                tool_result
            )

            # --------------------------------------------------
            # Step 2 : Build Prompt
            # --------------------------------------------------

            logger.info(
                "Formatting ICU Prompt..."
            )

            messages = self.prompt.format_prompt(

                hospital_id=hospital_id,

                department="ICU",

                query=query,

                icu_data=str(tool_result)

            )

            logger.success(
                "ICU Prompt created."
            )

            # --------------------------------------------------
            # Step 3 : Invoke LLM
            # --------------------------------------------------

            logger.info(
                "Invoking ICU LLM..."
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

            # --------------------------------------------------
            # Step 4 : Parse JSON
            # --------------------------------------------------

            logger.info(
                "Parsing ICU JSON..."
            )

            parsed = self.parser.parse(
                response.content
            )

            logger.success(
                "ICU JSON parsed successfully."
            )

            logger.debug(
                "Parsed ICU AI Output : {}",
                parsed
            )

            # --------------------------------------------------
            # Step 5 : Build Enterprise Response
            # --------------------------------------------------

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
                "ICU Agent completed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "ICU Agent execution failed : {}",
                ex
            )

            raise

        # ==========================================================
    # Build Statistics
    # ==========================================================

    def _build_statistics(
        self,
        tool_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Building ICU statistics..."
        )

        if not tool_result:

            logger.warning(
                "ICU Management Tool returned empty data."
            )

            return {}

        logger.success(
            "ICU statistics created successfully."
        )

        return tool_result
    
        # ==========================================================
    # Build AI Response
    # ==========================================================

    def _build_ai_response(
        self,
        parsed: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Building ICU AI response..."
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
            "ICU AI response created."
        )

        return ai
    
        # ==========================================================
    # Build Final Response
    # ==========================================================

    def _build_response(
        self,
        tool_result: Dict[str, Any],
        parsed: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Constructing ICU response..."
        )

        statistics = self._build_statistics(
            tool_result
        )

        ai = self._build_ai_response(
            parsed
        )

        response = {

            "statistics":

                statistics,

            "ai":

                ai,

            "recommendations":

                ai.get(
                    "recommendations",
                    []
                )

        }

        logger.success(
            "ICU response created successfully."
        )

        return response
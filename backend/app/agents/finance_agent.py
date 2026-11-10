"""
finance_agent.py

Enterprise Healthcare Command Center AI

Finance Agent

Responsibilities
----------------
1. Retrieve Financial KPIs
2. Build AI Prompt
3. Invoke LLM
4. Parse Structured Output
5. Return Statistics + AI Analysis
"""

from typing import Any, Dict

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.output_parsers import JsonOutputParser


from app.prompts.finance_prompt import FinancePrompt
from app.tools.finance_tool import finance_management_tool


class FinanceAgent:
    """
    Enterprise Finance Agent

    Workflow
    --------
        Finance Tool
              │
              ▼
        Finance Prompt
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
            "Initializing Finance Agent..."
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

            self.prompt = FinancePrompt()

            logger.success(
                "Finance Prompt initialized."
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

            self.tool = finance_management_tool

            logger.success(
                "Finance Analysis Tool initialized."
            )

            logger.success(
                "Finance Agent initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Failed to initialize Finance Agent: {}",
                ex
            )

            raise

    

    # ==========================================================
    # Execute Finance Agent
    # ==========================================================

    def run(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        hospital_id = state["hospital_id"]

        query = state["query"]

        logger.info(
            "Finance Agent Started | Hospital={}",
            hospital_id
        )

        try:

            # --------------------------------------------------
            # Step 1 : Retrieve Financial Statistics
            # --------------------------------------------------

            logger.info(
                "Calling Finance Analysis Tool..."
            )

            tool_result = self.tool.invoke(
                {
                    "hospital_id": hospital_id
                }
            )

            logger.success(
                "Finance Analysis Tool completed successfully."
            )

            logger.debug(
                "Finance Tool Result : {}",
                tool_result
            )

            # --------------------------------------------------
            # Step 2 : Build Prompt
            # --------------------------------------------------

            logger.info(
                "Formatting Finance Prompt..."
            )

            messages = self.prompt.format_prompt(

                hospital_id=hospital_id,

                department="Finance",

                query=query,

                finance_data=str(tool_result)

            )

            logger.success(
                "Finance Prompt created."
            )

            # --------------------------------------------------
            # Step 3 : Invoke LLM
            # --------------------------------------------------

            logger.info(
                "Invoking Finance LLM..."
            )

            response = self.llm.invoke(
                messages
            )

            logger.success(
                "Finance LLM invocation completed."
            )

            logger.debug(
                "Raw Finance LLM Response : {}",
                response.content
            )

            # --------------------------------------------------
            # Step 4 : Parse JSON
            # --------------------------------------------------

            logger.info(
                "Parsing Finance JSON..."
            )

            parsed = self.parser.parse(
                response.content
            )

            logger.success(
                "Finance JSON parsed successfully."
            )

            logger.debug(
                "Parsed Finance AI Output : {}",
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
                "Finance Agent completed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "Finance Agent execution failed : {}",
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
            "Building Finance statistics..."
        )

        if not tool_result:

            logger.warning(
                "Finance Analysis Tool returned empty data."
            )

            return {}

        logger.success(
            "Finance statistics created successfully."
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
            "Building Finance AI response..."
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
            "Finance AI response created."
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
            "Constructing Finance response..."
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
            "Finance response created successfully."
        )

        return response
"""
bed_agent.py

Enterprise Healthcare Command Center AI

Bed Management Agent

Responsibilities
----------------
1. Retrieve Bed Management statistics
2. Build AI Prompt
3. Invoke LLM
4. Parse Structured Output
5. Return Statistics + AI Analysis
"""

from typing import Any, Dict

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.output_parsers import JsonOutputParser


from app.prompts.bed_prompt import BedManagementPrompt
from app.tools.bed_tool import bed_management_tool


class BedManagementAgent:
    """
    Enterprise Bed Management Agent

    Workflow
    --------
        Bed Tool
            │
            ▼
      Bed Prompt
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
            "Initializing Bed Management Agent..."
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

            self.prompt = BedManagementPrompt()

            logger.success(
                "Bed Management Prompt initialized."
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

            self.tool = bed_management_tool

            logger.success(
                "Bed Management Tool initialized."
            )

            logger.success(
                "Bed Management Agent initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Failed to initialize Bed Management Agent: {}",
                ex
            )

            raise

    

    # ==========================================================
    # Execute Bed Management Agent
    # ==========================================================

    def run(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        hospital_id = state["hospital_id"]

        query = state["query"]

        logger.info(
            "Bed Management Agent Started | Hospital={}",
            hospital_id
        )

        try:

            # --------------------------------------------------
            # Step 1 : Retrieve Bed Statistics
            # --------------------------------------------------

            logger.info(
                "Calling Bed Management Tool..."
            )

            tool_result = self.tool.invoke(

                {
                    "hospital_id": hospital_id
                }

            )

            logger.success(
                "Bed Management Tool completed successfully."
            )

            logger.debug(
                "Bed Tool Result : {}",
                tool_result
            )

            # --------------------------------------------------
            # Step 2 : Build Prompt
            # --------------------------------------------------

            logger.info(
                "Formatting Bed Management Prompt..."
            )

            messages = self.prompt.format_prompt(

                hospital_id=hospital_id,

                department="Bed Management",

                query=query,

                bed_data=str(tool_result)

            )

            logger.success(
                "Bed Management Prompt created."
            )

            # --------------------------------------------------
            # Step 3 : Invoke LLM
            # --------------------------------------------------

            logger.info(
                "Invoking Bed Management LLM..."
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
                "Parsing Bed Management JSON..."
            )

            parsed = self.parser.parse(
                response.content
            )

            logger.success(
                "Bed Management JSON parsed successfully."
            )

            logger.debug(
                "Parsed AI Output : {}",
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
                "Bed Management Agent completed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "Bed Management Agent execution failed : {}",
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
            "Building Bed Management statistics..."
        )

        if not tool_result:

            logger.warning(
                "Bed Management Tool returned empty data."
            )

            return {}

        logger.success(
            "Bed Management statistics created."
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
            "Building Bed Management AI response..."
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
            "Bed Management AI response created."
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
            "Constructing Bed Management response..."
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
            "Bed Management response created successfully."
        )

        return response
    


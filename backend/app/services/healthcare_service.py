"""
healthcare_service.py

Enterprise Healthcare Command Center AI

Service Layer

Responsibilities
----------------
1. Receive API Requests
2. Delegate to Implementation Layer
3. Return CommandCenterResponse
4. Health Check
5. Enterprise Logging
"""

from __future__ import annotations

from typing import Any
from typing import Dict

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.healthcare_impl import (
    HealthcareImplementation,
)

from app.schemas.request_model import (
    CommandCenterRequest,
)

from app.schemas.response_model import (
    CommandCenterResponse,
)

class HealthcareService:
    """
    Enterprise Healthcare Service

    Router
        │
        ▼
    Service
        │
        ▼
    Implementation
        │
        ▼
    Healthcare Graph
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        logger.info(
            "Initializing Healthcare Service..."
        )

        try:

            self.implementation = (
                HealthcareImplementation()
            )

            logger.success(
                "Healthcare Implementation initialized."
            )

            logger.success(
                "Healthcare Service initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Healthcare Service initialization failed: {}",
                ex
            )

            raise

    # =====================================================
    # Log Incoming Request
    # =====================================================

    @staticmethod
    def _log_request(
        request: CommandCenterRequest
    ) -> None:

        logger.info(
            "Healthcare Service Request Received"
        )

        logger.info(
            "Hospital ID : {}",
            request.hospital_id
        )

        logger.info(
            "User ID : {}",
            request.user_id
        )

        logger.info(
            "Agent : {}",
            request.agent
        )

        logger.info(
            "Query : {}",
            request.query
        )

    # =====================================================
    # Log Response
    # =====================================================

    @staticmethod
    def _log_response(
        response: CommandCenterResponse
    ) -> None:

        logger.success(
            "Healthcare Service completed successfully."
        )

        logger.info(
            "Status : {}",
            response.status
        )

        logger.info(
            "Success : {}",
            response.success
        )

    # =====================================================
    # Process Request
    # =====================================================

    async def process_request(
        self,
        request: CommandCenterRequest
    ) -> CommandCenterResponse:

        logger.info(
            "Healthcare Service processing request..."
        )

        try:

            # ----------------------------------------------
            # Log Request
            # ----------------------------------------------

            self._log_request(
                request
            )

            # ----------------------------------------------
            # Invoke Implementation
            # ----------------------------------------------

            response = await self.implementation.process(
                request
            )

            # ----------------------------------------------
            # Log Response
            # ----------------------------------------------

            self._log_response(
                response
            )

            logger.success(
                "Healthcare Service request completed."
            )

            return response

        except Exception as ex:

            logger.exception(
                "Healthcare Service request failed: {}",
                ex
            )

            return self.implementation.handle_exception(
                ex
            )
        
    # =====================================================
    # Async Process Request
    # =====================================================

    async def process_request_async(
        self,
        request: CommandCenterRequest
    ) -> CommandCenterResponse:

        logger.info(
            "Executing asynchronous Healthcare request..."
        )

        return await self.process_request(
            request
        )

    # =====================================================
    # Execute Implementation
    # =====================================================

    async def execute(
        self,
        request: CommandCenterRequest
    ) -> CommandCenterResponse:

        logger.info(
            "Invoking Healthcare Implementation..."
        )

        response = await self.implementation.process(
            request
        )

        logger.success(
            "Healthcare Implementation completed."
        )

        return response

    # =====================================================
    # Health Check
    # =====================================================

    async def health_check(
        self
    ) -> Dict[str, Any]:

        logger.info(
            "Healthcare Service Health Check started."
        )

        try:

            implementation_health = (
                await self.implementation.health_check()
            )

            health = {

                "service": "Healthy",

                "implementation":

                    implementation_health,

                "status": "UP"

            }

            logger.success(
                "Healthcare Service Health Check completed."
            )

            return health

        except Exception as ex:

            logger.exception(
                "Healthcare Service Health Check failed : {}",
                ex
            )

            return {

                "service": "DOWN",

                "status": "FAILED",

                "error": str(ex)

            }
        
    # =====================================================
    # Readiness Check
    # =====================================================

    async def readiness_check(
        self
    ) -> Dict[str, Any]:

        logger.info(
            "Readiness Check..."
        )

        return {

            "ready": True,

            "graph": "Ready",

            "implementation": "Ready",

            "service": "Ready"

        }

    # =====================================================
    # Supported Agents
    # =====================================================

    @staticmethod
    def supported_agents() -> list[str]:

        logger.info(
            "Retrieving supported agents."
        )

        return [

            "supervisor",

            "admissions",

            "bed_management",

            "icu",

            "finance"

        ]

        # =====================================================
    # Supported Analytics
    # =====================================================

    @staticmethod
    def supported_analytics() -> list[str]:

        logger.info(
            "Retrieving supported analytics."
        )

        return [

            "Admissions",

            "Bed Management",

            "ICU",

            "Finance"

        ]

    # =====================================================
    # Version Information
    # =====================================================

    @staticmethod
    def version() -> Dict[str, str]:

        return {

            "application":

                "Healthcare Command Center AI",

            "version":

                "1.0.0",

            "framework":

                "LangGraph",

            "llm":

                "OpenAI GPT-4.1"

        }

    # =====================================================
    # Service Statistics
    # =====================================================

    @staticmethod
    def statistics() -> Dict[str, Any]:

        return {

            "agents": 5,

            "analytics_modules": 4,

            "graph": "HealthcareGraph",

            "architecture":

                "Router → Service → Implementation → Graph"

        }

    # =====================================================
    # Enterprise Exception Handler
    # =====================================================

    @staticmethod
    def handle_exception(
        ex: Exception
    ) -> Dict[str, Any]:

        logger.exception(
            "Unhandled Healthcare Service Exception : {}",
            ex
        )

        return {

            "success": False,

            "status": "FAILED",

            "message": str(ex)

        }


    # =====================================================
    # Startup Banner
    # =====================================================

    @staticmethod
    def startup_banner():

        logger.info("=" * 70)

        logger.info(
            "Healthcare Command Center AI"
        )

        logger.info(
            "Enterprise Multi-Agent Platform"
        )

        logger.info(
            "Router → Service → Implementation → Graph"
        )

        logger.info("=" * 70)
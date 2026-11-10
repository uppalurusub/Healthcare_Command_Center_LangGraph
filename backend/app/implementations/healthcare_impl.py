"""
healthcare_impl.py

Enterprise Healthcare Command Center AI
aryResponse
Implementation Layer

Responsibilities
----------------
1. Validate Request
2. Build Graph State
3. Execute LangGraph
4. Map Response
5. Return CommandCenterResponse
"""

from __future__ import annotations

from typing import Any
from typing import Dict
import time

from app.config.settings import settings
logger = settings.get_logger()

from app.graph.healthcare_graph import HealthcareGraph

from app.models.request_model import (
    CommandCenterRequest,
)

from app.models.response_model import (
    CommandCenterResponse,
)

from app.models.response_model import (
    AdmissionsResponse,
    BedManagementResponse,
    ICUResponse,
    FinanceResponse,
    AnalyticsResponse,
    MetadataResponse,
)


class HealthcareImplementation:
    """
    Enterprise Healthcare Implementation

    Router
        ↓

    Service
        ↓

    Implementation
        ↓

    Healthcare Graph
        ↓

    Supervisor
        ↓

    Agents
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        logger.info(
            "Initializing Healthcare Implementation..."
        )

        try:

            self.graph = HealthcareGraph()

            logger.success(
                "Healthcare Graph initialized."
            )

            logger.success(
                "Healthcare Implementation initialized successfully."
            )

        except Exception as ex:

            logger.exception(
                "Healthcare Implementation initialization failed : {}",
                ex
            )

            raise

    # =====================================================
    # Log Request
    # =====================================================

    def _log_request(
        self,
        request: CommandCenterRequest
    ) -> None:

        logger.info(
            "Hospital ID : {}",
            request.hospital_id
        )

        logger.info(
            "User ID : {}",
            request.user_id
        )

        logger.info(
            "Requested Agent : {}",
            request.agent
        )

        logger.info(
            "Query : {}",
            request.query
        )

    # =====================================================
    # Validate Request
    # =====================================================

    def _validate_request(
        self,
        request: CommandCenterRequest
    ) -> None:

        logger.info(
            "Validating request..."
        )

        if not request.hospital_id:

            raise ValueError(
                "Hospital ID cannot be empty."
            )

        if not request.query:

            raise ValueError(
                "Query cannot be empty."
            )

        logger.success(
            "Request validation completed."
        )

    # =====================================================
    # Build Initial Graph State
    # =====================================================

    def build_state(
        self,
        request: CommandCenterRequest
    ) -> Dict[str, Any]:

        logger.info(
            "Building Healthcare Graph State..."
        )

        state = {

            # =====================================================
            # Request Information
            # =====================================================

            "hospital_id":

                request.hospital_id,

            "user_id":

                request.user_id,

            "query":

                request.query,

            "agent":

                request.agent,

            # =====================================================
            # Analytics Selection
            # =====================================================

            "analytics": {

                "admissions":

                    request.analytics.admissions,

                "bed_management":

                    request.analytics.bed_management,

                "icu":

                    request.analytics.icu,

                "finance":

                    request.analytics.finance

            },

            # =====================================================
            # Filters
            # =====================================================

            "filters": {

                "department":

                    request.filters.department,

                "ward":

                    request.filters.ward,

                "patient_id":

                    request.filters.patient_id,

                "physician":

                    request.filters.physician,

                "admission_date":

                    request.filters.admission_date,

                "discharge_date":

                    request.filters.discharge_date

            },

            # =====================================================
            # Options
            # =====================================================

            "top_k":

                request.top_k,

            "include_recommendations":

                request.include_recommendations,

            "include_predictions":

                request.include_predictions,

            "metadata":

                request.metadata,

            # =====================================================
            # Workflow Runtime
            # =====================================================

            "execution_plan": [],

            "completed_agents": [],

            "start_time": time.perf_counter(),

            "summary": {},

            "admissions": {},

            "bed_management": {},

            "icu": {},

            "finance": {},

            "recommendations": [],

            "analytics_response": {},

            "ai_outputs": {},

            "status": "Initialized",

            "success": False,

            "message": ""

        }

        logger.success(
            "Healthcare Graph State created."
        )

        return state
    
    # =====================================================
    # Execute Healthcare Graph
    # =====================================================

    def execute_graph(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Executing Healthcare Graph..."
        )

        try:

            result = self.graph.invoke(
                state
            )

            logger.success(
                "Healthcare Graph executed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "Healthcare Graph execution failed : {}",
                ex
            )

            raise

    # =====================================================
    # Execute Workflow
    # =====================================================

    def execute(
        self,
        request: CommandCenterRequest
    ) -> Dict[str, Any]:

        logger.info(
            "Healthcare workflow started."
        )

        self._validate_request(
            request
        )

        self._log_request(
            request
        )

        state = self.build_state(
            request
        )

        result = self.execute_graph(
            state
        )

        logger.success(
            "Healthcare workflow completed."
        )

        return result
    

    # =====================================================
    # Build Response
    # =====================================================

    




    def build_response(
        self,
        state: dict
    ) -> CommandCenterResponse:

        logger.info(
            "Building CommandCenterResponse..."
        )

        try:

            response = CommandCenterResponse(

                success=state.get(
                    "success",
                    True
                ),

                status=state.get(
                    "status",
                    "SUCCESS"
                ),

                message=state.get(
                    "message",
                    "Healthcare Command Center completed successfully."
                ),

                hospital_id=state.get("hospital_id"),
                generated_at=(
                    state.get("analytics_response", {}).get("timestamp")
                    if isinstance(state.get("analytics_response"), dict)
                    else None
                ),

                summary=state.get(
                    "summary",
                    None
                ),

                admissions=state.get(
                    "admissions",
                    None
                ),

                bed_management=state.get(
                    "bed_management",
                    None
                ),

                icu=state.get(
                    "icu",
                    None
                ),

                finance=state.get(
                    "finance",
                    None
                ),

                recommendations=state.get(
                    "recommendations",
                    []
                ),

                analytics=state.get(
                    "analytics_response",
                    None
                ),

                metadata=state.get(
                    "metadata",
                    None
                )

            )

            logger.success(
                "CommandCenterResponse created successfully."
            )

            return response

        except Exception as ex:

            logger.exception(
                "Failed building CommandCenterResponse : {}",
                ex
            )

            raise

    # =====================================================
    # Summary
    # =====================================================

    def _build_summary(
        self,
        state: Dict[str, Any]
    ) -> SummaryResponse:

        logger.info(
            "Building summary..."
        )

        return SummaryResponse(

            executive_summary=

                state["summary"].get(
                    "executive_summary",
                    ""
                ),

            predicted_risk=

                state["summary"].get(
                    "predicted_risk",
                    "Low"
                ),

            confidence_score=

                state["summary"].get(
                    "confidence_score",
                    0.95
                )

        )

    # =====================================================
    # Admissions
    # =====================================================

    def _build_admissions(
        self,
        state: Dict[str, Any]
    ) -> AdmissionsResponse:

        return AdmissionsResponse(

            **state.get(
                "admissions",
                {}
            )

        )

    # =====================================================
    # Bed Management
    # =====================================================

    def _build_bed_management(
        self,
        state: Dict[str, Any]
    ) -> BedManagementResponse:

        return BedManagementResponse(

            **state.get(
                "bed_management",
                {}
            )

        )

    # =====================================================
    # ICU
    # =====================================================

    def _build_icu(
        self,
        state: Dict[str, Any]
    ) -> ICUResponse:

        return ICUResponse(

            **state.get(
                "icu",
                {}
            )

        )

    # =====================================================
    # Finance
    # =====================================================

    def _build_finance(
        self,
        state: Dict[str, Any]
    ) -> FinanceResponse:

        return FinanceResponse(

            **state.get(
                "finance",
                {}
            )

        )

    # =====================================================
    # Analytics
    # =====================================================

    def _build_analytics(
        self,
        state: Dict[str, Any]
    ) -> AnalyticsResponse:

        analytics = state.get(
            "analytics_response",
            {}
        )

        return AnalyticsResponse(

            timestamp=

                analytics.get(
                    "timestamp",
                    ""
                ),

            hospital_status=

                analytics.get(
                    "hospital_status",
                    ""
                ),

            alerts=

                analytics.get(
                    "alerts",
                    []
                ),

            kpis=

                analytics.get(
                    "kpis",
                    {}
                )

        )

    # =====================================================
    # Metadata
    # =====================================================

    def _build_metadata(
        self,
        state: Dict[str, Any]
    ) -> MetadataResponse:

        metadata = state.get(
            "metadata",
            {}
        )

        return MetadataResponse(

            request_id=

                metadata.get(
                    "request_id",
                    ""
                ),

            processing_time_ms=

                metadata.get(
                    "processing_time_ms",
                    0
                ),

            workflow=

                metadata.get(
                    "workflow",
                    ""
                ),

            agent=

                metadata.get(
                    "agent",
                    ""
                ),

            model_name=

                metadata.get(
                    "model_name",
                    ""
                )

        )

    # =====================================================
    # Process Request
    # =====================================================

    async def process(
        self,
        request: CommandCenterRequest
    ) -> CommandCenterResponse:

        logger.info(
            "Healthcare Command Center processing started."
        )

        try:

            self._validate_request(
                request
            )

            self._log_request(
                request
            )

            state = self.build_state(
                request
            )

            state = self.execute_graph(
                state
            )

            response = self.build_response(
                state
            )

            logger.success(
                "Healthcare Command Center completed successfully."
            )

            return response

        except Exception as ex:

            logger.exception(
                "Healthcare processing failed : {}",
                ex
            )

            raise

    # =====================================================
    # Async Execute
    # =====================================================

    async def process_async(
        self,
        request: CommandCenterRequest
    ) -> CommandCenterResponse:

        logger.info(
            "Executing async workflow..."
        )

        return await self.process(
            request
        )

    # =====================================================
    # Health Check
    # =====================================================

    async def health_check(
        self
    ) -> Dict[str, Any]:

        logger.info(
            "Healthcare Implementation Health Check..."
        )

        try:

            return {

                "status":

                    "Healthy",

                "graph":

                    "Ready",

                "implementation":

                    "Ready"

            }

        except Exception as ex:

            logger.exception(
                "Health Check Failed : {}",
                ex
            )

            return {

                "status":

                    "Unhealthy",

                "error":

                    str(ex)

            }
        
    # =====================================================
    # Get Supported Agents
    # =====================================================

    @staticmethod
    def supported_agents() -> list[str]:

        return [

            "supervisor",

            "admissions",

            "bed_management",

            "icu",

            "finance"

        ]

    # =====================================================
    # Enabled Analytics
    # =====================================================

    @staticmethod
    def enabled_analytics(
        request: CommandCenterRequest
    ) -> list[str]:

        analytics = []

        if request.analytics.admissions:

            analytics.append(
                "Admissions"
            )

        if request.analytics.bed_management:

            analytics.append(
                "Bed Management"
            )

        if request.analytics.icu:

            analytics.append(
                "ICU"
            )

        if request.analytics.finance:

            analytics.append(
                "Finance"
            )

        return analytics

    # =====================================================
    # Enterprise Exception Handler
    # =====================================================

    @staticmethod
    def handle_exception(ex: Exception) -> CommandCenterResponse:
        """Return a schema-valid failure response without masking the original error."""
        logger.exception("Unhandled Exception: {}", ex)
        return CommandCenterResponse(
            success=False,
            status="FAILED",
            message=str(ex),
            summary=None,
            admissions=None,
            bed_management=None,
            icu=None,
            finance=None,
            recommendations=[],
            analytics=None,
            metadata=None,
        )

"""
supervisor_agent.py

Enterprise Healthcare Command Center AI

Supervisor Agent

Responsibilities
----------------
1. Determine execution plan
2. Route requests
3. Execute required agents
4. Aggregate responses
5. Generate executive summary
"""

from typing import Dict
from typing import Any
from typing import List

from app.config.settings import settings
logger = settings.get_logger()

from app.agents.admissions_agent import AdmissionsAgent
from app.agents.bed_agent import BedManagementAgent
from app.agents.icu_agent import ICUAgent
from app.agents.finance_agent import FinanceAgent
from datetime import datetime
import time

class SupervisorAgent:

    def __init__(self):

        logger.info(
            "Initializing Supervisor Agent..."
        )

        self.admissions = AdmissionsAgent()

        self.bed = BedManagementAgent()

        self.icu = ICUAgent()

        self.finance = FinanceAgent()

        logger.success(
            "Supervisor Agent initialized successfully."
        )

    # ==========================================================
    # Determine Execution Plan
    # ==========================================================

    def determine_execution_plan(
        self,
        state: Dict[str, Any]
    ) -> List[str]:

        logger.info(
            "Determining execution plan..."
        )

        analytics = state.get(
            "analytics",
            {}
        )

        plan = []

        if analytics.get(
            "admissions",
            False
        ):
            plan.append(
                "admissions"
            )

        if analytics.get(
            "bed_management",
            False
        ):
            plan.append(
                "bed_management"
            )

        if analytics.get(
            "icu",
            False
        ):
            plan.append(
                "icu"
            )

        if analytics.get(
            "finance",
            False
        ):
            plan.append(
                "finance"
            )

        logger.success(
            "Execution Plan : {}",
            plan
        )

        return plan
    
    # ==========================================================
    # Next Agent
    # ==========================================================

    def determine_next_agent(
        self,
        state: Dict[str, Any]
    ) -> str:

        execution_plan = state.get(
            "execution_plan",
            []
        )

        completed = state.get(
            "completed_agents",
            []
        )

        for agent in execution_plan:

            if agent not in completed:

                logger.info(
                    "Routing to {}",
                    agent
                )

                return agent

        logger.info(
            "All agents completed."
        )

        return "finalize"
    
    # ==========================================================
    # Initialize Workflow State
    # ==========================================================

    def initialize_state(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Initializing Supervisor State..."
        )

        # The implementation initializes execution_plan to [] before invoking
        # LangGraph. An empty list is therefore not proof that planning has run.
        # Build the plan when it is absent OR empty and no department has yet
        # completed. Once execution starts, preserve the plan across supervisor
        # revisits so completed agents are not re-planned or repeated.
        if not state.get("execution_plan") and not state.get("completed_agents"):
            state["execution_plan"] = self.determine_execution_plan(state)
            logger.info(
                "Execution plan initialized from request analytics | selected={} | plan={}",
                state.get("analytics", {}),
                state["execution_plan"],
            )
        state.setdefault("completed_agents", [])
        state.setdefault("recommendations", [])
        state.setdefault("summary", {})
        state.setdefault("analytics_response", {})
        state.setdefault("metadata", {})
        state.setdefault("ai_outputs", {})
        state.setdefault("status", "RUNNING")
        state.setdefault("error", "")

        logger.success(
            "Workflow State Initialized."
        )

        return state
    
    # ==========================================================
    # Mark Agent Complete
    # ==========================================================

    def mark_completed(
        self,
        state: Dict[str, Any],
        agent: str
    ):

        completed = state.get(
            "completed_agents",
            []
        )

        if agent not in completed:

            completed.append(
                agent
            )

        state["completed_agents"] = completed

        logger.success(
            "{} completed.",
            agent
        )

    # ==========================================================
    # Run
    # ==========================================================

    def run(
        self,
        state: Dict[str, Any]
    ):

        logger.info(
            "Supervisor Started..."
        )

        # build_state() seeds execution_plan=[]; test for an empty plan as
        # well as a missing key. Do not re-plan after any department completed.
        if not state.get("execution_plan") and not state.get("completed_agents"):
            state = self.initialize_state(state)

        state["next_agent"] = (
            self.determine_next_agent(
                state
            )
        )

        logger.success(
            "Next Agent : {}",
            state["next_agent"]
        )

        return state
    

    # ==========================================================
    # Execute Admissions
    # ==========================================================

    def execute_admissions(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Executing Admissions Agent")

        try:

            result = self.admissions.run(state)

            state["admissions"] = result.get(
                "statistics",
                {}
            )

            state.setdefault(
                "recommendations",
                []
            ).extend(
                result.get(
                    "recommendations",
                    []
                )
            )

            state.setdefault(
                "ai_outputs",
                {}
            )["admissions"] = result.get(
                "ai",
                {}
            )

            self.mark_completed(
                state,
                "admissions"
            )

            logger.success(
                "Admissions Agent execution completed."
            )

            return state

        except Exception as ex:

            logger.exception(
                "Admissions execution failed: {}",
                ex
            )

            raise


    # ==========================================================
    # Execute Bed Management
    # ==========================================================

    def execute_bed(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Executing Bed Management Agent")

        try:

            result = self.bed.run(state)

            state["bed_management"] = result.get(
                "statistics",
                {}
            )

            state.setdefault(
                "recommendations",
                []
            ).extend(
                result.get(
                    "recommendations",
                    []
                )
            )

            state.setdefault(
                "ai_outputs",
                {}
            )["bed_management"] = result.get(
                "ai",
                {}
            )

            self.mark_completed(
                state,
                "bed_management"
            )

            logger.success(
                "Bed Management Agent execution completed."
            )

            return state

        except Exception as ex:

            logger.exception(
                "Bed Management execution failed: {}",
                ex
            )

            raise


    # ==========================================================
    # Execute ICU
    # ==========================================================

    def execute_icu(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Executing ICU Agent")

        try:

            result = self.icu.run(state)

            state["icu"] = result.get(
                "statistics",
                {}
            )

            state.setdefault(
                "recommendations",
                []
            ).extend(
                result.get(
                    "recommendations",
                    []
                )
            )

            state.setdefault(
                "ai_outputs",
                {}
            )["icu"] = result.get(
                "ai",
                {}
            )

            self.mark_completed(
                state,
                "icu"
            )

            logger.success(
                "ICU Agent execution completed."
            )

            return state

        except Exception as ex:

            logger.exception(
                "ICU execution failed: {}",
                ex
            )

            raise


    # ==========================================================
    # Execute Finance
    # ==========================================================

    def execute_finance(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("Executing Finance Agent")

        try:

            result = self.finance.run(state)

            state["finance"] = result.get(
                "statistics",
                {}
            )

            state.setdefault(
                "recommendations",
                []
            ).extend(
                result.get(
                    "recommendations",
                    []
                )
            )

            state.setdefault(
                "ai_outputs",
                {}
            )["finance"] = result.get(
                "ai",
                {}
            )

            self.mark_completed(
                state,
                "finance"
            )

            logger.success(
                "Finance Agent execution completed."
            )

            return state

        except Exception as ex:

            logger.exception(
                "Finance execution failed: {}",
                ex
            )

            raise

        # ==========================================================
    # Aggregate Recommendations
    # ==========================================================

    def aggregate_recommendations(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Aggregating recommendations..."
        )

        recommendations = []

        agents = [

            "admissions",

            "bed_management",

            "icu",

            "finance"

        ]

        for agent in agents:

            ai_output = state.get(
                "ai_outputs",
                {}
            ).get(
                agent,
                {}
            )

            recs = ai_output.get(
                "recommendations",
                []
            )

            if isinstance(
                recs,
                list
            ):

                recommendations.extend(
                    recs
                )

        unique = []

        seen = set()

        for rec in recommendations:

            key = str(rec)

            if key not in seen:

                unique.append(rec)

                seen.add(key)

        state["recommendations"] = unique

        logger.success(

            "Total Recommendations : {}",

            len(unique)

        )

        return state


    # ==========================================================
    # Generate Analytics
    # ==========================================================

    def generate_analytics(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        from datetime import datetime

        logger.info(
            "Generating analytics..."
        )

        admissions = state.get(
            "admissions",
            {}
        )

        beds = state.get(
            "bed_management",
            {}
        )

        icu = state.get(
            "icu",
            {}
        )

        finance = state.get(
            "finance",
            {}
        )

        alerts = []

        if beds.get(
            "occupancy_rate",
            0
        ) > 90:

            alerts.append(
                "Hospital bed occupancy exceeds 90%."
            )

        if icu.get(
            "pressure_level",
            ""
        ) == "High":

            alerts.append(
                "ICU operating under high pressure."
            )

        if finance.get(
            "financial_health",
            ""
        ) == "Critical":

            alerts.append(
                "Financial health requires immediate attention."
            )

        state["analytics_response"] = {

            "timestamp":

                datetime.now().isoformat(),

            "hospital_status":

                "Operational"

                if len(alerts) == 0

                else "Attention Required",

            "alerts":

                alerts,

            "kpis": {

                "admissions":

                    admissions,

                "bed_management":

                    beds,

                "icu":

                    icu,

                "finance":

                    finance

            }

        }

        logger.success(
            "Analytics generated successfully."
        )

        return state


    # ==========================================================
    # Generate Executive Summary
    # ==========================================================

    def generate_executive_summary(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Generating executive summary..."
        )

        summaries = []

        risks = []

        confidence_scores = []

        for agent in [

            "admissions",

            "bed_management",

            "icu",

            "finance"

        ]:

            ai = state.get(
                "ai_outputs",
                {}
            ).get(
                agent,
                {}
            )

            if ai.get(
                "summary"
            ):

                summaries.append(
                    ai["summary"]
                )

            if ai.get(
                "risk"
            ):

                risks.append(
                    ai["risk"]
                )

            if ai.get(
                "confidence_score"
            ) is not None:

                confidence_scores.append(

                    ai[
                        "confidence_score"
                    ]

                )

        executive_summary = " ".join(
            summaries
        )

        risk = None

        if "High" in risks:

            risk = "High"

        elif "Medium" in risks:

            risk = "Medium"

        elif risks:

            risk = risks[0]

        confidence = (

            round(

                sum(confidence_scores)

                /

                len(confidence_scores),

                2

            )

            if confidence_scores

            else None

        )

        state["summary"] = {

            "executive_summary":

                executive_summary,

            "predicted_risk":

                risk,

            "confidence_score":

                confidence

        }

        logger.success(
            "Executive summary generated."
        )

        return state

    # ==========================================================
    # Finalize Response
    # ==========================================================

    def finalize_response(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Finalizing Healthcare Command Center response..."
        )

        processing_time = round(

            (
                time.perf_counter()

                -

                state.get(
                    "start_time",
                    time.perf_counter()
                )

            ) * 1000,

            2

        )

        state["metadata"] = {

            "request_id":

                state.get(
                    "request_id",
                    ""
                ),

            "processing_time_ms":

                processing_time,

            "workflow":

                "Healthcare Command Center",

            "agent":

                "Supervisor",

            "model_name":

                "GPT-4.1"

        }

        state["generated_at"] = (
            datetime.now().isoformat()
        )

        state["success"] = True

        state["message"] = (
            "Healthcare Command Center analysis completed successfully."
        )

        state["status"] = "SUCCESS"

        logger.success(
            "Healthcare response finalized."
        )

        return state
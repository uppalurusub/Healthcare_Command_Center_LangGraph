"""
healthcare_graph.py

Enterprise Healthcare Command Center AI

LangGraph Workflow

Responsibilities
----------------
1. Define Healthcare State
2. Register Graph Nodes
3. Build Workflow
4. Compile Graph
5. Execute Workflow
"""

from typing import TypedDict, Dict, Any, List
from datetime import datetime
from app.config.settings import settings
logger = settings.get_logger()

from langgraph.graph import StateGraph
from langgraph.graph import END

from app.agents.supervisor_agent import SupervisorAgent
from app.agents.admissions_agent import AdmissionsAgent
from app.agents.bed_agent import BedManagementAgent
from app.agents.icu_agent import ICUAgent
from app.agents.finance_agent import FinanceAgent


# ==========================================================
# Graph State
# ==========================================================

class HealthcareState(TypedDict):

    hospital_id: str

    user_id: str

    query: str

    analytics: Dict[str, bool]

    filters: Dict[str, Any]

    admissions: Dict[str, Any]

    bed_management: Dict[str, Any]

    icu: Dict[str, Any]

    finance: Dict[str, Any]

    summary: Dict[str, Any]

    recommendations: List[Dict[str, Any]]

    metadata: Dict[str, Any]

    analytics_response: Dict[str, Any]

    next_agent: str

    # These fields must be declared in the LangGraph state schema.
    # Otherwise LangGraph drops them between nodes, causing the supervisor
    # to rebuild the plan and route to Admissions repeatedly.
    execution_plan: List[str]

    completed_agents: List[str]

    ai_outputs: Dict[str, Any]

    start_time: float

    status: str

    error: str

    # Final API fields must be part of the schema or LangGraph may drop them.
    agent: str
    success: bool
    message: str


# ==========================================================
# Healthcare Graph
# ==========================================================

class HealthcareGraph:

    def __init__(self):

        logger.info(
            "Initializing Healthcare Graph..."
        )

        self.supervisor = SupervisorAgent()

        self.admissions = AdmissionsAgent()

        self.bed = BedManagementAgent()

        self.icu = ICUAgent()

        self.finance = FinanceAgent()

        self.workflow = StateGraph(
            HealthcareState
        )

        self._register_nodes()

        self._register_edges()

        self.graph = self.workflow.compile()

        logger.success(
            "Healthcare Graph initialized successfully."
        )

    # ======================================================
    # Register Graph Nodes
    # ======================================================

    def _register_nodes(self):

        logger.info(
            "Registering LangGraph Nodes..."
        )

        self.workflow.add_node(
            "supervisor",
            self.supervisor_node
        )

        self.workflow.add_node(
            "admissions",
            self.admissions_node
        )

        self.workflow.add_node(
            "bed_management",
            self.bed_node
        )

        self.workflow.add_node(
            "icu",
            self.icu_node
        )

        self.workflow.add_node(
            "finance",
            self.finance_node
        )

        self.workflow.add_node(
            "finalize",
            self.finalize_node
        )

        logger.success(
            "All LangGraph nodes registered."
        )

    # ======================================================
    # Register Workflow
    # ======================================================

    def _register_edges(self):

        logger.info(
            "Registering LangGraph Workflow..."
        )

        self.workflow.set_entry_point(
            "supervisor"
        )

        self.workflow.add_conditional_edges(

            "supervisor",

            self.route,

            {

                "admissions": "admissions",

                "bed_management": "bed_management",

                "icu": "icu",

                "finance": "finance",

                "finalize": "finalize"

            }

        )

        self.workflow.add_edge(
            "admissions",
            "supervisor"
        )

        self.workflow.add_edge(
            "bed_management",
            "supervisor"
        )

        self.workflow.add_edge(
            "icu",
            "supervisor"
        )

        self.workflow.add_edge(
            "finance",
            "supervisor"
        )

        self.workflow.add_edge(
            "finalize",
            END
        )

        logger.success(
            "Healthcare Workflow Created."
        )

    
    # ======================================================
    # Route
    # ======================================================

    def route(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Routing -> {}",
            state["next_agent"]
        )

        return state["next_agent"]
    

    # ======================================================
    # Supervisor
    # ======================================================

    def supervisor_node(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Executing Supervisor Agent"
        )

        result = self.supervisor.run(
            state
        )

        state.update(result)

        return state
    

    # ======================================================
    # Admissions
    # ======================================================

    def admissions_node(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Executing Admissions Agent"
        )

        result = self.admissions.run(state)
        self._store_agent_result(state, "admissions", result)
        return state
    

    # ======================================================
    # Bed Management
    # ======================================================

    def bed_node(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Executing Bed Management Agent"
        )

        result = self.bed.run(state)
        self._store_agent_result(state, "bed_management", result)
        return state
    
    # ======================================================
    # ICU Node
    # ======================================================

    def icu_node(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Executing ICU Agent..."
        )

        try:

            result = self.icu.run(state)
            self._store_agent_result(state, "icu", result)

            logger.success("ICU Agent completed successfully.")
            return state

        except Exception as ex:

            logger.exception(
                "ICU Agent Failed : {}",
                ex
            )

            state["status"] = "FAILED"

            state["error"] = str(ex)

            raise

    # ======================================================
    # Finance Node
    # ======================================================

    def finance_node(
        self,
        state: HealthcareState
    ):

        logger.info(
            "Executing Finance Agent..."
        )

        try:

            result = self.finance.run(state)
            self._store_agent_result(state, "finance", result)

            logger.success("Finance Agent completed successfully.")
            return state

        except Exception as ex:

            logger.exception(
                "Finance Agent Failed : {}",
                ex
            )

            state["status"] = "FAILED"

            state["error"] = str(ex)

            raise

    # ======================================================
    # Persist agent outputs and mark each department complete
    # ======================================================

    @staticmethod
    def _store_agent_result(
        state: HealthcareState,
        agent_name: str,
        result: Dict[str, Any],
    ) -> None:
        """Normalize a department agent's tool payload into API-facing metrics.

        Agent result shape:
            {"statistics": {"statistics": {...raw metrics...}, "kpis": {...}},
             "ai": {...}, "recommendations": [...]}
        Keep values sourced from the tool/agent; do not manufacture missing metrics.
        """
        if not isinstance(result, dict):
            raise TypeError(
                f"{agent_name} agent must return a dictionary; "
                f"received {type(result).__name__}"
            )

        agent_payload = result.get("statistics", {})
        if not isinstance(agent_payload, dict):
            raise TypeError(
                f"{agent_name} statistics must be a dictionary; "
                f"received {type(agent_payload).__name__}"
            )

        # The tools return {"statistics": raw_data, "kpis": computed_kpis}.
        # Accept a flat statistics dictionary too, so alternate tools remain compatible.
        raw_stats = agent_payload.get("statistics", agent_payload)
        raw_kpis = agent_payload.get("kpis", {})
        if not isinstance(raw_stats, dict):
            raise TypeError(f"{agent_name} raw statistics must be a dictionary")
        if not isinstance(raw_kpis, dict):
            raw_kpis = {}

        merged = {**raw_stats, **raw_kpis}

        if agent_name == "admissions":
            metrics = {
                "total_admissions": merged.get("total_admissions", merged.get("today_admissions")),
                "emergency_admissions": merged.get("emergency_admissions"),
                "scheduled_admissions": merged.get("scheduled_admissions"),
                "pending_admissions": merged.get("pending_admissions"),
                "waiting_patients": merged.get("waiting_patients"),
                "predicted_next_24_hours": merged.get("predicted_next_24_hours"),
                "average_wait_time_minutes": merged.get("average_wait_time_minutes"),
                "average_length_of_stay": merged.get("average_length_of_stay"),
                "occupancy_pressure": merged.get("occupancy_pressure"),
                "emergency_percentage": merged.get("emergency_percentage"),
                "scheduled_percentage": merged.get("scheduled_percentage"),
            }
            stats_key = "admissions"
        elif agent_name == "bed_management":
            metrics = {
                "total_beds": merged.get("total_beds"),
                "occupied_beds": merged.get("occupied_beds"),
                "available_beds": merged.get("available_beds"),
                "occupancy_rate": merged.get("occupancy_rate"),
                "availability_rate": merged.get("availability_rate"),
                "icu_beds": merged.get("icu_beds"),
                "icu_available": merged.get("icu_available"),
                "icu_utilization": merged.get("icu_utilization"),
                "isolation_beds": merged.get("isolation_beds"),
                "expected_discharges_today": merged.get("expected_discharges_today"),
                "bed_turnover_rate": merged.get("bed_turnover_rate"),
                "pressure_level": merged.get("pressure_level"),
            }
            stats_key = "bed_management"
        elif agent_name == "icu":
            metrics = {
                "total_icu_beds": merged.get("total_icu_beds"),
                "occupied_icu_beds": merged.get("occupied_icu_beds"),
                "available_icu_beds": merged.get("available_icu_beds"),
                "critical_patients": merged.get("critical_patients"),
                "high_risk_patients": merged.get("high_risk_patients"),
                "ventilators_total": merged.get("ventilators_total"),
                "ventilators_in_use": merged.get("ventilators_in_use"),
                "ventilator_utilization": merged.get("ventilator_utilization"),
                "average_length_of_stay": merged.get("average_length_of_stay"),
                "predicted_icu_admissions": merged.get("predicted_icu_admissions"),
                "mortality_risk": merged.get("mortality_risk"),
                "pressure_level": merged.get("pressure_level"),
            }
            stats_key = "icu"
        elif agent_name == "finance":
            metrics = {
                "today_revenue": merged.get("today_revenue"),
                "monthly_revenue": merged.get("monthly_revenue"),
                "operating_cost": merged.get("operating_cost"),
                "insurance_claims": merged.get("insurance_claims"),
                "approved_claims": merged.get("approved_claims"),
                "pending_claims": merged.get("pending_claims"),
                "outstanding_payments": merged.get("outstanding_payments", merged.get("outstanding_receivables")),
                "average_cost_per_patient": merged.get("average_cost_per_patient"),
                "predicted_month_end_revenue": merged.get("predicted_month_end_revenue"),
                "profit": merged.get("profit"),
                "profit_margin": merged.get("profit_margin"),
                "claim_approval_rate": merged.get("claim_approval_rate"),
                "financial_health": merged.get("financial_health"),
            }
            stats_key = "finance"
        else:
            raise ValueError(f"Unknown department agent: {agent_name}")

        # Keep only actual values; None is retained for genuinely unavailable metrics.
        state[stats_key] = metrics
        state.setdefault("ai_outputs", {})[agent_name] = result.get("ai", {})

        recommendations = result.get("recommendations", [])
        if isinstance(recommendations, list):
            state.setdefault("recommendations", []).extend(recommendations)

        completed = state.setdefault("completed_agents", [])
        if agent_name not in completed:
            completed.append(agent_name)

        logger.success(
            "Department output normalized | department={} | populated_metrics={} | completed_agents={}",
            agent_name,
            sum(value is not None for value in metrics.values()),
            completed,
        )

    # ======================================================
    # Finalize Node
    # ======================================================

    def finalize_node(
        self,
        state: HealthcareState
    ):
        """Assemble analytics from department outputs without inventing metrics."""
        logger.info("Building Final Response...")

        ai_outputs = state.get("ai_outputs", {})
        existing_summary = state.get("summary")
        if not isinstance(existing_summary, dict):
            existing_summary = {}

        department_summaries = [
            output.get("summary")
            for output in ai_outputs.values()
            if isinstance(output, dict) and output.get("summary")
        ]
        summary_text = existing_summary.get("executive_summary")
        if not summary_text and department_summaries:
            summary_text = " ".join(str(item) for item in department_summaries)

        # Only expose risk/confidence when an agent actually supplied them.
        risks = [
            output.get("risk")
            for output in ai_outputs.values()
            if isinstance(output, dict) and output.get("risk")
        ]
        confidences = [
            output.get("confidence_score")
            for output in ai_outputs.values()
            if isinstance(output, dict)
            and isinstance(output.get("confidence_score"), (int, float))
        ]
        state["summary"] = {
            "executive_summary": summary_text,
            "predicted_risk": existing_summary.get("predicted_risk") or (risks[0] if risks else None),
            "confidence_score": existing_summary.get("confidence_score") if existing_summary.get("confidence_score") is not None
                else (sum(confidences) / len(confidences) if confidences else None),
        }

        # Recommendations were captured from each department during _store_agent_result.
        recommendations = state.get("recommendations", [])
        if not isinstance(recommendations, list):
            recommendations = []
        state["recommendations"] = recommendations

        selected_departments = [
            name for name, selected in state.get("analytics", {}).items() if selected
        ]
        completed = set(state.get("completed_agents", []))
        missing = [name for name in selected_departments if name not in completed]
        if missing:
            state["status"] = "PARTIAL" if completed else "FAILED"
            state["success"] = False
            state["message"] = (
                "Healthcare Command Center completed with missing department outputs: "
                + ", ".join(missing)
            )
        else:
            state["status"] = "SUCCESS"
            state["success"] = True
            state["message"] = "Healthcare Command Center completed successfully."

        state["analytics_response"] = {
            "timestamp": datetime.now().isoformat(),
            "hospital_status": None,
            "alerts": [
                f"No usable output received from {name}"
                for name in missing
            ],
            "kpis": {
                "admissions": state.get("admissions", {}),
                "bed_management": state.get("bed_management", {}),
                "icu": state.get("icu", {}),
                "finance": state.get("finance", {}),
            },
        }

        original_metadata = state.get("metadata", {})
        if not isinstance(original_metadata, dict):
            original_metadata = {}
        start_time = state.get("start_time")
        elapsed_ms = None
        if isinstance(start_time, (int, float)):
            import time
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        metadata = dict(original_metadata)
        metadata.setdefault("request_id", None)
        metadata["processing_time_ms"] = elapsed_ms
        metadata.setdefault("workflow", "Healthcare Command Center")
        metadata.setdefault("agent", "Supervisor")
        metadata.setdefault("model_name", None)
        state["metadata"] = metadata

        logger.info(
            "Final response assembled | status={} | completed={} | missing={}",
            state["status"],
            sorted(completed),
            missing,
        )
        return state

    # ======================================================
    # Execute Graph
    # ======================================================

    def invoke(
        self,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info(
            "Executing Healthcare LangGraph..."
        )

        try:

            result = self.graph.invoke(state)

            logger.success(
                "Healthcare LangGraph completed successfully."
            )

            return result

        except Exception as ex:

            logger.exception(
                "Healthcare Graph Execution Failed : {}",
                ex
            )

            raise

    async def ainvoke(
        self,
        state: Dict[str, Any]
    ):

        logger.info(
            "Executing Async Healthcare Graph..."
        )

        result = await self.graph.ainvoke(state)

        logger.success(
            "Async Graph completed."
        )

        return result
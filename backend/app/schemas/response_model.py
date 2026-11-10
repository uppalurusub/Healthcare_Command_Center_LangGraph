"""
response_model.py

Healthcare Command Center AI
Response Models
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


# ==========================================================
# Recommendation
# ==========================================================

class Recommendation(BaseModel):
    """A recommendation emitted by a department agent.

    Agents may return either structured recommendations or plain-text
    recommendations. Plain text is preserved as the description; unknown
    priority/title values remain None rather than being fabricated.
    """
    priority: Optional[str] = Field(
        default=None,
        description="High | Medium | Low when supplied by the source agent"
    )
    title: Optional[str] = None
    description: str

    @model_validator(mode="before")
    @classmethod
    def normalize_plain_text(cls, value):
        if isinstance(value, str):
            return {"description": value}
        return value


# ==========================================================
# AI Summary
# ==========================================================

class AISummary(BaseModel):
    executive_summary: Optional[str] = None
    predicted_risk: Optional[str] = None
    confidence_score: Optional[float] = None


# ==========================================================
# Admissions Response
# ==========================================================

class AdmissionsResponse(BaseModel):

    total_admissions: Optional[int] = None

    emergency_admissions: Optional[int] = None

    scheduled_admissions: Optional[int] = None

    pending_admissions: Optional[int] = None

    waiting_patients: Optional[int] = None

    predicted_next_24_hours: Optional[int] = None

    average_wait_time_minutes: Optional[float] = None

    average_length_of_stay: Optional[float] = None

    occupancy_pressure: Optional[float] = None

    emergency_percentage: Optional[float] = None

    scheduled_percentage: Optional[float] = None


# ==========================================================
# Bed Management Response
# ==========================================================

class BedManagementResponse(BaseModel):

    total_beds: Optional[int] = None

    occupied_beds: Optional[int] = None

    available_beds: Optional[int] = None

    occupancy_rate: Optional[float] = None

    availability_rate: Optional[float] = None

    icu_beds: Optional[int] = None

    icu_available: Optional[int] = None

    icu_utilization: Optional[float] = None

    isolation_beds: Optional[int] = None

    expected_discharges_today: Optional[int] = None

    bed_turnover_rate: Optional[float] = None

    pressure_level: Optional[str] = None


# ==========================================================
# ICU Response
# ==========================================================

class ICUResponse(BaseModel):

    total_icu_beds: Optional[int] = None

    occupied_icu_beds: Optional[int] = None

    available_icu_beds: Optional[int] = None

    critical_patients: Optional[int] = None

    high_risk_patients: Optional[int] = None

    ventilators_total: Optional[int] = None

    ventilators_in_use: Optional[int] = None

    ventilator_utilization: Optional[float] = None

    average_length_of_stay: Optional[float] = None

    predicted_icu_admissions: Optional[int] = None

    mortality_risk: Optional[str] = None

    pressure_level: Optional[str] = None


# ==========================================================
# Finance Response
# ==========================================================

class FinanceResponse(BaseModel):

    today_revenue: Optional[float] = None

    monthly_revenue: Optional[float] = None

    operating_cost: Optional[float] = None

    insurance_claims: Optional[int] = None

    approved_claims: Optional[int] = None

    pending_claims: Optional[int] = None

    outstanding_payments: Optional[float] = None

    average_cost_per_patient: Optional[float] = None

    predicted_month_end_revenue: Optional[float] = None

    profit: Optional[float] = None

    profit_margin: Optional[float] = None

    claim_approval_rate: Optional[float] = None

    financial_health: Optional[str] = None


# ==========================================================
# Analytics
# ==========================================================

class AnalyticsResponse(BaseModel):

    timestamp: Optional[str] = None

    hospital_status: Optional[str] = None

    alerts: Optional[List[str]] = None

    kpis: Optional[Dict[str, Any]] = None


# ==========================================================
# Metadata
# ==========================================================

class MetadataResponse(BaseModel):

    request_id: Optional[str] = None

    processing_time_ms: Optional[float] = None

    model_name: Optional[str] = None

    workflow: Optional[str] = None

    agent: Optional[str] = None


# ==========================================================
# Main Response
# ==========================================================

class CommandCenterResponse(BaseModel):

    success: bool

    status: Optional[str] = None

    message: str

    hospital_id: Optional[str] = None

    generated_at: Optional[str] = None


    summary: Optional[AISummary] = None

    admissions: Optional[AdmissionsResponse] = None


    bed_management: Optional[BedManagementResponse] = None


    icu: Optional[ICUResponse] = None


    finance: Optional[FinanceResponse] = None

    analytics: Optional[AnalyticsResponse] = None


    recommendations: Optional[List[Recommendation]] = None


    metadata: Optional[MetadataResponse] = None

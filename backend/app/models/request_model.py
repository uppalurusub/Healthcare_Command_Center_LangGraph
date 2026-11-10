"""
request_model.py

Pydantic Request Models for Healthcare Command Center AI
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class FilterCriteria(BaseModel):
    """
    Filter data for analysis.
    """

    department: Optional[str] = Field(
        default=None,
        description="Department name (ICU, ER, Cardiology, etc.)"
    )

    ward: Optional[str] = Field(
        default=None,
        description="Ward name"
    )

    patient_id: Optional[str] = Field(
        default=None,
        description="Patient Identifier"
    )

    physician: Optional[str] = Field(
        default=None,
        description="Physician Name"
    )

    admission_date: Optional[str] = Field(
        default=None,
        description="Admission Date (YYYY-MM-DD)"
    )

    discharge_date: Optional[str] = Field(
        default=None,
        description="Discharge Date (YYYY-MM-DD)"
    )


class AnalyticsOptions(BaseModel):
    """
    Enable or Disable Analytics
    """

    admissions: bool = True
    bed_management: bool = True
    icu: bool = True
    finance: bool = True


class CommandCenterRequest(BaseModel):
    """
    Main Request Model
    """

    hospital_id: str = Field(
        ...,
        description="Hospital Identifier"
    )

    user_id: Optional[str] = Field(
        default=None,
        description="User requesting the analysis"
    )

    query: str = Field(
        ...,
        description="Natural language question"
    )

    agent: Literal[
        "supervisor",
        "admissions",
        "bed_management",
        "icu",
        "finance"
    ] = Field(
        default="supervisor",
        description="Agent to execute"
    )

    analytics: AnalyticsOptions = Field(
        default_factory=AnalyticsOptions
    )

    filters: Optional[FilterCriteria] = None

    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum records to return"
    )

    include_recommendations: bool = True

    include_predictions: bool = True

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional custom parameters"
    )
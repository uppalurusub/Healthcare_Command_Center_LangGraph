"""
healthcare_router.py

Enterprise Healthcare Command Center AI

FastAPI Router

Responsibilities
----------------
1. Expose REST Endpoints
2. Validate Request
3. Call Healthcare Service
4. Return API Response
5. Health & Readiness Endpoints
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from app.config.settings import settings
logger = settings.get_logger()

from app.models.request_model import (
    CommandCenterRequest,
)

from app.models.response_model import (
    CommandCenterResponse,
)

from app.services.healthcare_service import (
    HealthcareService,
)

# ==========================================================
# Router
# ==========================================================

router = APIRouter(

    prefix="/healthcare",

    tags=["Healthcare Command Center AI"]

)

# ==========================================================
# Dependency Injection
# ==========================================================

def get_healthcare_service() -> HealthcareService:

    return HealthcareService()



# ==========================================================
# Log Request
# ==========================================================

def log_request(
    request: CommandCenterRequest
):

    logger.info(
        "Healthcare API Request"
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

# ==========================================================
# Log Request
# ==========================================================

def log_request(
    request: CommandCenterRequest
):

    logger.info(
        "Healthcare API Request"
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

# ==========================================================
# Constants
# ==========================================================

API_NAME = "Healthcare Command Center AI"

API_VERSION = "1.0.0"

API_DESCRIPTION = (
    "Enterprise Multi-Agent Healthcare Analytics"
)

# ==========================================================
# Healthcare Command Center
# ==========================================================

@router.post(

    "/command-center",

    response_model=CommandCenterResponse,

    summary="Healthcare Command Center AI",

    description="Enterprise Multi-Agent Healthcare Analytics",

    response_description="Healthcare Command Center Response"

)

async def command_center(

    request: CommandCenterRequest,

    http_request: Request,

    service: Annotated[
        HealthcareService,
        Depends(get_healthcare_service)
    ]

) -> CommandCenterResponse:

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center Request Received"
    )

    logger.info(
        "Client : {}",
        http_request.client.host
        if http_request.client
        else "Unknown"
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

    logger.info("=" * 80)

    try:

        response = await service.process_request(
            request
        )

        logger.success(
            "Healthcare Command Center completed successfully."
        )

        logger.info(
            "Status : {}",
            response.status
        )

        return response

    except HTTPException:

        raise

    except ValueError as ex:

        logger.exception(
            "Validation Error : {}",
            ex
        )

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(ex)

        )

    except Exception as ex:

        logger.exception(
            "Healthcare Router Error : {}",
            ex
        )

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail={

                "success": False,

                "status": "FAILED",

                "message": str(ex)

            }

        )
    
# ==========================================================
# Health Check
# ==========================================================

@router.get(

    "/health",

    summary="Health Check",

    description="Healthcare Command Center Health"

)

async def health(

    service: Annotated[
        HealthcareService,
        Depends(get_healthcare_service)
    ]

):

    logger.info(
        "Health Check Request"
    )

    return await service.health_check()

# ==========================================================
# Readiness
# ==========================================================

@router.get(

    "/ready",

    summary="Readiness Check"

)

async def readiness(

    service: Annotated[
        HealthcareService,
        Depends(get_healthcare_service)
    ]

):

    logger.info(
        "Readiness Check Request"
    )

    return await service.readiness_check()

# ==========================================================
# Version
# ==========================================================

@router.get(

    "/version",

    summary="Application Version"

)

async def version():

    logger.info(
        "Version Request"
    )

    return HealthcareService.version()


# ==========================================================
# Supported Agents
# ==========================================================

@router.get(

    "/agents",

    summary="Supported Agents"

)

async def supported_agents():

    logger.info(
        "Supported Agents Request"
    )

    return {

        "agents":

            HealthcareService.supported_agents()

    }


# ==========================================================
# Supported Analytics
# ==========================================================

@router.get(

    "/analytics",

    summary="Supported Analytics"

)

async def supported_analytics():

    logger.info(
        "Supported Analytics Request"
    )

    return {

        "analytics":

            HealthcareService.supported_analytics()

    }

# ==========================================================
# Statistics
# ==========================================================

@router.get(

    "/statistics",

    summary="Application Statistics"

)

async def statistics():

    logger.info(
        "Statistics Request"
    )

    return HealthcareService.statistics()


# ==========================================================
# Root
# ==========================================================

@router.get(

    "/",

    summary="Healthcare Command Center"

)

async def root():

    logger.info(
        "Root Endpoint Accessed"
    )

    return {

        "application":

            API_NAME,

        "version":

            API_VERSION,

        "description":

            API_DESCRIPTION,

        "status":

            "Running"

    }


# ==========================================================
# Startup Banner
# ==========================================================

def router_banner():

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center AI"
    )

    logger.info(
        "Enterprise Multi-Agent Platform"
    )

    logger.info(
        "FastAPI Router Ready"
    )

    logger.info("=" * 80)
"""
main.py

Enterprise Healthcare Command Center AI

Application Entry Point

Architecture

FastAPI
    │
    ▼
Routers
    │
    ▼
Services
    │
    ▼
Implementation
    │
    ▼
Healthcare Graph
    │
    ▼
Supervisor Agent
    │
 ┌──┼─────────────┬─────────────┬────────────┐
 ▼  ▼             ▼             ▼            ▼
Admissions     Bed Mgmt       ICU       Finance

"""

from __future__ import annotations

import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
logger = settings.get_logger()

from app.routers.healthcare_router import router as healthcare_router

from app.services.healthcare_service import HealthcareService

# ==========================================================
# Configure Loguru
# ==========================================================

logger.remove()

logger.add(

    sys.stdout,

    level="INFO",

    colorize=True,

    enqueue=True,

    backtrace=True,

    diagnose=True,

    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

)

logger.add(

    "logs/healthcare.log",

    rotation="25 MB",

    retention="30 days",

    compression="zip",

    enqueue=True,

    level="DEBUG",

    backtrace=True,

    diagnose=True

)

# ==========================================================
# Configure Loguru
# ==========================================================

logger.remove()

logger.add(

    sys.stdout,

    level="INFO",

    colorize=True,

    enqueue=True,

    backtrace=True,

    diagnose=True,

    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

)

logger.add(

    "logs/healthcare.log",

    rotation="25 MB",

    retention="30 days",

    compression="zip",

    enqueue=True,

    level="DEBUG",

    backtrace=True,

    diagnose=True

)

# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center AI Starting..."
    )

    logger.info(
        "Initializing Enterprise Components..."
    )

    logger.success(
        "Healthcare Service Ready."
    )

    logger.success(
        "Healthcare Graph Ready."
    )

    logger.success(
        "Supervisor Agent Ready."
    )

    logger.info("=" * 80)

    api_banner()

    yield

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center AI Stopping..."
    )

    logger.info("=" * 80)


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(

    title="Healthcare Command Center AI",

    description=(
        "Enterprise Multi-Agent Healthcare Analytics "
        "using LangGraph + LangChain"
    ),

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc",

    openapi_url="/openapi.json",

    lifespan=lifespan

)

# ==========================================================
# Register Routers
# ==========================================================

app.include_router(
    healthcare_router
)

APP_NAME = "Healthcare Command Center AI"

APP_VERSION = "1.0.0"

AUTHOR = "Enterprise AI"

DESCRIPTION = (
    "Healthcare Command Center "
    "using LangGraph Multi-Agent Architecture"
)

# ==========================================================
# CORS Middleware
# ==========================================================

from fastapi.middleware.cors import CORSMiddleware

logger.info(
    "Configuring CORS Middleware..."
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

logger.success(
    "CORS Middleware configured."
)

# ==========================================================
# Request Logging Middleware
# ==========================================================

import time

from fastapi import Request


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next
):

    request_id = str(time.time_ns())

    logger.info("=" * 80)

    logger.info(
        "Incoming Request"
    )

    logger.info(
        "Request ID : {}",
        request_id
    )

    logger.info(
        "Method : {}",
        request.method
    )

    logger.info(
        "URL : {}",
        request.url
    )

    logger.info(
        "Client : {}",
        request.client.host
        if request.client
        else "Unknown"
    )

    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed = (
        time.perf_counter() - start_time
    ) * 1000

    response.headers["X-Process-Time"] = (
        f"{elapsed:.2f} ms"
    )

    response.headers["X-Request-ID"] = (
        request_id
    )

    logger.success(
        "Completed {} {} | {} | {:.2f} ms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed
    )

    logger.info("=" * 80)

    return response


# ==========================================================
# Startup Banner
# ==========================================================

def startup_banner():

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center AI"
    )

    logger.info(
        "Enterprise Multi-Agent Platform"
    )

    logger.info(
        "FastAPI + LangGraph + LangChain"
    )

    logger.info(
        "Router → Service → Implementation → Graph"
    )

    logger.info("=" * 80)

# ==========================================================
# Shutdown Banner
# ==========================================================

def shutdown_banner():

    logger.info("=" * 80)

    logger.info(
        "Healthcare Command Center AI Shutdown"
    )

    logger.info("=" * 80)


# ==========================================================
# Global Exception Handler
# ==========================================================

from fastapi.responses import JSONResponse


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        "Unhandled Exception"
    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "status": "FAILED",

            "message": str(exc)

        }

    )


# ==========================================================
# Validation Handler
# ==========================================================

from fastapi.exceptions import RequestValidationError


@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(

    request: Request,

    exc: RequestValidationError

):

    logger.exception(
        "Validation Error"
    )

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "status": "VALIDATION_ERROR",

            "message": exc.errors()

        }

    )

# ==========================================================
# HTTP Exception Handler
# ==========================================================

from fastapi import HTTPException


@app.exception_handler(
    HTTPException
)
async def http_exception_handler(

    request: Request,

    exc: HTTPException

):

    logger.exception(
        "HTTP Exception"
    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "status": "HTTP_ERROR",

            "message": exc.detail

        }

    )


# ==========================================================
# HTTP Exception Handler
# ==========================================================

from fastapi import HTTPException


@app.exception_handler(
    HTTPException
)
async def http_exception_handler(

    request: Request,

    exc: HTTPException

):

    logger.exception(
        "HTTP Exception"
    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "status": "HTTP_ERROR",

            "message": exc.detail

        }

    )

# ==========================================================
# OpenAPI Tags
# ==========================================================

tags_metadata = [

    {
        "name": "Healthcare Command Center AI",

        "description":
            "Enterprise Multi-Agent Healthcare Analytics"

    },

    {
        "name": "Health",

        "description":
            "Application Health APIs"

    },

    {
        "name": "System",

        "description":
            "System Information"

    }

]



# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(

    "/",

    tags=["System"],

    summary="Application Home"

)

async def root():

    logger.info(
        "Root endpoint accessed."
    )

    return {

        "application":

            APP_NAME,

        "version":

            APP_VERSION,

        "description":

            DESCRIPTION,

        "status":

            "Running"

    }


# ==========================================================
# API Information
# ==========================================================

@app.get(

    "/info",

    tags=["System"],

    summary="Application Information"

)

async def info():

    logger.info(
        "Application information requested."
    )

    return {

        "application":

            APP_NAME,

        "version":

            APP_VERSION,

        "author":

            AUTHOR,

        "framework":

            "FastAPI",

        "architecture":

            "Router → Service → Implementation → Graph",

        "graph":

            "LangGraph",

        "agents": [

            "Supervisor",

            "Admissions",

            "Bed Management",

            "ICU",

            "Finance"

        ]

    }

# ==========================================================
# Custom OpenAPI
# ==========================================================

from fastapi.openapi.utils import get_openapi

def custom_openapi():

    if app.openapi_schema:

        return app.openapi_schema

    schema = get_openapi(

        title=APP_NAME,

        version=APP_VERSION,

        description=DESCRIPTION,

        routes=app.routes

    )

    schema["info"]["x-logo"] = {

        "url":
            "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"

    }

    schema["info"]["contact"] = {

        "name":
            "Enterprise AI Team",

        "email":
            "support@hospital.ai"

    }

    schema["info"]["license"] = {

        "name":
            "Apache-2.0"

    }

    app.openapi_schema = schema

    return app.openapi_schema


# ==========================================================
# Metadata
# ==========================================================

@app.get(

    "/metadata",

    tags=["System"],

    summary="API Metadata"

)

async def metadata():

    logger.info(
        "Metadata requested."
    )

    return {

        "title":

            APP_NAME,

        "version":

            APP_VERSION,

        "description":

            DESCRIPTION,

        "documentation":

            "/docs",

        "redoc":

            "/redoc",

        "openapi":

            "/openapi.json"

    }

# ==========================================================
# API Banner
# ==========================================================

def api_banner():

    logger.info("=" * 80)

    logger.info(APP_NAME)

    logger.info(APP_VERSION)

    logger.info(DESCRIPTION)

    logger.info("OpenAPI Documentation : /docs")

    logger.info("ReDoc Documentation : /redoc")

    logger.info("=" * 80)
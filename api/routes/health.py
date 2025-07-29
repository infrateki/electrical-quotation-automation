from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ProQuote API",
        "version": "0.1.0"
    }


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for dependencies."""
    # TODO: Add actual dependency checks (DB, Redis, etc.)
    dependencies = {
        "database": "ready",
        "redis": "ready",
        "neo4j": "ready"
    }
    
    all_ready = all(status == "ready" for status in dependencies.values())
    
    return {
        "ready": all_ready,
        "dependencies": dependencies,
        "timestamp": datetime.utcnow().isoformat()
    }
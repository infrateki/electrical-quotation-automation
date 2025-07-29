from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from api.routes import quotations, agents, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    logger.info("Starting ProQuote API...")
    # Initialize connections, load models, etc.
    yield
    logger.info("Shutting down ProQuote API...")
    # Cleanup connections, save state, etc.


# Create FastAPI app
app = FastAPI(
    title="ProQuote API",
    description="AI-powered electrical quotation automation system",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(quotations.router, prefix="/api/v1/quotations", tags=["quotations"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to ProQuote API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
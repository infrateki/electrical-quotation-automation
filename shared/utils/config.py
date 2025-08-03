"""
Configuration Management for Quotation Automation System

This module provides centralized configuration management using Pydantic Settings.
It handles environment variables, validation, and provides type-safe access to
all application settings across the system.

Author: ProQuote Team
Version: 1.0.0
"""

import os
from typing import List, Optional, Any, Dict
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from functools import lru_cache

from shared.exceptions.custom_exceptions import (
    ConfigurationError,
    MissingEnvironmentVariableError
)


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    
    # PostgreSQL (Primary Database)
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL connection URL"
    )
    DB_POOL_SIZE: int = Field(10, ge=1, le=50)
    DB_MAX_OVERFLOW: int = Field(20, ge=0, le=100)
    DB_POOL_TIMEOUT: int = Field(30, ge=5, le=300)
    
    # Neo4j (Graph Database)
    NEO4J_URI: str = Field(
        ...,
        description="Neo4j connection URI"
    )
    NEO4J_USER: str = Field("neo4j")
    NEO4J_PASSWORD: str = Field(...)
    NEO4J_DATABASE: str = Field("quotation", description="Neo4j database name")
    
    # Redis (Cache & Sessions)
    REDIS_URL: str = Field(
        ...,
        description="Redis connection URL"
    )
    REDIS_POOL_SIZE: int = Field(10, ge=1, le=50)
    REDIS_SOCKET_TIMEOUT: int = Field(5, ge=1, le=30)
    
    @field_validator('DATABASE_URL')
    @classmethod
    def validate_postgres_url(cls, v: str) -> str:
        if not v.startswith(('postgresql://', 'postgresql+asyncpg://')):
            raise ValueError('DATABASE_URL must be a valid PostgreSQL connection string')
        return v
    
    @field_validator('NEO4J_URI')
    @classmethod
    def validate_neo4j_uri(cls, v: str) -> str:
        if not v.startswith(('bolt://', 'neo4j://', 'bolt+s://', 'neo4j+s://')):
            raise ValueError('NEO4J_URI must be a valid Neo4j connection string')
        return v
    
    @field_validator('REDIS_URL')
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        if not v.startswith('redis://'):
            raise ValueError('REDIS_URL must be a valid Redis connection string')
        return v

    model_config = SettingsConfigDict(env_prefix='')


class APISettings(BaseSettings):
    """API server configuration settings"""
    
    # Server Configuration
    API_HOST: str = Field("0.0.0.0")
    API_PORT: int = Field(8000, ge=1000, le=65535)
    API_WORKERS: int = Field(1, ge=1, le=20)
    
    # CORS Settings
    CORS_ORIGINS: List[str] = Field([
        "http://localhost:3000",
        "http://localhost:8080",
        "https://quotation-automation.com"
    ])
    ALLOWED_HOSTS: List[str] = Field(["*"])
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(True)
    RATE_LIMIT_PER_MINUTE: int = Field(60, ge=10, le=1000)
    
    # Request Limits
    MAX_REQUEST_SIZE: int = Field(10 * 1024 * 1024)  # 10MB
    REQUEST_TIMEOUT: int = Field(300, ge=30, le=3600)  # 5 minutes

    model_config = SettingsConfigDict(env_prefix='')


class AISettings(BaseSettings):
    """AI and LLM configuration settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(
        ...,
        description="OpenAI API key for LLM access"
    )
    OPENAI_ORG_ID: Optional[str] = Field(None)
    DEFAULT_LLM_MODEL: str = Field("gpt-4o")
    SIMPLE_AGENT_MODEL: str = Field("gpt-3.5-turbo")
    ADVANCED_AGENT_MODEL: str = Field("gpt-4o")
    
    # Token Limits
    MAX_TOKENS_PER_AGENT: int = Field(2000, ge=100, le=8000)
    MAX_TOTAL_TOKENS_PER_QUOTATION: int = Field(50000, ge=1000, le=200000)
    
    # Alternative LLM (Anthropic Claude)
    ANTHROPIC_API_KEY: Optional[str] = Field(None)
    
    # Vector Database (Pinecone)
    PINECONE_API_KEY: Optional[str] = Field(None)
    PINECONE_ENVIRONMENT: Optional[str] = Field(None)
    PINECONE_INDEX_NAME: str = Field("quotation-components")
    
    @field_validator('OPENAI_API_KEY')
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v.startswith('sk-'):
            raise ValueError('OPENAI_API_KEY must start with "sk-"')
        return v

    model_config = SettingsConfigDict(env_prefix='')


class AgentSettings(BaseSettings):
    """Agent system configuration settings"""
    
    # Agent Execution
    AGENT_TIMEOUT_SECONDS: int = Field(300, ge=30, le=3600)
    AGENT_MAX_RETRIES: int = Field(3, ge=0, le=10)
    AGENT_PARALLEL_LIMIT: int = Field(5, ge=1, le=20)
    
    # Cache Settings
    AGENT_CACHE_ENABLED: bool = Field(True)
    AGENT_CACHE_TTL: int = Field(3600, ge=60, le=86400)  # 1 hour
    
    # Performance Monitoring
    AGENT_METRICS_ENABLED: bool = Field(True)
    AGENT_TRACING_ENABLED: bool = Field(True)

    model_config = SettingsConfigDict(env_prefix='')


class ExternalAPISettings(BaseSettings):
    """External API integration settings"""
    
    # Manufacturer Pricing APIs
    ASCO_API_KEY: Optional[str] = Field(None)
    ASCO_API_URL: str = Field("https://api.asco.com/v1")
    
    SCHNEIDER_API_KEY: Optional[str] = Field(None)
    SCHNEIDER_API_URL: str = Field("https://api.schneider-electric.com/v1")
    
    SQUARE_D_API_KEY: Optional[str] = Field(None)
    SQUARE_D_API_URL: str = Field("https://api.squared.com/v1")
    
    ABB_API_KEY: Optional[str] = Field(None)
    ABB_API_URL: str = Field("https://api.abb.com/v1")
    
    EATON_API_KEY: Optional[str] = Field(None)
    EATON_API_URL: str = Field("https://api.eaton.com/v1")
    
    # Compliance APIs
    NEC_API_KEY: Optional[str] = Field(None)
    NEC_API_URL: str = Field("https://api.neccode.org/v1")
    
    # Pricing Configuration
    PRICING_CACHE_TTL: int = Field(3600, ge=300, le=86400)  # 1 hour
    PRICING_API_TIMEOUT: int = Field(30, ge=5, le=120)
    PRICING_BATCH_SIZE: int = Field(50, ge=1, le=500)

    model_config = SettingsConfigDict(env_prefix='')


class SecuritySettings(BaseSettings):
    """Security configuration settings"""
    
    # JWT Configuration
    SECRET_KEY: str = Field(
        ...,
        description="Secret key for JWT token signing"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, ge=5, le=1440)
    ALGORITHM: str = Field("HS256")
    
    # Security Headers
    SECURE_HEADERS_ENABLED: bool = Field(True)
    HTTPS_ONLY: bool = Field(False)  # Set to True in production
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        return v

    model_config = SettingsConfigDict(env_prefix='')


class MonitoringSettings(BaseSettings):
    """Monitoring and observability settings"""
    
    # Logging
    LOG_LEVEL: str = Field("INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    LOG_FORMAT: str = Field("json", pattern=r"^(json|text)$")
    LOG_FILE: Optional[str] = Field(None)
    
    # Metrics
    PROMETHEUS_ENABLED: bool = Field(True)
    PROMETHEUS_PORT: int = Field(8001, ge=8000, le=9000)
    
    # Error Tracking
    SENTRY_DSN: Optional[str] = Field(None)
    SENTRY_ENVIRONMENT: str = Field("development")
    
    # Tracing
    TRACING_ENABLED: bool = Field(True)
    TRACING_SAMPLE_RATE: float = Field(0.1, ge=0.0, le=1.0)

    model_config = SettingsConfigDict(env_prefix='')


class FileStorageSettings(BaseSettings):
    """File storage configuration"""
    
    # Local Storage
    UPLOAD_DIRECTORY: str = Field("./uploads")
    MAX_FILE_SIZE: int = Field(10 * 1024 * 1024)  # 10MB
    
    # AWS S3 (Optional)
    AWS_ACCESS_KEY_ID: Optional[str] = Field(None)
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(None)
    AWS_REGION: str = Field("us-east-1")
    AWS_S3_BUCKET: Optional[str] = Field(None)
    
    @field_validator('UPLOAD_DIRECTORY')
    @classmethod
    def validate_upload_directory(cls, v: str) -> str:
        # Create directory if it doesn't exist
        Path(v).mkdir(parents=True, exist_ok=True)
        return v

    model_config = SettingsConfigDict(env_prefix='')


class Settings(BaseSettings):
    """
    Main application settings that combines all configuration sections.
    
    This class loads configuration from environment variables and provides
    validation, type safety, and easy access to all settings throughout
    the application.
    """
    
    # Application Metadata
    APP_NAME: str = Field("ProQuote - Electrical Quotation Automation")
    APP_VERSION: str = Field("1.0.0")
    ENVIRONMENT: str = Field("development", pattern=r"^(development|staging|production)$")
    DEBUG: bool = Field(False)
    
    # Development Settings
    RELOAD_ON_CHANGE: bool = Field(False)
    ENABLE_DEBUG_TOOLBAR: bool = Field(False)
    
    # Nested Settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: APISettings = Field(default_factory=APISettings)
    ai: AISettings = Field(default_factory=AISettings)
    agents: AgentSettings = Field(default_factory=AgentSettings)
    external_apis: ExternalAPISettings = Field(default_factory=ExternalAPISettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    file_storage: FileStorageSettings = Field(default_factory=FileStorageSettings)
    
    # Convenience properties for backward compatibility
    @property
    def DATABASE_URL(self) -> str:
        return self.database.DATABASE_URL
    
    @property
    def NEO4J_URI(self) -> str:
        return self.database.NEO4J_URI
    
    @property
    def REDIS_URL(self) -> str:
        return self.database.REDIS_URL
    
    @property
    def OPENAI_API_KEY(self) -> str:
        return self.ai.OPENAI_API_KEY
    
    @property
    def SECRET_KEY(self) -> str:
        return self.security.SECRET_KEY
    
    @property
    def LOG_LEVEL(self) -> str:
        return self.monitoring.LOG_LEVEL
    
    @property
    def API_HOST(self) -> str:
        return self.api.API_HOST
    
    @property
    def API_PORT(self) -> int:
        return self.api.API_PORT
    
    @property
    def API_WORKERS(self) -> int:
        return self.api.API_WORKERS
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.api.CORS_ORIGINS
    
    @property
    def ALLOWED_HOSTS(self) -> List[str]:
        return self.api.ALLOWED_HOSTS
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    def validate_required_settings(self) -> None:
        """
        Validate that all required settings are properly configured.
        Raises ConfigurationError if any critical settings are missing.
        """
        critical_settings = [
            ("DATABASE_URL", self.database.DATABASE_URL),
            ("NEO4J_URI", self.database.NEO4J_URI),
            ("REDIS_URL", self.database.REDIS_URL),
            ("OPENAI_API_KEY", self.ai.OPENAI_API_KEY),
            ("SECRET_KEY", self.security.SECRET_KEY),
        ]
        
        missing_settings = []
        for setting_name, setting_value in critical_settings:
            if not setting_value:
                missing_settings.append(setting_name)
        
        if missing_settings:
            raise MissingEnvironmentVariableError(
                f"Missing required environment variables: {', '.join(missing_settings)}"
            )
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration for SQLAlchemy"""
        return {
            "url": self.database.DATABASE_URL,
            "pool_size": self.database.DB_POOL_SIZE,
            "max_overflow": self.database.DB_MAX_OVERFLOW,
            "pool_timeout": self.database.DB_POOL_TIMEOUT,
            "echo": self.DEBUG,
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration"""
        return {
            "url": self.database.REDIS_URL,
            "socket_timeout": self.database.REDIS_SOCKET_TIMEOUT,
            "connection_pool_kwargs": {
                "max_connections": self.database.REDIS_POOL_SIZE
            }
        }
    
    def get_neo4j_config(self) -> Dict[str, Any]:
        """Get Neo4j configuration"""
        return {
            "uri": self.database.NEO4J_URI,
            "auth": (self.database.NEO4J_USER, self.database.NEO4J_PASSWORD),
            "database": self.database.NEO4J_DATABASE,
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT == "development"


# ===================================================================
# SETTINGS INSTANCE AND UTILITIES
# ===================================================================

def load_settings() -> Settings:
    """
    Load and validate application settings.
    
    Returns:
        Validated Settings instance
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    try:
        settings = Settings()
        settings.validate_required_settings()
        return settings
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load application settings: {str(e)}",
            original_error=e
        )


# Use lru_cache to ensure we only create one settings instance
@lru_cache()
def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    This function is useful for dependency injection in FastAPI
    and for testing with override settings.
    """
    return load_settings()


def override_settings(**kwargs) -> Settings:
    """
    Create a new settings instance with overridden values.
    Useful for testing.
    
    Args:
        **kwargs: Settings to override
        
    Returns:
        New Settings instance with overrides
    """
    return Settings(**kwargs)


# ===================================================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# ===================================================================

def get_test_settings() -> Settings:
    """Get settings configured for testing"""
    return Settings(
        ENVIRONMENT="development",
        DEBUG=True,
        DATABASE_URL="postgresql+asyncpg://test:test@localhost:5432/quotation_test_db",
        NEO4J_URI="bolt://localhost:7687",
        NEO4J_PASSWORD="test_password",
        REDIS_URL="redis://localhost:6379/1",
        OPENAI_API_KEY="sk-test-key-for-testing",
        SECRET_KEY="test-secret-key-minimum-32-characters-long",
    )


def get_development_settings() -> Settings:
    """Get settings configured for development"""
    return Settings(
        ENVIRONMENT="development",
        DEBUG=True,
        RELOAD_ON_CHANGE=True,
        ENABLE_DEBUG_TOOLBAR=True,
    )


def get_production_settings() -> Settings:
    """Get settings configured for production"""
    return Settings(
        ENVIRONMENT="production",
        DEBUG=False,
        RELOAD_ON_CHANGE=False,
        HTTPS_ONLY=True,
        SECURE_HEADERS_ENABLED=True,
    )


# ===================================================================
# EXAMPLE USAGE
# ===================================================================

"""
Example usage:

from shared.utils.config import get_settings

settings = get_settings()

# Access settings
database_url = settings.database.DATABASE_URL
openai_key = settings.ai.OPENAI_API_KEY

# In FastAPI
from fastapi import Depends

@app.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
"""

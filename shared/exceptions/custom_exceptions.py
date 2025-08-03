"""
Custom Exceptions for Quotation Automation System

This module defines all custom exceptions used throughout the application.
Exceptions are categorized by type and include context information for debugging.

Author: ProQuote Team
Version: 1.0.0
"""

from typing import Optional, Dict, Any
from datetime import datetime
import traceback
from enum import Enum


class ErrorSeverity(Enum):
    """Severity levels for errors"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categories of errors for better organization"""
    CONFIGURATION = "configuration"
    DATABASE = "database"
    AGENT = "agent"
    EXTERNAL_API = "external_api"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NETWORK = "network"
    FILE_OPERATION = "file_operation"


# ===================================================================
# BASE EXCEPTIONS
# ===================================================================

class QuotationAutomationException(Exception):
    """
    Base exception for all custom exceptions in the quotation automation system.
    
    Attributes:
        message: Error message
        error_code: Unique error code for tracking
        severity: Severity level of the error
        category: Category of the error
        context: Additional context information
        timestamp: When the error occurred
        original_error: The original exception if this wraps another error
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.BUSINESS_LOGIC,
        context: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self._generate_error_code()
        self.severity = severity
        self.category = category
        self.context = context or {}
        self.timestamp = datetime.utcnow()
        self.original_error = original_error
        self.traceback = traceback.format_exc() if original_error else None
    
    def _generate_error_code(self) -> str:
        """Generate a unique error code based on category and timestamp"""
        return f"{self.category.value.upper()}_{int(self.timestamp.timestamp())}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging and API responses"""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "severity": self.severity.value,
            "category": self.category.value,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback
        }


# ===================================================================
# CONFIGURATION EXCEPTIONS
# ===================================================================

class ConfigurationError(QuotationAutomationException):
    """Raised when there are configuration issues"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.CONFIGURATION,
            **kwargs
        )


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when required environment variables are missing"""
    
    def __init__(self, message: str, variable_name: Optional[str] = None, **kwargs):
        context = {"variable_name": variable_name} if variable_name else {}
        super().__init__(
            message=message,
            error_code=f"ENV_MISSING_{variable_name}" if variable_name else "ENV_MISSING",
            severity=ErrorSeverity.CRITICAL,
            context=context,
            **kwargs
        )


# ===================================================================
# DATABASE EXCEPTIONS
# ===================================================================

class DatabaseError(QuotationAutomationException):
    """Base class for database-related errors"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.DATABASE,
            **kwargs
        )


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails"""
    
    def __init__(self, message: str, database_type: str, **kwargs):
        super().__init__(
            message=message,
            severity=ErrorSeverity.CRITICAL,
            context={"database_type": database_type},
            **kwargs
        )


class DatabaseQueryError(DatabaseError):
    """Raised when database query fails"""
    
    def __init__(self, message: str, query: Optional[str] = None, **kwargs):
        context = {"query": query[:500]} if query else {}  # Limit query length for logging
        super().__init__(
            message=message,
            severity=ErrorSeverity.HIGH,
            context=context,
            **kwargs
        )


class RecordNotFoundError(DatabaseError):
    """Raised when a database record is not found"""
    
    def __init__(self, entity_type: str, entity_id: Any, **kwargs):
        super().__init__(
            message=f"{entity_type} with id {entity_id} not found",
            error_code=f"NOT_FOUND_{entity_type.upper()}",
            severity=ErrorSeverity.LOW,
            context={"entity_type": entity_type, "entity_id": str(entity_id)},
            **kwargs
        )


# ===================================================================
# AGENT EXCEPTIONS
# ===================================================================

class AgentError(QuotationAutomationException):
    """Base class for agent-related errors"""
    
    def __init__(self, message: str, agent_name: str, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.AGENT,
            context={"agent_name": agent_name},
            **kwargs
        )


class AgentExecutionError(AgentError):
    """Raised when agent execution fails"""
    
    def __init__(self, message: str, agent_name: str, execution_step: Optional[str] = None, **kwargs):
        context = {"agent_name": agent_name, "execution_step": execution_step}
        super().__init__(
            message=message,
            agent_name=agent_name,
            severity=ErrorSeverity.HIGH,
            context=context,
            **kwargs
        )


class AgentTimeoutError(AgentError):
    """Raised when agent execution times out"""
    
    def __init__(self, agent_name: str, timeout_seconds: int, **kwargs):
        super().__init__(
            message=f"Agent {agent_name} timed out after {timeout_seconds} seconds",
            agent_name=agent_name,
            error_code=f"TIMEOUT_{agent_name.upper()}",
            severity=ErrorSeverity.HIGH,
            context={"timeout_seconds": timeout_seconds},
            **kwargs
        )


class AgentDependencyError(AgentError):
    """Raised when agent dependencies are not met"""
    
    def __init__(self, agent_name: str, missing_dependency: str, **kwargs):
        super().__init__(
            message=f"Agent {agent_name} is missing dependency: {missing_dependency}",
            agent_name=agent_name,
            error_code="AGENT_DEPENDENCY_ERROR",
            severity=ErrorSeverity.HIGH,
            context={"missing_dependency": missing_dependency},
            **kwargs
        )


class AgentStateError(AgentError):
    """Raised when agent state is invalid"""
    
    def __init__(self, agent_name: str, state_issue: str, current_state: Optional[Dict] = None, **kwargs):
        super().__init__(
            message=f"Agent {agent_name} has invalid state: {state_issue}",
            agent_name=agent_name,
            error_code="AGENT_STATE_ERROR",
            severity=ErrorSeverity.MEDIUM,
            context={"state_issue": state_issue, "current_state": current_state},
            **kwargs
        )


# ===================================================================
# EXTERNAL API EXCEPTIONS
# ===================================================================

class ExternalAPIError(QuotationAutomationException):
    """Base class for external API errors"""
    
    def __init__(self, message: str, api_name: str, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.EXTERNAL_API,
            context={"api_name": api_name},
            **kwargs
        )


class APIConnectionError(ExternalAPIError):
    """Raised when connection to external API fails"""
    
    def __init__(self, api_name: str, endpoint: str, **kwargs):
        super().__init__(
            message=f"Failed to connect to {api_name} API at {endpoint}",
            api_name=api_name,
            error_code=f"API_CONN_{api_name.upper()}",
            severity=ErrorSeverity.HIGH,
            context={"endpoint": endpoint},
            **kwargs
        )


class APIRateLimitError(ExternalAPIError):
    """Raised when API rate limit is exceeded"""
    
    def __init__(self, api_name: str, reset_time: Optional[datetime] = None, **kwargs):
        super().__init__(
            message=f"Rate limit exceeded for {api_name} API",
            api_name=api_name,
            error_code=f"RATE_LIMIT_{api_name.upper()}",
            severity=ErrorSeverity.MEDIUM,
            context={"reset_time": reset_time.isoformat() if reset_time else None},
            **kwargs
        )


class APIResponseError(ExternalAPIError):
    """Raised when API response is invalid or unexpected"""
    
    def __init__(self, api_name: str, status_code: int, response_body: Optional[str] = None, **kwargs):
        super().__init__(
            message=f"Invalid response from {api_name} API: {status_code}",
            api_name=api_name,
            error_code=f"API_RESP_{api_name.upper()}_{status_code}",
            severity=ErrorSeverity.MEDIUM,
            context={"status_code": status_code, "response_body": response_body[:500] if response_body else None},
            **kwargs
        )


# ===================================================================
# VALIDATION EXCEPTIONS
# ===================================================================

class ValidationError(QuotationAutomationException):
    """Base class for validation errors"""
    
    def __init__(self, message: str, field_name: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            context={"field_name": field_name} if field_name else {},
            **kwargs
        )


class InputValidationError(ValidationError):
    """Raised when input data validation fails"""
    
    def __init__(self, field_name: str, value: Any, constraint: str, **kwargs):
        super().__init__(
            message=f"Validation failed for field '{field_name}': {constraint}",
            field_name=field_name,
            error_code=f"INVALID_{field_name.upper()}",
            context={"field_name": field_name, "value": str(value)[:100], "constraint": constraint},
            **kwargs
        )


class BusinessRuleViolationError(ValidationError):
    """Raised when business rules are violated"""
    
    def __init__(self, rule_name: str, rule_description: str, **kwargs):
        super().__init__(
            message=f"Business rule '{rule_name}' violated: {rule_description}",
            error_code=f"RULE_{rule_name.upper()}",
            severity=ErrorSeverity.MEDIUM,
            context={"rule_name": rule_name, "rule_description": rule_description},
            **kwargs
        )


# ===================================================================
# BUSINESS LOGIC EXCEPTIONS
# ===================================================================

class QuotationError(QuotationAutomationException):
    """Base class for quotation-specific errors"""
    
    def __init__(self, message: str, quotation_id: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.BUSINESS_LOGIC,
            context={"quotation_id": quotation_id} if quotation_id else {},
            **kwargs
        )


class InsufficientDataError(QuotationError):
    """Raised when there's insufficient data to generate quotation"""
    
    def __init__(self, missing_data_type: str, **kwargs):
        super().__init__(
            message=f"Insufficient data to generate quotation: missing {missing_data_type}",
            error_code="INSUFFICIENT_DATA",
            severity=ErrorSeverity.MEDIUM,
            context={"missing_data_type": missing_data_type},
            **kwargs
        )


class ComplianceError(QuotationError):
    """Raised when compliance requirements are not met"""
    
    def __init__(self, compliance_type: str, requirement: str, **kwargs):
        super().__init__(
            message=f"Compliance requirement not met: {compliance_type} - {requirement}",
            error_code=f"COMPLIANCE_{compliance_type.upper()}",
            severity=ErrorSeverity.HIGH,
            context={"compliance_type": compliance_type, "requirement": requirement},
            **kwargs
        )


class PricingError(QuotationError):
    """Raised when pricing calculation fails"""
    
    def __init__(self, component: str, reason: str, **kwargs):
        super().__init__(
            message=f"Pricing error for {component}: {reason}",
            error_code="PRICING_ERROR",
            severity=ErrorSeverity.HIGH,
            context={"component": component, "reason": reason},
            **kwargs
        )


# ===================================================================
# AUTHENTICATION & AUTHORIZATION EXCEPTIONS
# ===================================================================

class AuthenticationError(QuotationAutomationException):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.AUTHENTICATION,
            error_code="AUTH_FAILED",
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class AuthorizationError(QuotationAutomationException):
    """Raised when authorization fails"""
    
    def __init__(self, resource: str, action: str, **kwargs):
        super().__init__(
            message=f"Not authorized to {action} {resource}",
            category=ErrorCategory.AUTHORIZATION,
            error_code="AUTHZ_FAILED",
            severity=ErrorSeverity.MEDIUM,
            context={"resource": resource, "action": action},
            **kwargs
        )


# ===================================================================
# FILE OPERATION EXCEPTIONS
# ===================================================================

class FileOperationError(QuotationAutomationException):
    """Base class for file operation errors"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.FILE_OPERATION,
            context={"file_path": file_path} if file_path else {},
            **kwargs
        )


class FileNotFoundError(FileOperationError):
    """Raised when a required file is not found"""
    
    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            message=f"File not found: {file_path}",
            file_path=file_path,
            error_code="FILE_NOT_FOUND",
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )


class FileParsingError(FileOperationError):
    """Raised when file parsing fails"""
    
    def __init__(self, file_path: str, file_type: str, parse_error: str, **kwargs):
        super().__init__(
            message=f"Failed to parse {file_type} file: {parse_error}",
            file_path=file_path,
            error_code=f"PARSE_{file_type.upper()}",
            severity=ErrorSeverity.MEDIUM,
            context={"file_type": file_type, "parse_error": parse_error},
            **kwargs
        )


# ===================================================================
# NETWORK EXCEPTIONS
# ===================================================================

class NetworkError(QuotationAutomationException):
    """Base class for network-related errors"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class ConnectionTimeoutError(NetworkError):
    """Raised when network connection times out"""
    
    def __init__(self, service_name: str, timeout_seconds: int, **kwargs):
        super().__init__(
            message=f"Connection to {service_name} timed out after {timeout_seconds} seconds",
            error_code="CONN_TIMEOUT",
            context={"service_name": service_name, "timeout_seconds": timeout_seconds},
            **kwargs
        )


# ===================================================================
# ERROR HANDLING UTILITIES
# ===================================================================

def handle_exception(exception: Exception, logger=None) -> Dict[str, Any]:
    """
    Utility function to handle exceptions consistently across the application.
    
    Args:
        exception: The exception to handle
        logger: Optional logger instance
        
    Returns:
        Dictionary representation of the error for API responses
    """
    if isinstance(exception, QuotationAutomationException):
        error_dict = exception.to_dict()
    else:
        # Handle unexpected exceptions
        error_dict = {
            "error_type": exception.__class__.__name__,
            "message": str(exception),
            "error_code": "UNEXPECTED_ERROR",
            "severity": ErrorSeverity.HIGH.value,
            "category": ErrorCategory.BUSINESS_LOGIC.value,
            "timestamp": datetime.utcnow().isoformat(),
            "traceback": traceback.format_exc()
        }
    
    if logger:
        if error_dict.get("severity") in [ErrorSeverity.HIGH.value, ErrorSeverity.CRITICAL.value]:
            logger.error(f"Error occurred: {error_dict}")
        else:
            logger.warning(f"Warning: {error_dict}")
    
    return error_dict

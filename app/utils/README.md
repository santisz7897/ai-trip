# Logging System Documentation

This document explains how to use the logging system in the Japan Honeymoon Travel Assistant project.

## Overview

Our logging system is built on Python's standard `logging` library, with several enhancements:

- Structured logging with JSON support
- Automatic log rotation (size and time-based)
- Request ID tracking across logs
- Integration with FastAPI
- Multiple output formats (console, file, JSON)
- Contextual logging

## Basic Usage

Here's how to use the logging system in your code:

```python
from app.utils.logger import get_app_logger

# Create a logger with a module name
logger = get_app_logger("your_module_name")

# Log at different levels
logger.debug("This is debug information")
logger.info("This is general information")
logger.warning("This is a warning")
logger.error("This is an error")

# Log exceptions with traceback
try:
    # some code that might raise an exception
    result = 1 / 0
except Exception:
    logger.exception("An error occurred")
```

## FastAPI Request Logging

For API endpoints, you can use request-aware logging:

```python
from fastapi import FastAPI, Request
from app.utils.middleware import get_request_logger

@app.get("/example")
async def example_endpoint(request: Request):
    # Get a logger with request context
    logger = get_request_logger(request)
    
    # Log with request context (request_id, client_ip, etc.)
    logger.info("Processing example request")
    
    # Your endpoint logic here
    return {"result": "success"}
```

## Structured Logging

Add structured context to your log messages:

```python
# Log with extra context fields
logger.info(
    "User authenticated", 
    extra={
        "user_id": "user123",
        "login_method": "oauth",
        "user_role": "admin"
    }
)

# Log performance metrics
logger.info(
    "Database operation completed",
    extra={
        "operation": "query",
        "table": "users",
        "duration_ms": 45.2,
        "rows_affected": 10
    }
)
```

## Configuration

The logging system is configured automatically when you use `get_app_logger()`. The log level can be set via the `LOG_LEVEL` environment variable:

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG

# Set log level to ERROR
export LOG_LEVEL=ERROR
```

Valid log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## Log Files

Logs are stored in the `logs/` directory at the project root:

- Text logs: `logs/app_module_name.log`
- JSON logs: `logs/app_module_name_json.log` (if enabled)

Log files are automatically rotated:
- By default, size-based rotation occurs when a log file reaches ~10MB
- Time-based rotation is available by using the appropriate handler

## Custom Loggers

If you need a custom logger with special configuration:

```python
from app.utils.logger import setup_logger
import logging

# Create a custom logger with time-based rotation
custom_logger = setup_logger(
    name="custom_service",
    log_level=logging.DEBUG,
    log_file="/path/to/custom.log",
    rotation_type="time",  # Rotate at midnight
    use_json=False,  # Use text format
    add_console_handler=True  # Also log to console
)
```

## JSON Logging

For structured data logging or log aggregation, you can use JSON formatting:

```python
from app.utils.logger import setup_logger

# Create a JSON logger
json_logger = setup_logger(
    name="transactions",
    log_file="/path/to/transactions.log",
    use_json=True,  # Enable JSON formatting
    add_console_handler=False  # JSON only to file
)

# Log structured data
json_logger.info(
    "Payment processed", 
    extra={
        "transaction_id": "tx-12345",
        "amount": 99.95,
        "currency": "USD",
        "payment_method": "credit_card",
        "status": "success"
    }
)
```

## Middleware Integration

The logging system includes middleware for automatic request/response logging. This is already set up in `main.py`:

```python
from app.utils.middleware import RequestLoggingMiddleware

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)
```

This middleware:
1. Generates a unique request ID for each request
2. Logs request details when a request starts
3. Logs response details when a request completes
4. Logs exceptions if a request fails
5. Adds request ID to response headers for tracking

## Best Practices

1. **Use appropriate log levels:**
   - `DEBUG`: Detailed information for debugging
   - `INFO`: General information about application progress
   - `WARNING`: Indication of potential issues
   - `ERROR`: Error conditions that should be investigated
   - `CRITICAL`: Critical errors requiring immediate attention

2. **Include context in log messages:**
   - Add relevant IDs (user ID, request ID, transaction ID)
   - Include operation details (what was being attempted)
   - Add performance metrics when relevant

3. **Structure log messages consistently:**
   - Start with a verb (Processing, Completed, Failed)
   - Include the entity being operated on
   - Keep messages concise but descriptive

4. **Log at key points:**
   - Application startup/shutdown
   - Beginning and end of important operations
   - Authentication/authorization events
   - Data modifications
   - External service interactions
   - Errors and exceptions

## Examples

See `app/utils/log_examples.py` for more detailed examples of using the logging system. 
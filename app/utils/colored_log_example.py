"""
Example demonstrating colored logging output.
Run this file directly to see colorful logs in action.
"""

from app.utils.logger import get_app_logger


def show_colored_logs():
    # Get a logger with colored console output
    logger = get_app_logger("colors")

    # Show logs at all levels
    logger.debug("This is a DEBUG message (blue)")
    logger.info("This is an INFO message (green)")
    logger.warning("This is a WARNING message (yellow)")
    logger.error("This is an ERROR message (red)")
    logger.critical("This is a CRITICAL message (bold red)")

    # Demonstrate structured logging
    logger.info(
        "Structured log with context",
        extra={"user_id": "user_123", "page": "home", "action": "view"},
    )

    # Demonstrate exception logging
    try:
        # Intentional error to trigger exception
        _ = 100 / 0  # Using _ to indicate intentionally unused variable
    except Exception:
        logger.exception("This is an exception with traceback (red)")


if __name__ == "__main__":
    print("Running colored logging example...")
    show_colored_logs()
    print("\nExample complete. Check the logs directory for log files.")
    print("Note: Colors only appear in terminal output, not in log files.")

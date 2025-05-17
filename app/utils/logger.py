import logging
import os
import sys
import json
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """
    Formatter that adds color to console logs based on log level and displays extra context.
    """

    # Color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD_RED = "\033[1;91m"
    RESET = "\033[0m"
    GRAY = "\033[90m"

    # Format string with extra context
    BASE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: BLUE + BASE_FORMAT + RESET,
        logging.INFO: GREEN + BASE_FORMAT + RESET,
        logging.WARNING: YELLOW + BASE_FORMAT + RESET,
        logging.ERROR: RED + BASE_FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + BASE_FORMAT + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        result = formatter.format(record)

        # Add extra context as gray text if present
        extra_data = {
            key: value
            for key, value in record.__dict__.items()
            if key
            not in [
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "id",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            ]
        }

        if extra_data:
            extra_formatted = " ".join(f"{k}={v}" for k, v in extra_data.items())
            result += f" {self.GRAY}[{extra_formatted}]{self.RESET}"

        return result


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the log record.
    """

    def __init__(self, **kwargs):
        self.fmt_dict = kwargs

    def format(self, record: logging.LogRecord) -> str:
        record_dict = self.__get_record_dict(record)
        return json.dumps(record_dict, ensure_ascii=False)

    def __get_record_dict(self, record: logging.LogRecord) -> dict:
        record_dict = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Include exception info if present
        if record.exc_info:
            record_dict["exception"] = self.formatException(record.exc_info)

        # Include custom fields from the log record
        for key, value in self.fmt_dict.items():
            if hasattr(record, key):
                record_dict[key] = getattr(record, key)

        # Include any extra attributes that were passed via the extra parameter
        for key, value in record.__dict__.items():
            if key not in [
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "id",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            ]:
                record_dict[key] = value

        return record_dict


def get_console_handler(use_colors=True) -> logging.Handler:
    """Returns a console handler for the logger."""
    console_handler = logging.StreamHandler(sys.stdout)

    if use_colors and sys.stdout.isatty():  # Only use colors when in a real terminal
        console_handler.setFormatter(ColoredFormatter())
    else:
        console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        console_handler.setFormatter(logging.Formatter(console_format))

    return console_handler


def get_file_handler(
    log_file: str, max_bytes: int = 10485760, backup_count: int = 20
) -> logging.Handler:
    """Returns a file handler for the logger with size-based rotation."""
    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_handler.setFormatter(logging.Formatter(file_format))
    return file_handler


def get_timed_file_handler(
    log_file: str, when: str = "midnight", interval: int = 1, backup_count: int = 30
) -> logging.Handler:
    """Returns a file handler for the logger with time-based rotation."""
    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = TimedRotatingFileHandler(
        log_file, when=when, interval=interval, backupCount=backup_count
    )
    file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_handler.setFormatter(logging.Formatter(file_format))
    return file_handler


def get_json_file_handler(
    log_file: str, max_bytes: int = 10485760, backup_count: int = 20
) -> logging.Handler:
    """Returns a file handler that logs in JSON format with size-based rotation."""
    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(JsonFormatter())
    return file_handler


def setup_logger(
    name: str,
    log_level: int = logging.INFO,
    log_file: str | None = None,
    use_json: bool = False,
    add_console_handler: bool = True,
    rotation_type: str = "size",
    use_colors: bool = True,
) -> logging.Logger:
    """
    Sets up and returns a logger with the specified configuration.

    Args:
        name (str): Name of the logger
        log_level (int, optional): Logging level. Defaults to logging.INFO.
        log_file (str, optional): Path to log file. If None, only console logging is used.
        use_json (bool, optional): Whether to use JSON formatting for file logs. Defaults to False.
        add_console_handler (bool, optional): Whether to add a console handler. Defaults to True.
        rotation_type (str, optional): Type of log rotation ('size' or 'time'). Defaults to 'size'.
        use_colors (bool, optional): Whether to use colors in console output. Defaults to True.

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name=name)

    # Clear any existing handlers
    logger.handlers = []

    logger.setLevel(level=log_level)

    # Add console handler if requested
    if add_console_handler:
        logger.addHandler(hdlr=get_console_handler(use_colors=use_colors))

    # Add file handler if log file is specified
    if log_file:
        if use_json:
            logger.addHandler(hdlr=get_json_file_handler(log_file=log_file))
        elif rotation_type == "time":
            logger.addHandler(hdlr=get_timed_file_handler(log_file=log_file))
        else:  # 'size' is the default
            logger.addHandler(hdlr=get_file_handler(log_file=log_file))

    # Prevent propagation to the root logger
    logger.propagate = False

    return logger


# Default application-wide logger configuration
def get_app_logger(module_name: str | None = None) -> logging.Logger:
    """
    Gets an application-wide logger with a standardized configuration.

    Args:
        module_name (str, optional): Module name to append to the app name.
            If None, just the app name is used.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Define log directory - place logs in a 'logs' folder at project root
    base_dir = Path(__file__).resolve().parent.parent.parent
    log_dir = base_dir / "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Get logger name: 'app' or 'app.module_name'
    logger_name = "app"
    if module_name:
        logger_name = f"{logger_name}.{module_name}"

    # Set up log file paths
    log_file = log_dir / f"{logger_name.replace('.', '_')}.log"

    # Get log level from environment variable or default to INFO
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Set up logger with both console (colored) and file output
    logger = setup_logger(
        name=logger_name,
        log_level=log_level,
        log_file=str(log_file),  # Regular text log file
        use_json=False,
        add_console_handler=True,  # Enable console output
        use_colors=True,  # Enable colored output
    )

    return logger

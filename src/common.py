"""
Common functionalities for the codebase.
"""


# Standard Library
from typing import Any, Type
from os import listdir
from pathlib import Path
from inspect import stack
from traceback import format_exception_only, extract_tb
import logging
import json


# == Constants == #
ExceptionType = Type[Exception]


# == Utility Classes == #
class DemoException(Exception):
    """
    Refers to any exception raised by the package developed for the demo.
    """
    pass


# == Internal Functions == #
def _get_stack_summary(e: ExceptionType) -> list[str]:
    """
    Get the stack summary for an exception.

    Parameters
    ----------
    e: ExceptionType
        The exception to be summarized.

    Returns
    -------
    list[str]
        The stack summary.
    """
    # Handle the case where the traceback is None
    if e.__traceback__ is None:
        # Return default empty list
        return []
    # Generate the stack summary
    else:
        # Extract the stack frames
        return [
            # <file> function:lineno
            f"{frame.filename.split('/')[-1]}::{frame.name}:{frame.lineno}"
            for frame in extract_tb(e.__traceback__)
        ]


# == Helper Functions == #
def get_root_path() -> str:
    """
    Get the root path of the project.

    Returns
    -------
    str
        The root path of the project.
    """
    # Set current path
    current_path = Path(__file__).parent
    # Check if the root path is reached
    while "src" not in listdir(current_path):
        # Check if root path is reached
        if current_path == Path("/"):
            # Raise an exception
            raise DemoException(
                "The root path of the project could not be found."
            )
        # Move up one level
        current_path = current_path.parent
    # Return the root path
    return str(current_path.absolute())


# == Core Functions == #
def summarize_exception(e: ExceptionType) -> dict[str, Any]:
    """
    Summarize an exception for logging purposes.

    Parameters
    ----------
    e: ExceptionType
        The exception to be summarized.

    Returns
    -------
    dict[str, Any]
        The summarized exception.
    """
    # Context information
    caller = stack()[1].function
    lineno = stack()[1].lineno
    # Retrieve the exception
    exception_message = format_exception_only(
        type(e),
        e
    )[0].strip()
    # Retrieve the stack trace
    stack_summary = _get_stack_summary(e)
    # Create the summary
    summary = {
        "function_name": caller,
        "lineno": lineno,
        "exception_message": exception_message,
        "traceback": stack_summary
    }
    # Return the summary
    return summary


def log_error(error_msg: str | dict) -> None:
    """
    Log an error message.

    Parameters
    ----------
    error_msg: str | dict
        The error message to be logged.
    """
    # For dictionary error messages, dump them as JSON
    if isinstance(error_msg, dict):
        # Notifiy of error.
        error_json_str = json.dumps(error_msg, indent=4)
        logging.error(
            f"An error ocurred in the codebase:\n{error_json_str}"
        )
    # For string error messages, log them directly
    elif isinstance(error_msg, str):
        logging.error(
            error_msg
        )
    else:
        logging.error(
            "An error occurred in the codebase."
        )
        logging.error(
            "The error message is not a string or a dictionary."
        )
        logging.error(
            "Please check the error message format."
        )
        logging.error(
            "Error message: {error_msg}"
        )
    return None

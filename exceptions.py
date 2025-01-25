from typing import List, Dict, Any
from fastapi import HTTPException


class OutOfRangeException(HTTPException):
    pass


class EmptyCartException(HTTPException):
    pass


def format_validation_error(error: Dict[str, Any]) -> Dict[str, Any]:
    """Formats a single validation error into a more readable format."""
    field_path = ".".join(str(loc) for loc in error.get("loc", []))
    field_name = str(error.get("loc", [""])[-1]) if error.get("loc") else ""

    error_type_messages = {
        "missing": f"{field_name} is required.",
        "literal_error": f"{error.get('input')} is not a valid venue",
    }

    error_type = error.get("type", "")

    custom_msg = error_type_messages.get(
        error_type, error.get("msg", "Unknown error"))

    return {
        "field": field_path,
        "error_type": error_type,
        "message": custom_msg
    }


def format_all_validation_errors(
        errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Formats all validation errors into a more readable format."""
    formatted_errors = [format_validation_error(error) for error in errors]

    return {
        "status": "error",
        "error_count": len(formatted_errors),
        "errors": formatted_errors
    }

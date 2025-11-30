"""Bug Hunt - Bug templates in English."""

from typing import Any

# Bug template translations in English
BUG_TEMPLATES_EN: dict[str, dict[str, Any]] = {
    "bug_001": {
        "title": "Loop Boundary Error",
        "description": "Find the off-by-one error in this list iteration",
        "bugs": [
            {
                "description": "Loop starts at 1 instead of 0, causing IndexError and skipping first item",
                "hint": "Python lists are 0-indexed"
            }
        ]
    },
    "bug_002": {
        "title": "Mutable Default Argument",
        "description": "Classic Python pitfall with mutable defaults",
        "bugs": [
            {
                "description": "Mutable default argument [] is shared across calls",
                "hint": "Default arguments are evaluated once at function definition"
            }
        ]
    },
    "bug_003": {
        "title": "Missing Input Validation",
        "description": "API endpoint without proper validation",
        "bugs": [
            {
                "description": "No validation for username length or age range",
                "hint": "Use Pydantic models with Field() validation"
            },
            {
                "description": "Should return 201 Created, not 200 OK",
                "hint": "POST endpoints that create resources should return 201"
            }
        ]
    },
    "bug_004": {
        "title": "SQL Injection Vulnerability",
        "description": "Security vulnerability in database query",
        "bugs": [
            {
                "description": "String interpolation in SQL query allows SQL injection",
                "hint": "Use parameterized queries with placeholders"
            }
        ]
    },
    "bug_005": {
        "title": "Hardcoded Credentials",
        "description": "Security issue with hardcoded secrets",
        "bugs": [
            {
                "description": "API key hardcoded in source code",
                "hint": "Use environment variables for secrets"
            }
        ]
    },
    "bug_006": {
        "title": "Type Conversion Error",
        "description": "Missing type conversion causes comparison bug",
        "bugs": [
            {
                "description": "Comparing string to int without conversion",
                "hint": "Form inputs are strings, need int() conversion"
            }
        ]
    },
    "bug_007": {
        "title": "Missing Exception Handling",
        "description": "Division without error handling",
        "bugs": [
            {
                "description": "Division by zero when list is empty",
                "hint": "Check if list is empty before dividing"
            }
        ]
    },
    "bug_008": {
        "title": "Variable Shadowing",
        "description": "Loop variable shadows outer scope",
        "bugs": [
            {
                "description": "Loop variable 'total' shadows the accumulator variable",
                "hint": "Use different variable names for loop iterator"
            }
        ]
    },
    "bug_009": {
        "title": "Incorrect Comparison",
        "description": "Assignment instead of comparison",
        "bugs": [
            {
                "description": "Using assignment operator = instead of comparison ==",
                "hint": "This is a syntax error in Python (unlike some languages)"
            }
        ]
    },
    "bug_010": {
        "title": "FastAPI Status Code Error",
        "description": "Incorrect HTTP status code for error response",
        "bugs": [
            {
                "description": "Should return 404 Not Found, not 500 Internal Server Error",
                "hint": "500 is for server errors, 404 is for resource not found"
            }
        ]
    },
}

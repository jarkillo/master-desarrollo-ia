"""Bug Hunt - Educational bug templates for the mini-game."""

from typing import List, Dict, Any
from enum import Enum


class BugType(Enum):
    """Types of bugs in the game."""
    OFF_BY_ONE = "off_by_one"
    MUTABLE_DEFAULT = "mutable_default"
    MISSING_VALIDATION = "missing_validation"
    TYPE_ERROR = "type_error"
    SQL_INJECTION = "sql_injection"
    HARDCODED_SECRET = "hardcoded_secret"
    INCORRECT_STATUS_CODE = "incorrect_status_code"
    MISSING_EXCEPTION_HANDLING = "missing_exception_handling"
    VARIABLE_SHADOWING = "variable_shadowing"
    INCORRECT_COMPARISON = "incorrect_comparison"


class BugTemplate:
    """Template for a code snippet with bugs."""

    def __init__(
        self,
        id: str,
        title: str,
        difficulty: str,  # "easy", "medium", "hard"
        code: str,
        bugs: List[Dict[str, Any]],
        description: str,
        xp_reward: int
    ):
        self.id = id
        self.title = title
        self.difficulty = difficulty
        self.code = code
        self.bugs = bugs  # List of {line: int, type: BugType, description: str}
        self.description = description
        self.xp_reward = xp_reward


# Bug Templates Database
BUG_TEMPLATES = [
    BugTemplate(
        id="bug_001",
        title="Loop Boundary Error",
        difficulty="easy",
        description="Find the off-by-one error in this list iteration",
        xp_reward=50,
        code="""def get_first_n_items(items, n):
    \"\"\"Return first n items from a list.\"\"\"
    result = []
    for i in range(1, n + 1):
        result.append(items[i])
    return result

# Example usage
numbers = [10, 20, 30, 40, 50]
print(get_first_n_items(numbers, 3))""",
        bugs=[
            {
                "line": 4,
                "type": BugType.OFF_BY_ONE.value,
                "description": "Loop starts at 1 instead of 0, causing IndexError and skipping first item",
                "hint": "Python lists are 0-indexed"
            }
        ]
    ),

    BugTemplate(
        id="bug_002",
        title="Mutable Default Argument",
        difficulty="medium",
        description="Classic Python pitfall with mutable defaults",
        xp_reward=75,
        code="""def add_item_to_cart(item, cart=[]):
    \"\"\"Add an item to the shopping cart.\"\"\"
    cart.append(item)
    return cart

# Usage
cart1 = add_item_to_cart("Apple")
cart2 = add_item_to_cart("Banana")
print(f"Cart 1: {cart1}")
print(f"Cart 2: {cart2}")""",
        bugs=[
            {
                "line": 1,
                "type": BugType.MUTABLE_DEFAULT.value,
                "description": "Mutable default argument [] is shared across calls",
                "hint": "Default arguments are evaluated once at function definition"
            }
        ]
    ),

    BugTemplate(
        id="bug_003",
        title="Missing Input Validation",
        difficulty="easy",
        description="API endpoint without proper validation",
        xp_reward=60,
        code="""from fastapi import FastAPI

app = FastAPI()

@app.post("/users")
async def create_user(username: str, age: int):
    return {"username": username, "age": age}""",
        bugs=[
            {
                "line": 5,
                "type": BugType.MISSING_VALIDATION.value,
                "description": "No validation for username length or age range",
                "hint": "Use Pydantic models with Field() validation"
            },
            {
                "line": 5,
                "type": BugType.INCORRECT_STATUS_CODE.value,
                "description": "Should return 201 Created, not 200 OK",
                "hint": "POST endpoints that create resources should return 201"
            }
        ]
    ),

    BugTemplate(
        id="bug_004",
        title="SQL Injection Vulnerability",
        difficulty="hard",
        description="Security vulnerability in database query",
        xp_reward=100,
        code="""def get_user_by_username(username: str):
    \"\"\"Fetch user from database by username.\"\"\"
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# Usage
user = get_user_by_username(request.form['username'])""",
        bugs=[
            {
                "line": 3,
                "type": BugType.SQL_INJECTION.value,
                "description": "String interpolation in SQL query allows SQL injection",
                "hint": "Use parameterized queries with placeholders"
            }
        ]
    ),

    BugTemplate(
        id="bug_005",
        title="Hardcoded Credentials",
        difficulty="easy",
        description="Security issue with hardcoded secrets",
        xp_reward=50,
        code="""import requests

def call_external_api():
    api_key = "sk_live_1234567890abcdef"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.example.com/data", headers=headers)
    return response.json()""",
        bugs=[
            {
                "line": 4,
                "type": BugType.HARDCODED_SECRET.value,
                "description": "API key hardcoded in source code",
                "hint": "Use environment variables for secrets"
            }
        ]
    ),

    BugTemplate(
        id="bug_006",
        title="Type Conversion Error",
        difficulty="medium",
        description="Missing type conversion causes comparison bug",
        xp_reward=70,
        code="""def process_age(age_input):
    \"\"\"Process user age from form input.\"\"\"
    if age_input >= 18:
        return "Adult"
    else:
        return "Minor"

# Usage (age_input comes from HTML form as string)
result = process_age(request.form.get('age'))""",
        bugs=[
            {
                "line": 3,
                "type": BugType.TYPE_ERROR.value,
                "description": "Comparing string to int without conversion",
                "hint": "Form inputs are strings, need int() conversion"
            }
        ]
    ),

    BugTemplate(
        id="bug_007",
        title="Missing Exception Handling",
        difficulty="medium",
        description="Division without error handling",
        xp_reward=65,
        code="""def calculate_average(numbers):
    \"\"\"Calculate average of a list of numbers.\"\"\"
    total = sum(numbers)
    count = len(numbers)
    return total / count

# Usage
scores = []
avg = calculate_average(scores)
print(f"Average: {avg}\")""",
        bugs=[
            {
                "line": 5,
                "type": BugType.MISSING_EXCEPTION_HANDLING.value,
                "description": "Division by zero when list is empty",
                "hint": "Check if list is empty before dividing"
            }
        ]
    ),

    BugTemplate(
        id="bug_008",
        title="Variable Shadowing",
        difficulty="hard",
        description="Loop variable shadows outer scope",
        xp_reward=90,
        code="""def process_items(items):
    \"\"\"Process items and return summary.\"\"\"
    total = 0
    for total in items:
        print(f"Processing: {total}")

    return f"Processed {total} items"

# Usage
result = process_items([1, 2, 3, 4, 5])
print(result)""",
        bugs=[
            {
                "line": 4,
                "type": BugType.VARIABLE_SHADOWING.value,
                "description": "Loop variable 'total' shadows the accumulator variable",
                "hint": "Use different variable names for loop iterator"
            }
        ]
    ),

    BugTemplate(
        id="bug_009",
        title="Incorrect Comparison",
        difficulty="easy",
        description="Assignment instead of comparison",
        xp_reward=50,
        code="""def check_admin(user_role):
    \"\"\"Check if user is admin.\"\"\"
    if user_role = "admin":
        return True
    return False

# Usage
is_admin = check_admin("user")""",
        bugs=[
            {
                "line": 3,
                "type": BugType.INCORRECT_COMPARISON.value,
                "description": "Using assignment operator = instead of comparison ==",
                "hint": "This is a syntax error in Python (unlike some languages)"
            }
        ]
    ),

    BugTemplate(
        id="bug_010",
        title="FastAPI Status Code Error",
        difficulty="medium",
        description="Incorrect HTTP status code for error response",
        xp_reward=75,
        code="""from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=500, detail="User not found")
    return user""",
        bugs=[
            {
                "line": 9,
                "type": BugType.INCORRECT_STATUS_CODE.value,
                "description": "Should return 404 Not Found, not 500 Internal Server Error",
                "hint": "500 is for server errors, 404 is for resource not found"
            }
        ]
    ),
]


def get_random_template(difficulty: str = None) -> BugTemplate:
    """Get a random bug template, optionally filtered by difficulty."""
    import random

    if difficulty:
        filtered = [t for t in BUG_TEMPLATES if t.difficulty == difficulty]
        if not filtered:
            raise ValueError(f"No templates found for difficulty: {difficulty}")
        return random.choice(filtered)

    return random.choice(BUG_TEMPLATES)


def get_template_by_id(template_id: str) -> BugTemplate:
    """Get a specific bug template by ID."""
    for template in BUG_TEMPLATES:
        if template.id == template_id:
            return template
    raise ValueError(f"Template not found: {template_id}")


def get_all_templates() -> List[BugTemplate]:
    """Get all available bug templates."""
    return BUG_TEMPLATES

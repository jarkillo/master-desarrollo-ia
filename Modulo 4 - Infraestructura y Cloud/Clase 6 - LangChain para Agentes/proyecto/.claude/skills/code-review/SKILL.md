---
name: Code Review Assistant
description: Perform comprehensive code reviews following SOLID principles and best practices
version: 1.0.0
---

# Code Review Skill

## When to Use This Skill

Use this skill when reviewing:
- ✅ Pull requests before merge
- ✅ Refactoring proposals
- ✅ Security-sensitive code changes
- ✅ Performance-critical implementations

**DO NOT use for**:
- ❌ Simple typo fixes (use direct editing)
- ❌ Documentation-only changes (unless checking technical accuracy)
- ❌ Generated code without logic (e.g., auto-generated migrations)

## Review Checklist

### 1. Architecture & Design

**Principle: SOLID**

- [ ] **Single Responsibility**: Each class/function does ONE thing well
  - Example violation: `UserManager` that handles auth + emails + logging
  - Fix: Split into `AuthService`, `EmailService`, `Logger`

- [ ] **Dependency Inversion**: Depends on abstractions, not concretions
  - Example violation: `class OrderService` depends on `PostgreSQLRepository`
  - Fix: Depend on `RepositorioBase` (Protocol/Interface)

- [ ] **Open/Closed**: Open for extension, closed for modification
  - Example: Use strategy pattern instead of if/elif chains

### 2. Code Quality

- [ ] **Naming**: Variables/functions have clear, descriptive names
  - ❌ `def calc(x, y)`
  - ✅ `def calculate_total_price(items: list[Item], tax_rate: float)`

- [ ] **Complexity**: Cyclomatic complexity < 10 per function
  - Use: `radon cc file.py` to measure
  - If > 10: Extract helper functions

- [ ] **DRY (Don't Repeat Yourself)**: No code duplication (3+ lines repeated)
  - Tool: `pylint --disable=all --enable=duplicate-code`

### 3. Testing

- [ ] **Coverage**: Critical paths have tests (>80% coverage)
  - Run: `pytest --cov=api --cov-report=term-missing --cov-fail-under=80`

- [ ] **Test Quality**: Tests are isolated, deterministic, fast
  - Isolated: No shared state between tests
  - Deterministic: Same input → same output (no random, no time.sleep())
  - Fast: Unit tests < 100ms, integration < 1s

- [ ] **Edge Cases**: Error conditions tested
  - Empty inputs, null values, boundary conditions
  - Network failures, database errors, invalid data

### 4. Security

- [ ] **Input Validation**: All user inputs validated with Pydantic
  ```python
  # ✅ Good
  class TaskCreate(BaseModel):
      title: str = Field(min_length=1, max_length=200)
      priority: int = Field(ge=1, le=5)
  ```

- [ ] **SQL Injection**: Parameterized queries used
  - ❌ `db.execute(f"SELECT * FROM users WHERE id = {user_id}")`
  - ✅ `db.execute("SELECT * FROM users WHERE id = ?", (user_id,))`

- [ ] **Secrets**: No hardcoded credentials
  - Use environment variables: `os.getenv("API_KEY")`
  - Never commit `.env` files

### 5. Performance

- [ ] **N+1 Queries**: No database query loops
  ```python
  # ❌ N+1 query
  for user_id in user_ids:
      user = db.query(User).get(user_id)  # N queries!

  # ✅ Single query with eager loading
  users = db.query(User).filter(User.id.in_(user_ids)).all()
  ```

- [ ] **Caching**: Expensive operations cached
  - Use `@lru_cache` for pure functions
  - Use Redis for distributed caching

- [ ] **Async I/O**: Blocking operations are async
  - HTTP calls: `async with httpx.AsyncClient()`
  - DB queries: `await session.execute()`

## Severity Levels

**🔴 CRITICAL**: Must fix before merge
- Security vulnerabilities (SQL injection, XSS, etc.)
- Data loss risks (missing transactions, unsafe deletes)
- Breaking changes without migration path

**🟡 MAJOR**: Should fix before merge
- Performance issues (N+1 queries, memory leaks)
- Maintainability problems (high complexity, violation of SOLID)
- Missing critical tests (core business logic untested)

**🟢 MINOR**: Nice to have
- Style inconsistencies (use `ruff` to autofix)
- Missing docstrings (non-public methods)
- Suggestions for readability

## Review Output Format

For each issue found, provide:

```
[SEVERITY] [CATEGORY]: Brief description

**Issue**: Detailed explanation of the problem
**Location**: file.py:line_number
**Impact**: What could go wrong / why it matters

**Fix**:
```python
# Code showing the correction
```

**Reference**: Link to relevant documentation or `checklist.md` section
```

## Example Review

**Code being reviewed**:

```python
# api/tasks.py
def get_user_tasks(user_id: str) -> list[dict]:
    user = db.query(User).get(user_id)
    tasks = []
    for task_id in user.task_ids:
        task = db.query(Task).get(task_id)  # ⚠️ N+1 query!
        tasks.append({
            "id": task.id,
            "title": task.title,
            "status": task.status
        })
    return tasks
```

**Review output**:

```
🟡 MAJOR: N+1 Query Detected

**Issue**: Line 5 executes a database query inside a loop, causing N+1 queries.

**Location**: api/tasks.py:5

**Impact**:
- Performance degrades linearly with number of tasks
- 100 tasks = 101 database queries (1 for user + 100 for tasks)
- Database connection pool exhaustion under load

**Fix**:
```python
def get_user_tasks(user_id: str) -> list[dict]:
    user = db.query(User).get(user_id)

    # Single query with eager loading
    tasks = db.query(Task).filter(
        Task.id.in_(user.task_ids)
    ).all()

    return [
        {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
        for task in tasks
    ]
```

**Reference**: See `performance_patterns.md` section 3.2 - "Avoiding N+1 Queries"

---

🟢 MINOR: Missing Type Hints for Return

**Issue**: Return type annotation missing

**Location**: api/tasks.py:1

**Fix**:
```python
from typing import TypedDict

class TaskDict(TypedDict):
    id: int
    title: str
    status: str

def get_user_tasks(user_id: str) -> list[TaskDict]:
    ...
```

**Reference**: PEP 484 - Type Hints
```

## Tools Integration

This skill can be invoked from LangChain agents:

```python
def code_review_with_skill(code: str, file_path: str) -> str:
    """
    Invoke Agent Skill for code review.

    This loads:
    - .claude/skills/code-review/SKILL.md
    - .claude/skills/code-review/checklist.md

    Returns structured review output.
    """
    # Agent with skills executes review
    return claude_with_skills.review(code, file_path)
```

## Continuous Improvement

Track review quality:

```python
# metrics.json
{
  "reviews_performed": 42,
  "critical_issues_found": 3,
  "major_issues_found": 15,
  "minor_issues_found": 28,
  "avg_time_per_review": "2.5 minutes"
}
```

Update checklist based on:
- Frequent issues found → add to checklist
- False positives → refine criteria
- Team feedback → adjust severity levels

## Related Skills

- `performance-optimizer` - For deep performance analysis
- `security-hardening` - For comprehensive security audit
- `test-coverage-strategist` - For testing guidance

## Version History

- **1.0.0** (2025-10-30): Initial version
  - Complete SOLID checklist
  - Security & Performance sections
  - Example reviews with fixes

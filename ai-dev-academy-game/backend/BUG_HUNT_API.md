# Bug Hunt Mini-Game API Documentation

## Overview

Bug Hunt is an educational mini-game where players identify bugs in code snippets. Players earn XP based on accuracy and speed.

## Base URL

```
http://localhost:8000/api/minigames
```

## Authentication

Currently no authentication required. Player ID is passed in requests.

---

## Endpoints

### 1. Start Bug Hunt Game

**POST** `/bug-hunt/start`

Start a new Bug Hunt session. Returns a code snippet with bugs to identify.

#### Request Body

```json
{
  "player_id": 1,
  "difficulty": "easy"  // Optional: "easy", "medium", "hard"
}
```

#### Response (200 OK)

```json
{
  "session_id": 42,
  "template_id": "bug_001",
  "title": "Loop Boundary Error",
  "description": "Find the off-by-one error in this list iteration",
  "difficulty": "easy",
  "code": "def get_first_n_items(items, n):\n    ...",
  "bugs_count": 1,
  "max_xp": 50,
  "started_at": "2025-10-25T12:00:00Z"
}
```

#### Error Responses

- **404 Not Found**: Player not found
- **400 Bad Request**: Invalid difficulty level

---

### 2. Submit Bug Hunt Answers

**POST** `/bug-hunt/submit`

Submit identified bug lines and receive score/XP.

#### Request Body

```json
{
  "session_id": 42,
  "player_id": 1,
  "found_bug_lines": [4, 7],  // Line numbers identified as bugs
  "time_seconds": 45.5
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "score": 1150,
  "xp_earned": 125,
  "bugs_found": 2,
  "bugs_total": 2,
  "bugs_missed": 0,
  "false_positives": 0,
  "accuracy": 100.0,
  "time_seconds": 45.5,
  "is_perfect": true,
  "results": [
    {
      "line": 4,
      "found": true,
      "is_correct": true,
      "bug_type": "off_by_one",
      "description": "Loop starts at 1 instead of 0..."
    }
  ],
  "performance_bonus": 75,
  "achievements_unlocked": ["bug_hunter"]
}
```

#### Error Responses

- **404 Not Found**: Game session not found
- **403 Forbidden**: Session belongs to another player

---

### 3. Get Leaderboard

**GET** `/bug-hunt/leaderboard?difficulty=easy&limit=10`

Get top scores globally or filtered by difficulty.

#### Query Parameters

- `difficulty` (optional): Filter by "easy", "medium", or "hard"
- `limit` (optional): Number of entries (1-100, default: 10)

#### Response (200 OK)

```json
{
  "total_entries": 42,
  "entries": [
    {
      "rank": 1,
      "player_id": 5,
      "username": "code_ninja",
      "score": 1200,
      "bugs_found": 2,
      "bugs_total": 2,
      "time_seconds": 30.0,
      "accuracy": 100.0,
      "difficulty": "easy",
      "completed_at": "2025-10-25T12:05:00Z"
    }
  ],
  "difficulty_filter": "easy"
}
```

---

### 4. Get Player Stats

**GET** `/bug-hunt/stats/{player_id}`

Get aggregated Bug Hunt statistics for a player.

#### Path Parameters

- `player_id`: Player ID

#### Response (200 OK)

```json
{
  "total_games_played": 15,
  "total_bugs_found": 28,
  "total_perfect_games": 5,
  "best_score": 1200,
  "average_score": 875.5,
  "average_accuracy": 85.3,
  "favorite_difficulty": "medium",
  "total_xp_earned": 1850
}
```

#### Error Responses

- **404 Not Found**: Player not found

---

## Bug Types

The game includes these educational bug types:

| Type                        | Description                          | Difficulty |
|-----------------------------|--------------------------------------|------------|
| `off_by_one`                | Loop boundary errors                 | Easy       |
| `mutable_default`           | Mutable default arguments in Python  | Medium     |
| `missing_validation`        | API endpoints without validation     | Easy       |
| `sql_injection`             | SQL injection vulnerabilities        | Hard       |
| `hardcoded_secret`          | Hardcoded API keys/secrets           | Easy       |
| `type_error`                | Missing type conversions             | Medium     |
| `missing_exception_handling`| Missing try/except blocks            | Medium     |
| `variable_shadowing`        | Loop variables shadowing outer scope | Hard       |
| `incorrect_comparison`      | Using = instead of ==                | Easy       |
| `incorrect_status_code`     | Wrong HTTP status codes              | Medium     |

---

## Scoring System

### Base Score Calculation

```
base_score = (bugs_found / bugs_total) * 1000
base_score -= false_positives * 100  // Penalty for incorrect identifications
```

### Time Bonus

Faster completion = higher bonus (max 200 points)

**Time thresholds:**
- Easy: 60 seconds
- Medium: 120 seconds
- Hard: 180 seconds

```
time_bonus = max(0, 200 * (1 - min(time_seconds / threshold, 1)))
```

### Final Score

```
score = max(0, base_score + time_bonus)
```

---

## XP Rewards

### Base XP

- Easy: 50 XP
- Medium: 75 XP
- Hard: 100 XP

### Bonuses

- **Perfect game** (all bugs found, no false positives): +50 XP
- **Speed bonus**: Up to +25 XP for fast completion

### Total XP Formula

```
xp_earned = base_xp + perfect_bonus + speed_bonus
```

---

## Game Flow Example

### 1. Start Game

```bash
curl -X POST http://localhost:8000/api/minigames/bug-hunt/start \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "difficulty": "easy"}'
```

### 2. Player Identifies Bugs

Player reviews code and identifies lines: 4, 7

### 3. Submit Answers

```bash
curl -X POST http://localhost:8000/api/minigames/bug-hunt/submit \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 42,
    "player_id": 1,
    "found_bug_lines": [4, 7],
    "time_seconds": 45.5
  }'
```

### 4. Receive Results

API returns score, XP, and detailed feedback on each bug.

---

## Testing

Run the test suite:

```bash
cd ai-dev-academy-game/backend
pytest tests/test_bug_hunt.py -v
```

All 12 tests should pass:

- Health check
- Start game (with/without difficulty)
- Invalid player/difficulty
- Perfect score submission
- Partial score submission
- False positives handling
- Leaderboard (empty/with games)
- Player stats (no games/with games)

---

## Database Schema

### `bug_hunt_games` Table

| Column           | Type      | Description                          |
|------------------|-----------|--------------------------------------|
| id               | INTEGER   | Primary key                          |
| player_id        | INTEGER   | Foreign key to players table         |
| template_id      | TEXT      | Bug template ID (e.g., "bug_001")    |
| difficulty       | TEXT      | "easy", "medium", or "hard"          |
| bugs_found       | INTEGER   | Number of bugs correctly identified  |
| bugs_total       | INTEGER   | Total bugs in template               |
| time_seconds     | FLOAT     | Time taken to complete               |
| score            | INTEGER   | Calculated score                     |
| xp_earned        | INTEGER   | XP awarded                           |
| found_bugs       | JSON      | List of correctly identified lines   |
| missed_bugs      | JSON      | List of missed bug lines             |
| false_positives  | JSON      | List of incorrectly identified lines |
| started_at       | TIMESTAMP | Game start time                      |
| completed_at     | TIMESTAMP | Game completion time                 |

---

## Future Enhancements

### Planned Features

1. **More Bug Templates**: Expand to 50+ templates covering:
   - React/TypeScript bugs
   - Async/await issues
   - Database query optimization
   - Docker/deployment mistakes

2. **Difficulty Progression**: Unlock harder templates based on player level

3. **Multiplayer Mode**: Real-time bug hunting competitions

4. **Custom Templates**: Let players create and share templates

5. **Hint System**: Progressive hints that reduce XP rewards

6. **Bug Categories**: Filter by bug type (security, performance, logic)

7. **Time Attack Mode**: Find as many bugs as possible in 5 minutes

8. **Achievements**:
   - "Bug Exterminator": Find 100 bugs
   - "Speed Demon": Complete 10 games in under 30 seconds
   - "Perfectionist": 20 perfect games
   - "Security Sentinel": Find 50 security bugs

---

## Contributing

To add new bug templates:

1. Edit `app/content/bug_templates.py`
2. Add a new `BugTemplate` with:
   - Unique ID
   - Educational code snippet
   - Bug locations and types
   - Hints
3. Run tests to validate

Example:

```python
BugTemplate(
    id="bug_011",
    title="Your Bug Title",
    difficulty="medium",
    description="Brief description",
    xp_reward=75,
    code="""your code here""",
    bugs=[
        {
            "line": 5,
            "type": BugType.YOUR_TYPE.value,
            "description": "What's wrong",
            "hint": "How to fix it"
        }
    ]
)
```

---

## API Versioning

Current version: **v1.0.0**

Breaking changes will be announced with version bumps.

---

## Support

For issues or questions:
- GitHub Issues: [github.com/jarkillo/master-ia-manu](https://github.com/jarkillo/master-ia-manu)
- Linear: [JAR-238](https://linear.app/jarko/issue/JAR-238)

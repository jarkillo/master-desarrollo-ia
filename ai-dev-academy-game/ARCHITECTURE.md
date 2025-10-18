# AI Dev Academy - Game Architecture

## Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: TailwindCSS
- **Animations**: Framer Motion
- **State Management**: Zustand (simple, performant)
- **Icons**: Lucide React
- **Build**: Vite

### Backend
- **Framework**: FastAPI 0.118
- **Database**: SQLite (simple, portable)
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT (optional for multi-user)
- **CORS**: Enabled for local dev

### Deployment
- **Frontend**: Vercel / Netlify (static)
- **Backend**: Railway / Render (free tier)
- **Database**: SQLite file (can upgrade to PostgreSQL later)

---

## Architecture Diagram

```mermaid
graph TD
    A[Browser - React App] -->|HTTP/JSON| B[FastAPI Backend]
    B -->|SQLAlchemy ORM| C[SQLite Database]

    A --> A1[Components]
    A --> A2[Pages]
    A --> A3[State Management]

    A1 --> A1a[Dashboard]
    A1 --> A1b[Workspace]
    A1 --> A1c[ModuleCard]
    A1 --> A1d[MiniGames]

    B --> B1[Routes]
    B --> B2[Services]
    B --> B3[Models]

    B1 --> B1a[/player]
    B1 --> B1b[/progress]
    B1 --> B1c[/achievements]
    B1 --> B1d[/minigames]

    C --> C1[Tables]
    C1 --> C1a[players]
    C1 --> C1b[progress]
    C1 --> C1c[achievements]
    C1 --> C1d[stats]
```

---

## Directory Structure

```
ai-dev-academy-game/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── database.py             # DB connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── player.py           # Player model
│   │   │   ├── progress.py         # Progress tracking
│   │   │   └── achievement.py      # Achievements
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── player.py           # Pydantic schemas
│   │   │   ├── progress.py
│   │   │   └── achievement.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── player_service.py   # Business logic
│   │   │   ├── progress_service.py
│   │   │   └── xp_service.py       # XP calculation
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── player.py           # Player endpoints
│   │   │   ├── progress.py         # Progress endpoints
│   │   │   └── minigames.py        # Mini-games endpoints
│   │   └── content/
│   │       ├── __init__.py
│   │       ├── modules.py          # Module definitions
│   │       ├── achievements.py     # Achievement definitions
│   │       └── minigames.py        # Mini-game logic
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   │   └── assets/
│   │       ├── workspace/          # Workspace images
│   │       └── avatars/            # Character avatars
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Dashboard.tsx       # Main dashboard
│   │   │   ├── Workspace.tsx       # Animated workspace
│   │   │   ├── ModuleCard.tsx      # Module selector
│   │   │   ├── ClassCard.tsx       # Class within module
│   │   │   ├── ProgressBar.tsx     # XP/Level bar
│   │   │   ├── AchievementModal.tsx
│   │   │   └── minigames/
│   │   │       ├── BugHunt.tsx
│   │   │       ├── PromptDuel.tsx
│   │   │       └── ArchitectureBuilder.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── CreateCharacter.tsx
│   │   │   ├── ModuleView.tsx
│   │   │   ├── ClassView.tsx
│   │   │   └── Stats.tsx
│   │   ├── store/
│   │   │   ├── playerStore.ts      # Zustand store
│   │   │   └── gameStore.ts
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── game.ts             # TypeScript types
│   │   └── utils/
│   │       ├── xp.ts               # XP calculations
│   │       └── achievements.ts     # Achievement checks
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docker-compose.yml              # Full stack local dev
├── README.md
└── ARCHITECTURE.md                 # This file
```

---

## Database Schema

```sql
-- Players
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    avatar TEXT DEFAULT 'default.png',
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progress (tracks module/class completion)
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    module_number INTEGER NOT NULL,
    class_number INTEGER NOT NULL,
    status TEXT DEFAULT 'locked',  -- locked, unlocked, in_progress, completed
    exercises_completed INTEGER DEFAULT 0,
    exercises_total INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, module_number, class_number)
);

-- Achievements
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    achievement_key TEXT NOT NULL,  -- 'first_commit', 'bug_hunter', etc.
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, achievement_key)
);

-- Player Stats
CREATE TABLE player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    total_classes_completed INTEGER DEFAULT 0,
    total_exercises_done INTEGER DEFAULT 0,
    total_minigames_played INTEGER DEFAULT 0,
    total_code_lines INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_activity_date DATE,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id)
);

-- Unlocked Tools (Agent, IDE, etc.)
CREATE TABLE unlocked_tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    tool_key TEXT NOT NULL,  -- 'claude_code', 'cursor', 'git', 'test_strategist'
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, tool_key)
);
```

---

## API Endpoints

### Player Management
```
POST   /api/player/create          # Create new player
GET    /api/player/{id}             # Get player info
PUT    /api/player/{id}             # Update player (avatar, etc.)
GET    /api/player/{id}/stats       # Get player stats
```

### Progress Tracking
```
GET    /api/progress/{player_id}                    # Get all progress
POST   /api/progress/{player_id}/start-class       # Start a class
POST   /api/progress/{player_id}/complete-class    # Complete a class
POST   /api/progress/{player_id}/complete-exercise # Complete exercise
```

### Achievements
```
GET    /api/achievements/{player_id}               # Get unlocked achievements
POST   /api/achievements/{player_id}/check         # Check for new achievements
```

### Content
```
GET    /api/modules                                # Get all modules (with locked status)
GET    /api/modules/{module_number}                # Get specific module with classes
GET    /api/modules/{module_number}/class/{class_number}  # Get class content
```

### Mini-Games
```
POST   /api/minigames/bug-hunt/start               # Start Bug Hunt game
POST   /api/minigames/bug-hunt/submit              # Submit Bug Hunt answers
GET    /api/minigames/leaderboard                  # Global leaderboard
```

---

## XP & Leveling System

### XP Rewards
```typescript
const XP_REWARDS = {
  COMPLETE_CLASS: 100,
  COMPLETE_EXERCISE: 50,
  COMPLETE_MODULE_PROJECT: 500,
  WIN_MINIGAME: 100,
  DAILY_STREAK_BONUS: 0.10,  // 10% bonus per day
  FIRST_TRY_BONUS: 25,
  PERFECT_SCORE_BONUS: 50
};
```

### Level Progression
```typescript
// Level = floor(sqrt(XP / 100))
// Example:
// Level 1: 0-99 XP
// Level 2: 100-399 XP
// Level 3: 400-899 XP
// Level 4: 900-1599 XP
// Level 5: 1600-2499 XP
// ...
// Level 30: 90000+ XP

function calculateLevel(xp: number): number {
  return Math.floor(Math.sqrt(xp / 100)) + 1;
}

function xpForNextLevel(currentLevel: number): number {
  return (currentLevel * currentLevel) * 100;
}
```

### Unlock System
```typescript
const UNLOCKS = {
  // Tools
  CLAUDE_CODE: { level: 1, xp: 0 },      // Default
  GIT: { level: 1, xp: 0 },              // Default
  CURSOR: { level: 3, xp: 400 },
  GITHUB_COPILOT: { level: 5, xp: 1600 },

  // Agents
  GIT_COMMIT_HELPER: { level: 2, xp: 100 },
  TEST_STRATEGIST: { level: 6, xp: 2500 },
  CLEAN_ARCH_ENFORCER: { level: 8, xp: 4900 },
  SECURITY_MENTOR: { level: 10, xp: 9000 },

  // Workspace Upgrades
  DUAL_MONITORS: { level: 4, xp: 900 },
  STANDING_DESK: { level: 7, xp: 3600 },
  HOME_OFFICE: { level: 12, xp: 14400 },
  STARTUP_OFFICE: { level: 20, xp: 40000 }
};
```

---

## Achievement Definitions

```typescript
const ACHIEVEMENTS = {
  // Module 0
  FIRST_STEPS: {
    key: 'first_steps',
    name: 'First Steps',
    description: 'Complete Module 0',
    icon: '🎓',
    xp_bonus: 100,
    condition: (player) => player.modules_completed >= 1
  },

  PROMPT_ENGINEER: {
    key: 'prompt_engineer',
    name: 'Prompt Engineer',
    description: 'Create 5 effective prompts',
    icon: '✍️',
    xp_bonus: 50
  },

  // Testing
  TEST_MASTER: {
    key: 'test_master',
    name: 'Test Master',
    description: 'Achieve 80%+ coverage in 5 projects',
    icon: '🧪',
    xp_bonus: 200
  },

  // Architecture
  ARCHITECTURE_GURU: {
    key: 'architecture_guru',
    name: 'Architecture Guru',
    description: 'Implement Clean Architecture without errors',
    icon: '🏛️',
    xp_bonus: 150
  },

  // Security
  SECURITY_EXPERT: {
    key: 'security_expert',
    name: 'Security Expert',
    description: 'Detect 10 vulnerabilities with Security Mentor',
    icon: '🔒',
    xp_bonus: 200
  },

  // Agents
  ARMY_OF_AGENTS: {
    key: 'army_of_agents',
    name: 'Army of Agents',
    description: 'Create 10 custom agents',
    icon: '🤖',
    xp_bonus: 300
  },

  // Streak
  DEDICATED_LEARNER: {
    key: 'dedicated_learner',
    name: 'Dedicated Learner',
    description: '7-day learning streak',
    icon: '🔥',
    xp_bonus: 100
  },

  // Mini-games
  BUG_HUNTER: {
    key: 'bug_hunter',
    name: 'Bug Hunter',
    description: 'Win Bug Hunt mini-game 10 times',
    icon: '🐛',
    xp_bonus: 150
  }
};
```

---

## Module Content Structure

```typescript
interface Module {
  number: number;
  name: string;
  description: string;
  classes: Class[];
  finalProject: Project;
  unlockLevel: number;
}

interface Class {
  number: number;
  name: string;
  description: string;
  duration: string;  // "6 hours"
  exercises: Exercise[];
  xpReward: number;
  unlockRequirement: {
    previousClass?: number;
    level?: number;
  };
}

interface Exercise {
  id: string;
  title: string;
  description: string;
  type: 'quiz' | 'code' | 'project' | 'reading';
  xpReward: number;
}

// Example:
const MODULE_0: Module = {
  number: 0,
  name: "IA Development Foundations",
  description: "Master AI tools and fundamentals",
  unlockLevel: 1,  // Available from start
  classes: [
    {
      number: 1,
      name: "Fundamentos de IA en Desarrollo",
      description: "First contact with AI dev tools",
      duration: "6 hours",
      xpReward: 100,
      exercises: [
        { id: 'ex_0_1_1', title: 'Install Python', type: 'reading', xpReward: 10 },
        { id: 'ex_0_1_2', title: 'Setup Claude Code', type: 'code', xpReward: 25 },
        // ...
      ]
    },
    // Classes 2-6...
  ],
  finalProject: {
    name: "AI Development Toolkit",
    xpReward: 500
  }
};
```

---

## UI/UX Design

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────────┐
│  AI Dev Academy                    [🔔]  [⚙️]  [Avatar] ▼   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────┐  ┌────────────────────────────┐    │
│  │   Your Profile     │  │   Current Progress         │    │
│  │                    │  │   ████████████░░░░░ 75%    │    │
│  │   Level 12 ⭐      │  │   Module 2: FastAPI        │    │
│  │   Senior Dev       │  │   Class 4/6 completed      │    │
│  │                    │  │                            │    │
│  │   XP: 14,250/16,900│  │   Next Unlock:             │    │
│  │   ████████████░░   │  │   🤖 Clean Arch Enforcer   │    │
│  └────────────────────┘  │   (250 XP needed)          │    │
│                          └────────────────────────────┘    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   Your Workspace                                      │  │
│  │                                                       │  │
│  │   ┌─────────────────────────────────┐                │  │
│  │   │   🖥️  📚  ☕  🪴                │ Upgraded!      │  │
│  │   │                                 │                │  │
│  │   │   Standing Desk + Dual Monitors│                │  │
│  │   │                                 │                │  │
│  │   │        🧑‍💻 You                 │                │  │
│  │   └─────────────────────────────────┘                │  │
│  │                                                       │  │
│  │   Active Tools:                                      │  │
│  │   ✅ Claude Code  ✅ Git  ✅ Cursor  🔒 Copilot     │  │
│  │                                                       │  │
│  │   Active Agents:                                     │  │
│  │   🤖 Git Commit Helper  🤖 Test Strategist          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Modules                                                    │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │  M0  │ │  M1  │ │  M2  │ │  M3  │ │  M4  │ │  M5  │  │
│  │  ✅  │ │  ✅  │ │  🔓  │ │  🔒  │ │  🔒  │ │  🔒  │  │
│  │ 100% │ │ 100% │ │  75% │ │ Lvl  │ │ Lvl  │ │ Lvl  │  │
│  │      │ │      │ │      │ │  16  │ │  21  │ │  26  │  │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
│                                                             │
│  Mini-Games  🎮                                            │
│  [🐛 Bug Hunt]  [✍️ Prompt Duel]  [🏛️ Architect Builder]  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Strategy

### Phase 1: Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Phase 2: Production
```bash
# Build frontend
cd frontend
npm run build

# Deploy frontend to Vercel
vercel --prod

# Deploy backend to Railway
# railway.json config
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

## Extensibility Design

### Adding New Modules
```typescript
// 1. Add module definition in backend/app/content/modules.py
const MODULE_6 = {
  number: 6,
  name: "Advanced AI Patterns",
  description: "Master advanced AI integration",
  unlockLevel: 31,
  classes: [/* ... */]
};

// 2. Frontend automatically fetches and renders
// 3. No code changes needed in UI components
```

### Adding New Mini-Games
```typescript
// 1. Create component in frontend/src/components/minigames/
// 2. Add endpoint in backend/app/routes/minigames.py
// 3. Register in MiniGameRegistry
// 4. Game appears automatically in UI
```

### Adding New Achievements
```typescript
// 1. Add to ACHIEVEMENTS in backend/app/content/achievements.py
// 2. Frontend polls /api/achievements/check periodically
// 3. Shows popup when new achievement unlocked
```

---

## Next Steps

1. ✅ Architecture designed
2. ⏳ Implement backend (FastAPI + SQLite)
3. ⏳ Implement frontend (React + Tailwind)
4. ⏳ Integrate Module 0-3 content
5. ⏳ Create Bug Hunt mini-game
6. ⏳ Deploy to production

---

**Design Philosophy**:
- **Expandable**: Easy to add modules, classes, mini-games
- **Engaging**: Visual progress, achievements, unlocks
- **Educational**: Reinforces learning through gameplay
- **Portable**: SQLite for easy setup, can upgrade later

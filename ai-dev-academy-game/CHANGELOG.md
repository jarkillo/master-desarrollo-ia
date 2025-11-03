# Changelog

All notable changes to AI Dev Academy Game will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Pending Features
- Class viewer component (content display)
- Profile editor (username, avatar)
- Achievements gallery (complete view)
- Frontend tests (React Testing Library)
- E2E tests (Playwright/Cypress)

## [0.2.0] - 2025-11-01

### Added - Frontend React (JAR-234)

#### Main Game Frontend
- **Dashboard Component**: Player stats, XP bar, modules grid, recent achievements
- **ModuleViewer Component**: Class list with status, prerequisites, learning objectives
- **Notifications Component**: Toast notifications with achievement unlocks
- **GameApp Component**: Main container with header, footer, view routing
- **Home Page**: Game selection (Main Game vs Bug Hunt)

#### Infrastructure
- **TypeScript Types**: 40+ interfaces for Player, Progress, Achievement
- **API Client** (`gameApi.ts`): Complete client for backend APIs
  - Player API (CRUD + stats)
  - Progress API (full progress, module progress, unlocking)
  - Achievement API (all, player, check, unlock)
  - Helper functions (completeClass, initializePlayer)
- **State Management**: Zustand store with localStorage persistence
  - Player & stats tracking
  - Progress tracking
  - Achievement tracking
  - Notification system
  - View management
- **Routing**: React Router with /, /game, /bug-hunt routes

#### UI/UX
- Responsive design (desktop + mobile)
- Modern gradient backgrounds
- Smooth animations (hover, transitions, progress bars)
- Status badges (locked/unlocked/in_progress/completed)
- Achievement rarity colors (common/rare/epic/legendary)
- Difficulty tags (beginner/intermediate/advanced)

#### Dependencies
- Added `zustand` 4.x for state management
- Added `react-router-dom` 6.x for routing

#### Bug Fixes
- Fixed unused `useEffect` import in ModuleViewer (Codex P1)

### Changed
- Refactored Bug Hunt into separate `BugHuntApp` component
- Updated `App.tsx` to use React Router
- Separated game selection from game logic

### Technical Details
- **Files Created**: 16 files
- **Lines Added**: ~2,600 lines
- **Components**: 4 main components + 3 placeholders
- **TypeScript Interfaces**: 40+
- **API Methods**: 15+
- **CSS**: ~800 lines

## [0.1.0] - 2025-10-25

### Added - Backend FastAPI (JAR-233)

#### Player System
- **Player Routes** (`/api/player/`): CRUD endpoints for player management
- **Player Stats**: Track classes, exercises, bug hunts, streaks
- **PlayerStats Model**: Auto-created on player registration

#### Progress System
- **Progress Routes** (`/api/progress/`): Track class completion
- **Content Service**: Full curriculum structure (6 modules, 45 classes)
- **Prerequisite System**: Sequential class unlocking, module gating
- **Progress Status**: locked → unlocked → in_progress → completed

#### Achievement System
- **Achievement Routes** (`/api/achievements/`): 27 achievements
- **Auto-Unlock Logic**: Triggered by player actions
- **Achievement Categories**: learning, minigame, streak, mastery, special
- **Achievement Rarities**: common, rare, epic, legendary
- **XP Rewards**: 50-2000 XP per achievement

#### XP & Leveling
- **XP Service**: Centralized XP logic
- **Level Formula**: `level = int((xp / 100) ** 0.5) + 1`
- **Level Titles**: Junior Dev → CTO → Legend (levels 1-30+)
- **XP Sources**: Classes (100-200 XP), achievements (50-2000 XP)

#### Database
- **SQLAlchemy Models**: Player, Progress, Achievement, PlayerStats
- **Relationships**: One-to-many player relationships
- **Constraints**: Unique achievements per player

#### API Documentation
- **OpenAPI/Swagger**: Auto-generated at `/docs`
- **ReDoc**: Alternative docs at `/redoc`

#### Testing
- **Test Suite**: 106+ tests
- **Coverage**: 87.70%
- **Test Files**:
  - `test_player.py` (24 tests)
  - `test_progress.py` (20 tests)
  - `test_achievements.py` (22 tests)
  - `test_services.py` (40+ tests)

### Technical Details
- **Backend Framework**: FastAPI 0.115.5
- **Database**: SQLAlchemy 2.0.36 + SQLite
- **Validation**: Pydantic 2.10.3
- **Lines Added**: ~3,500 lines
- **Endpoints**: 17 REST endpoints
- **Models**: 4 database models

## [0.0.1] - 2025-10-18

### Added - Bug Hunt Mini-Game
- **Bug Hunt Game**: Find bugs in code snippets
- **Difficulty Levels**: Easy, Medium, Hard
- **Scoring System**: Time + accuracy based
- **Leaderboard**: Global rankings
- **React Frontend**: Complete UI with TypeScript
- **FastAPI Backend**: Game session management

### Initial Setup
- Project structure created
- Backend and frontend directories
- Basic documentation (README, SETUP, ARCHITECTURE)

---

## Version History

- **v0.2.0** (2025-11-01): Frontend React complete
- **v0.1.0** (2025-10-25): Backend FastAPI complete
- **v0.0.1** (2025-10-18): Bug Hunt mini-game + initial setup

## Links

- [GitHub Repository](https://github.com/jarkillo/master-desarrollo-ia)
- [Linear Project](https://linear.app/jarko/project/master-desarrollo-con-ia)
- [Documentation](./SETUP.md)

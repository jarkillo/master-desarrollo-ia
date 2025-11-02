# AI Dev Academy - Frontend

React + TypeScript frontend for AI Dev Academy Game.

Includes both the **Main Game** (progress tracking, achievements, modules) and the **Bug Hunt mini-game**.

## Features

### Main Game
- **Dashboard**: Player stats, XP bar, modules grid, achievements
- **Module Viewer**: Browse classes with prerequisites and learning objectives
- **Progress Tracking**: Sequential unlocking with status tracking
- **Achievement System**: 27 achievements with auto-unlock
- **Notifications**: Toast notifications for achievements and events
- **Responsive UI**: Modern design with gradients and animations
- **State Management**: Zustand with localStorage persistence
- **Routing**: React Router (/, /game, /bug-hunt)

### Bug Hunt Mini-Game
- **Difficulty Selection**: Easy, Medium, Hard, or Random
- **Interactive Code Display**: Click lines to mark bugs
- **Real-time Timer**: Live progress tracking
- **Detailed Results**: Score, XP, accuracy, performance
- **Leaderboard**: Global and difficulty-based rankings
- **Achievement Integration**: Unlocks game achievements

## Prerequisites

- Node.js 18+ (for npm)
- Backend API running on http://localhost:8000 (see `../backend/`)

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env if you need to change the API URL or player ID
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open in browser**:
   ```
   http://localhost:3000
   ```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/
│   ├── game/                         # Main Game components
│   │   ├── GameApp.tsx + .css        # Main container
│   │   ├── Dashboard.tsx + .css      # Dashboard with stats
│   │   ├── ModuleViewer.tsx + .css   # Module class list
│   │   └── Notifications.tsx + .css  # Toast notifications
│   ├── BugHuntApp.tsx                # Bug Hunt game
│   ├── BugHuntStart.tsx              # Difficulty selection
│   ├── BugHuntGame.tsx               # Main game logic
│   ├── BugHuntResults.tsx            # Results screen
│   └── BugHuntLeaderboard.tsx        # Leaderboard
├── services/
│   ├── api.ts                        # Axios config
│   ├── gameApi.ts                    # Main game API client
│   └── bugHuntApi.ts                 # Bug Hunt API client
├── stores/
│   └── gameStore.ts                  # Zustand state management
├── types/
│   ├── game.ts                       # Main game types (40+ interfaces)
│   └── bugHunt.ts                    # Bug Hunt types
├── hooks/
│   └── useTimer.ts                   # Timer hook
├── App.tsx                           # Router & home page
├── main.tsx                          # Entry point
└── index.css                         # Global styles
```

## Backend API

This frontend connects to the FastAPI backend. Make sure it's running:

```bash
cd ../backend
uvicorn app.main:app --reload
```

### Main Game API Endpoints
- `POST /api/player/` - Create player
- `GET /api/player/{id}` - Get player info
- `GET /api/player/{id}/stats` - Get player stats
- `GET /api/progress/player/{id}` - Get full progress
- `GET /api/progress/modules` - Get all modules
- `POST /api/progress/` - Create/unlock class
- `PATCH /api/progress/{id}` - Update progress
- `GET /api/achievements/` - Get all achievements
- `GET /api/achievements/player/{id}` - Get player achievements
- `POST /api/achievements/check` - Auto-check achievements

### Bug Hunt API Endpoints
- `POST /api/minigames/bug-hunt/start` - Start game
- `POST /api/minigames/bug-hunt/submit` - Submit answers
- `GET /api/minigames/bug-hunt/leaderboard` - Get rankings
- `GET /api/minigames/bug-hunt/stats/{player_id}` - Get stats

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)
- `VITE_DEFAULT_PLAYER_ID` - Player ID for testing (default: 1)

In production, player ID would come from authentication.

## Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling with dark/light mode support

## Design Features

- **Dark/Light Mode**: Automatically adapts to system preference
- **Responsive Layout**: Mobile-friendly design
- **Animations**: Smooth transitions and hover effects
- **Accessibility**: Semantic HTML and keyboard navigation

## Development Notes

- Timer uses `useTimer` custom hook with 0.1s precision
- Game state managed with React useState at App level
- API calls use async/await with error handling
- TypeScript types are generated from backend Pydantic schemas

## Future Enhancements

- [ ] Add player authentication
- [ ] Save game progress locally
- [ ] Add sound effects and music
- [ ] Implement keyboard shortcuts
- [ ] Add tutorial mode
- [ ] Player statistics dashboard
- [ ] Social features (share results)

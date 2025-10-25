# Bug Hunt - Frontend

React + TypeScript frontend for the Bug Hunt mini-game.

## Features

- **Difficulty Selection**: Choose between Easy, Medium, Hard, or Random
- **Interactive Code Display**: Click on lines to mark bugs
- **Real-time Timer**: Track your progress with a live timer
- **Detailed Results**: See your score, XP earned, accuracy, and performance breakdown
- **Leaderboard**: Compete with other players globally or by difficulty
- **Responsive Design**: Works on desktop and mobile devices

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
├── components/         # React components
│   ├── BugHuntStart.tsx          # Difficulty selection screen
│   ├── BugHuntGame.tsx           # Main game with code display
│   ├── BugHuntResults.tsx        # Results and statistics
│   └── BugHuntLeaderboard.tsx    # Global leaderboard
├── services/           # API clients
│   ├── api.ts                    # Axios configuration
│   └── bugHuntApi.ts             # Bug Hunt API methods
├── types/              # TypeScript types
│   └── bugHunt.ts                # Game types (from backend schemas)
├── hooks/              # Custom React hooks
│   └── useTimer.ts               # Timer hook
├── App.tsx             # Main app component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## Backend API

This frontend connects to the Bug Hunt API backend. Make sure the backend is running:

```bash
cd ../backend
uvicorn app.main:app --reload
```

API endpoints used:
- `POST /api/minigames/bug-hunt/start` - Start a new game
- `POST /api/minigames/bug-hunt/submit` - Submit answers
- `GET /api/minigames/bug-hunt/leaderboard` - Get rankings
- `GET /api/minigames/bug-hunt/stats/{player_id}` - Get player stats

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

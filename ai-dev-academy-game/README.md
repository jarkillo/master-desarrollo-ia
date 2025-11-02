# AI Dev Academy - The Game

**Aprende desarrollo con IA jugando** 🎮🤖

Un juego de simulación donde progresas de Junior Developer a CTO mientras aprendes el contenido del Master en IA Development.

## 🎮 Dos Juegos en Uno

### 1. **Main Game** (React Frontend + FastAPI Backend)
Juego completo con progresión, módulos, clases y achievements.

**Features**:
- 🎯 Sistema de progreso con XP y niveles (1-30+)
- 🏆 27 achievements desbloqueables
- 📚 6 módulos con 45+ clases
- 📊 Dashboard con estadísticas completas
- 🔓 Sistema de prerequisitos y unlocking
- 💫 Notificaciones de achievements animadas
- 📱 UI responsive (desktop + mobile)

### 2. **Bug Hunt Mini-Game** (React Standalone)
Encuentra bugs en snippets de código y compite en el leaderboard.

**Features**:
- 🐛 3 niveles de dificultad
- ⏱️ Timer con scoring
- 🏅 Leaderboard global
- 📈 Accuracy tracking
- 🎯 Achievement integration

## Características Generales

- 🎯 **Sistema de Progreso**: XP, niveles, skills desbloqueables
- 🏆 **Achievements**: 27 logros con rarities (common/rare/epic/legendary)
- 🤖 **Backend Completo**: FastAPI con Player, Progress, Achievement APIs
- 🎨 **UI Moderna**: React + TypeScript con Zustand state management
- 💾 **Persistencia**: Auto-save en localStorage + backend database
- 🎮 **Mini-Games**: Bug Hunt completamente funcional
- 📊 **Estadísticas**: Tracking completo de progreso y racha

## 🚀 Quick Start

### Backend (FastAPI)

```bash
cd ai-dev-academy-game/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`

### Frontend (React)

```bash
cd ai-dev-academy-game/frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Full Setup Guide

Ver [SETUP.md](./SETUP.md) para instrucciones completas de instalación y configuración.

## Cómo Jugar

1. Crea tu personaje al iniciar
2. Completa clases del Master para ganar XP
3. Desbloquea herramientas y agentes
4. Mejora tu workspace
5. Completa mini-games para bonus XP
6. ¡Alcanza el nivel Master!

## Estructura del Juego

```
Nivel 1-5:   Junior Developer (Módulo 0)
Nivel 6-10:  Mid Developer (Módulo 1)
Nivel 11-15: Senior Developer (Módulo 2)
Nivel 16-20: Tech Lead (Módulo 3)
Nivel 21-25: Architect (Módulo 4)
Nivel 26-30: CTO (Módulo 5)
```

## Progresión

- Cada clase completada: +100 XP
- Cada ejercicio: +50 XP
- Proyecto final de módulo: +500 XP
- Racha diaria: +10% bonus
- Mini-game ganado: +100 XP

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** 0.115.5 - Web framework
- **SQLAlchemy** 2.0.36 - ORM
- **Pydantic** 2.10.3 - Data validation
- **Uvicorn** 0.32.1 - ASGI server
- **Python** 3.12+

### Frontend
- **React** 18.2.0 - UI framework
- **TypeScript** 5.2.2 - Type safety
- **Vite** 7.1.12 - Build tool
- **Zustand** 4.x - State management
- **React Router** 6.x - Routing
- **Axios** 1.6.0 - HTTP client

### Database
- **SQLite** (development)
- **PostgreSQL** (production ready)

### Testing
- **Pytest** - Backend tests (106+ tests, 87%+ coverage)
- **React Testing Library** - Frontend tests (pending)

## Licencia

MIT

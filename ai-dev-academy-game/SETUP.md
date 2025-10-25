# Bug Hunt - Setup Completo

Guía completa para configurar y ejecutar el mini-juego Bug Hunt.

## Requisitos Previos

- Python 3.12+ (backend)
- Node.js 18+ (frontend)
- Git

## Setup Inicial (Solo una vez)

### 1. Backend Setup

```bash
cd ai-dev-academy-game/backend

# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear player de prueba
python -c "
from app.database import SessionLocal
from app.models import Player, PlayerStats
from datetime import datetime

db = SessionLocal()
player = Player(username='test_player', avatar='default.png', level=1, xp=0)
db.add(player)
db.commit()
db.refresh(player)

stats = PlayerStats(player_id=player.id, total_minigames_played=0, last_activity_date=datetime.now())
db.add(stats)
db.commit()

print(f'Player creado: ID {player.id}, Username: {player.username}')
db.close()
"
```

### 2. Frontend Setup

```bash
cd ai-dev-academy-game/frontend

# Instalar dependencias
npm install

# Crear archivo .env (copiar desde .env.example)
cp .env.example .env
# O en Windows:
copy .env.example .env

# Editar .env si es necesario (por defecto usa localhost:8000)
```

## Ejecutar el Juego

### Opción 1: Iniciar Manualmente (Desarrollo)

**Terminal 1 - Backend:**
```bash
cd ai-dev-academy-game/backend
.venv\Scripts\activate  # Windows
# O: source .venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ai-dev-academy-game/frontend
npm run dev
```

**Abrir navegador:**
```
http://localhost:3000
```

### Opción 2: Script de Inicio (Windows)

Crear `start-bug-hunt.bat`:
```batch
@echo off
echo Starting Bug Hunt...
echo.

echo [1/2] Starting Backend...
start "Bug Hunt Backend" cmd /k "cd ai-dev-academy-game\backend && .venv\Scripts\activate && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "Bug Hunt Frontend" cmd /k "cd ai-dev-academy-game\frontend && npm run dev"

echo.
echo Bug Hunt is starting!
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
pause
```

Ejecutar: `start-bug-hunt.bat`

## Verificar que Funciona

### Backend Health Check

```bash
curl http://localhost:8000/health
# Debería responder: {"status":"healthy"}
```

### Test End-to-End

```bash
python ai-dev-academy-game/test_bug_hunt_flow.py
```

Debería ver:
```
[SUCCESS] ALL TESTS PASSED - BUG HUNT IS FULLY FUNCTIONAL
```

## Estructura del Proyecto

```
ai-dev-academy-game/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── content/         # Bug templates (10 plantillas)
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Backend tests (15 tests)
│   ├── requirements.txt
│   └── ai_dev_academy.db    # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── components/      # 4 React components
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript types
│   │   └── hooks/           # Custom hooks (useTimer)
│   ├── package.json
│   └── .env                 # Config (VITE_API_URL)
│
└── test_bug_hunt_flow.py    # End-to-end test script
```

## Troubleshooting

### Backend no inicia

```bash
# Verificar que el entorno virtual está activado
which python  # Linux/Mac
where python  # Windows
# Debería mostrar la ruta del .venv

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Frontend no inicia

```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules && del package-lock.json  # Windows
npm install
```

### "Player not found" al jugar

```bash
# Verificar que existe el player
cd backend
python -c "from app.database import SessionLocal; from app.models import Player; db = SessionLocal(); print(f'Players: {db.query(Player).count()}'); db.close()"

# Si es 0, crear player (ver Setup Inicial paso 1)
```

### Puerto 8000 ya en uso

```bash
# Windows: Encontrar y matar proceso
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

## Tecnologías

**Backend:**
- FastAPI 0.118.0
- SQLAlchemy 2.0+
- Pydantic 2.11.0
- Python 3.12+

**Frontend:**
- React 18
- TypeScript (strict mode)
- Vite
- Axios

## Testing

**Backend tests:**
```bash
cd backend
pytest tests/ -v
# 15 tests, 87.70% coverage
```

**End-to-end test:**
```bash
python test_bug_hunt_flow.py
```

**Frontend** (pendiente):
```bash
cd frontend
npm test
```

## Próximos Pasos

1. ✅ Backend funcionando
2. ✅ Frontend implementado
3. ✅ End-to-end test pasando
4. ⚠️ Probar manualmente en navegador
5. 🔜 Frontend tests con Vitest
6. 🔜 Mejoras del React Integration Coach
7. 🔜 Auth real (en lugar de player ID hardcoded)

## Documentación API

Backend API documentation (Swagger):
```
http://localhost:8000/docs
```

Endpoints principales:
- `POST /api/minigames/bug-hunt/start` - Iniciar juego
- `POST /api/minigames/bug-hunt/submit` - Enviar respuestas
- `GET /api/minigames/bug-hunt/leaderboard` - Ver ranking
- `GET /api/minigames/bug-hunt/stats/{id}` - Stats del jugador

## Soporte

Para reportar issues: [JAR-238](https://linear.app/jarko/issue/JAR-238)

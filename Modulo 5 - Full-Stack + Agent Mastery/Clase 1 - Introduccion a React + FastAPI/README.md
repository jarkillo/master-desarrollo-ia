# Módulo 5 - Clase 1: Introducción a React + FastAPI

Esta clase introduce el desarrollo full-stack combinando **React + TypeScript** en el frontend con **FastAPI** en el backend, demostrando cómo crear aplicaciones web modernas con arquitectura cliente-servidor.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Instalación y Ejecución](#instalación-y-ejecución)
4. [Conceptos Clave](#conceptos-clave)
5. [🤖 AI Integration (40% del contenido)](#-ai-integration-40-del-contenido)
6. [Ejercicios y Mejoras](#ejercicios-y-mejoras)

---

## Descripción del Proyecto

Una aplicación de gestión de tareas (TODO list) que demuestra:

- **Backend**: API RESTful con FastAPI
  - Endpoints CRUD completos
  - Arquitectura limpia (Repository + Service + API)
  - CORS habilitado para desarrollo
  - Validación con Pydantic

- **Frontend**: SPA (Single Page Application) con React + TypeScript
  - Componentes funcionales con Hooks
  - Estado local con `useState`
  - Efectos con `useEffect`
  - Cliente HTTP con Axios
  - Error handling robusto

## Arquitectura

### Backend (FastAPI)

```
backend/
├── api/
│   ├── __init__.py
│   ├── api.py                    # Endpoints REST
│   ├── servicio_tareas.py        # Lógica de negocio
│   ├── repositorio_base.py       # Protocol (abstracción)
│   └── repositorio_memoria.py    # Implementación in-memory
├── tests/
│   ├── conftest.py
│   └── test_api.py               # Tests con TestClient
└── requirements.txt
```

**Endpoints disponibles**:
- `GET /` - Health check
- `POST /tareas` - Crear tarea
- `GET /tareas` - Listar todas las tareas
- `GET /tareas/{id}` - Obtener tarea específica
- `PATCH /tareas/{id}` - Actualizar estado de tarea
- `DELETE /tareas/{id}` - Eliminar tarea

### Frontend (React + TypeScript)

```
frontend/
├── src/
│   ├── components/
│   │   ├── TareasLista.tsx       # Componente principal con useState/useEffect
│   │   ├── TareaItem.tsx         # Componente individual
│   │   └── CrearTareaForm.tsx    # Formulario de creación
│   ├── services/
│   │   └── tareas.service.ts     # Cliente API con Axios
│   ├── types/
│   │   └── tarea.ts              # Tipos TypeScript
│   ├── App.tsx                   # Componente raíz
│   ├── main.tsx                  # Punto de entrada
│   └── App.css                   # Estilos
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts                # Configuración Vite + proxy
```

## Instalación y Ejecución

### Prerrequisitos

- Python 3.12+
- Node.js 18+
- npm o yarn

### 1. Backend (FastAPI)

```bash
# Navegar al directorio backend
cd backend

# Activar entorno virtual (IMPORTANTE según CLAUDE.md)
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn api.api:app --reload

# El backend estará disponible en: http://localhost:8000
# Documentación automática: http://localhost:8000/docs
```

**Ejecutar tests**:
```bash
cd backend
pytest --cov=api --cov-report=term-missing
```

### 2. Frontend (React + Vite)

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# El frontend estará disponible en: http://localhost:5173
```

**Builds de producción**:
```bash
npm run build      # Compila TypeScript + bundle optimizado
npm run preview    # Preview del build de producción
```

### 3. Ejecutar ambos simultáneamente

**Terminal 1** (Backend):
```bash
cd backend
uvicorn api.api:app --reload
```

**Terminal 2** (Frontend):
```bash
cd frontend
npm run dev
```

Abrir navegador en `http://localhost:5173` y la app estará conectada al backend.

---

## Conceptos Clave

### React Hooks Fundamentales

#### `useState` - Manejo de Estado Local

```tsx
const [tareas, setTareas] = useState<Tarea[]>([]);

// Actualizar estado
setTareas([...tareas, nuevaTarea]);

// Actualizar estado basado en valor previo
setTareas((prev) => [...prev, nuevaTarea]);
```

**Por qué usar `useState`**:
- React necesita saber cuándo re-renderizar componentes
- El estado mutable fuera de `useState` no dispara re-renders
- `useState` garantiza que los cambios se reflejen en la UI

#### `useEffect` - Efectos Secundarios

```tsx
useEffect(() => {
  // Este código se ejecuta después del render
  cargarTareas();
}, []); // Array vacío = solo ejecutar al montar
```

**Casos de uso**:
- Fetch de datos al montar componente
- Suscripciones a eventos
- Timers/intervals
- Sincronización con APIs externas

### TypeScript en React

**Ventajas**:
- Type safety: detecta errores en tiempo de desarrollo
- Autocompletado y IntelliSense
- Refactoring seguro
- Documentación viva

**Ejemplo**:
```tsx
interface TareaItemProps {
  tarea: Tarea;
  onToggle: (id: number, completada: boolean) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

export function TareaItem({ tarea, onToggle, onDelete }: TareaItemProps) {
  // TypeScript valida que las props coincidan con la interfaz
}
```

### Axios vs Fetch

Este proyecto usa **Axios** porque:
- ✅ Manejo automático de JSON
- ✅ Interceptors para logging/auth
- ✅ Timeout configurables
- ✅ Mejor manejo de errores
- ✅ Soporte para cancelación de requests

```tsx
// Axios
const response = await api.get<Tarea[]>('/tareas');
return response.data;

// Fetch (requiere más código)
const response = await fetch('/api/tareas');
if (!response.ok) throw new Error('Error');
return await response.json();
```

### FastAPI + CORS

Para que React pueda comunicarse con FastAPI en desarrollo, se necesita **CORS**:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puerto de Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternativa**: Vite proxy (ya configurado en `vite.config.ts`).

---

## 🤖 AI Integration (40% del contenido)

Esta sección demuestra cómo usar **IA como co-piloto** para acelerar el desarrollo full-stack.

### 1. Generación de Componentes React con IA

#### Prompt para crear componente nuevo:

```
Crea un componente React TypeScript llamado FiltroTareas que:
- Reciba como props: filtro actual y callback onChange
- Tenga 3 botones: "Todas", "Activas", "Completadas"
- Use TypeScript con tipos explícitos
- Siga los patrones de los componentes existentes en este proyecto
```

#### Prompt para refactorizar componente:

```
Refactoriza TareasLista.tsx para:
- Extraer la lógica de fetch a un custom hook useTareas()
- Mejorar el error handling con estados más granulares
- Agregar loading states por operación (crear, actualizar, eliminar)
```

### 2. Debugging con IA

#### Prompt efectivo para debuggear:

```
Mi componente React no se actualiza cuando cambio el estado.
Código:
[pegar código]

Backend responde correctamente, pero la UI no refleja los cambios.
¿Qué estoy haciendo mal?
```

**La IA puede detectar**:
- Estado mutado directamente (sin `setState`)
- Dependencias faltantes en `useEffect`
- Keys duplicadas en listas
- Async/await mal manejado

### 3. Testing con Asistencia IA

#### Prompt para generar tests:

```
Genera tests unitarios para el componente TareaItem.tsx usando:
- React Testing Library
- Jest
- TypeScript
- Mocks para las props callbacks

Casos a cubrir:
- Render básico
- Click en checkbox llama onToggle
- Click en botón eliminar muestra confirmación
- Estados de loading
```

### 4. Mejoras de Performance con IA

#### Prompt para optimización:

```
Analiza TareasLista.tsx y sugiere optimizaciones usando:
- useMemo para cálculos costosos
- useCallback para callbacks que se pasan a componentes hijos
- React.memo para componentes que re-renderizan innecesariamente

Explica cuándo SÍ y cuándo NO aplicar estas optimizaciones.
```

### 5. Agentes Educacionales Recomendados

Para esta clase, usa los siguientes agentes (desde `.claude/agents/educational/`):

1. **React Integration Coach**
   - Revisa patrones de integración React + FastAPI
   - Detecta anti-patterns como fetch directo sin error handling
   - Enseña state management

   ```bash
   # Invocación sugerida
   "Revisa src/components/TareasLista.tsx con React Integration Coach"
   ```

2. **FastAPI Design Coach**
   - Valida diseño de endpoints REST
   - Revisa uso correcto de status codes
   - Verifica Pydantic models

   ```bash
   "Revisa backend/api/api.py con FastAPI Design Coach"
   ```

3. **API Design Reviewer**
   - Asegura principios RESTful
   - Valida consistencia de respuestas
   - Revisa documentación OpenAPI

   ```bash
   "Revisa endpoints de backend/api/api.py con API Design Reviewer"
   ```

### 6. Prompts de Desarrollo Incremental

#### Agregar autenticación JWT:

```
Implementa autenticación JWT en esta app siguiendo estos pasos:
1. Agrega endpoint /auth/login en FastAPI
2. Usa python-jose para generar tokens
3. Crea middleware de autenticación
4. En React, almacena token en localStorage
5. Agrega interceptor de Axios para incluir token en headers
6. Maneja expiración de token y refresh

Muéstrame el código paso a paso, explicando cada decisión.
```

#### Migrar a React Query:

```
Refactoriza el manejo de estado en TareasLista.tsx para usar React Query:
- Reemplaza useState + useEffect por useQuery
- Usa useMutation para crear/actualizar/eliminar
- Implementa cache invalidation correcta
- Agrega optimistic updates

Compara el código antes/después y explica las ventajas.
```

### 7. Generación de Documentación con IA

#### Prompt para README automático:

```
Genera documentación completa para el componente TareasLista.tsx incluyendo:
- Descripción de responsabilidades
- Props y tipos
- Estados internos
- Hooks utilizados
- Diagramas de flujo de datos (Mermaid)
- Ejemplos de uso
```

### 8. Code Review con IA antes de Commit

#### Prompt pre-commit:

```
Actúa como senior developer y haz code review de estos cambios:
[git diff]

Busca específicamente:
- Type safety issues en TypeScript
- Posibles memory leaks (listeners no removidos)
- Errores no manejados
- Violaciones de principios SOLID
- Performance issues
- Accesibilidad (a11y)

Prioriza por severidad: crítico, alto, medio, bajo.
```

### 9. Migración de JavaScript a TypeScript con IA

Si tienes código legacy en JS:

```
Convierte este componente React de JavaScript a TypeScript:
[código JS]

Requisitos:
- Inferir tipos de props correctamente
- Tipar estado y variables locales
- Agregar tipos para callbacks
- Documentar con JSDoc los tipos complejos
```

### 10. Prompts para Aprender Conceptos

#### Entender Closures en Hooks:

```
Explica por qué este código tiene un bug de stale closure:

const [count, setCount] = useState(0);

useEffect(() => {
  const interval = setInterval(() => {
    console.log(count); // Siempre imprime 0
  }, 1000);
  return () => clearInterval(interval);
}, []);

Dame 3 formas de solucionarlo y explica cuándo usar cada una.
```

#### Entender Re-renders:

```
Dibuja un diagrama de flujo mostrando:
1. Cuándo React decide re-renderizar un componente
2. Cómo se propagan los re-renders por el árbol de componentes
3. Qué optimizaciones previenen re-renders innecesarios

Usa el componente TareasLista.tsx como ejemplo.
```

---

## Ejercicios y Mejoras

### 🎯 Ejercicios Guiados (con IA)

#### Ejercicio 1: Agregar Filtros
**Objetivo**: Filtrar tareas por estado (todas/activas/completadas)

**Prompt sugerido**:
```
Guíame paso a paso para agregar filtros a TareasLista.tsx:
1. Agregar estado para filtro activo
2. Crear componente FiltroTareas con 3 botones
3. Implementar lógica de filtrado
4. Mantener la lista filtrada reactiva
```

#### Ejercicio 2: Persistencia Local
**Objetivo**: Guardar tareas en localStorage

**Prompt sugerido**:
```
Implementa persistencia local en esta app:
- Sincroniza estado de React con localStorage
- Usa un custom hook useLocalStorage
- Maneja casos edge (localStorage lleno, JSON inválido)
- Agrega botón "Limpiar todo"
```

#### Ejercicio 3: Edición Inline
**Objetivo**: Permitir editar nombre de tarea sin modal

**Prompt sugerido**:
```
Agrega edición inline a TareaItem.tsx:
- Doble click en tarea habilita modo edición
- Muestra input con valor actual
- Enter guarda, Escape cancela
- Usa estado local para modo edición
- Valida que nombre no esté vacío
```

### 🚀 Mejoras Avanzadas

1. **React Query**: Migrar de `useState` + `useEffect` a `useQuery` + `useMutation`
2. **Zustand/Redux**: Implementar state management global
3. **React Router**: Agregar rutas (`/tareas`, `/estadisticas`)
4. **Drag & Drop**: Reordenar tareas con `react-beautiful-dnd`
5. **Dark Mode**: Implementar tema oscuro con Context API
6. **i18n**: Internacionalización con `react-i18next`
7. **PWA**: Convertir en Progressive Web App
8. **Animaciones**: Agregar transiciones con `framer-motion`

### 🤖 Usa IA para cada mejora

**Ejemplo - React Query**:
```
Migremos esta app a React Query. Muéstrame:
1. Setup de QueryClient
2. Custom hook useObtenerTareas con useQuery
3. Custom hook useMutarTarea con useMutation
4. Configuración de cache invalidation
5. Comparación antes/después del código
6. Cuándo esta migración SÍ vale la pena
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [React Docs](https://react.dev/) - Nueva docs con Hooks primero
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Axios Docs](https://axios-http.com/docs/intro)

### Tutoriales con IA
- **Prompt Engineering for Developers** (OpenAI)
- **React + TypeScript Cheatsheet** (generado con IA)
- **FastAPI Best Practices** (pide a la IA que lo genere)

### Herramientas AI
- **GitHub Copilot**: Autocompletado inteligente
- **Cursor**: IDE con IA integrada
- **Claude Code**: Agentes especializados para educación
- **ChatGPT/Claude**: Mentores disponibles 24/7

---

## 🎓 Aprendizajes Clave de esta Clase

1. ✅ **React Hooks**: `useState` y `useEffect` son fundamentales para componentes funcionales
2. ✅ **TypeScript**: Type safety previene bugs y mejora DX (Developer Experience)
3. ✅ **Axios + Error Handling**: Manejo robusto de comunicación cliente-servidor
4. ✅ **Clean Architecture**: Separación de responsabilidades (Repo + Service + API)
5. ✅ **CORS**: Entender comunicación cross-origin en desarrollo
6. ✅ **IA como Co-Piloto**: Usar IA para acelerar desarrollo, debugging y aprendizaje

---

## 🤖 Conclusión: El Poder de IA + Full-Stack

Esta clase demuestra que:

- **IA no reemplaza al desarrollador**, lo potencia
- Puedes construir aplicaciones full-stack complejas **más rápido** con IA
- Los **agentes educacionales** enseñan mejores prácticas mientras desarrollas
- El **40% de contenido IA** no es "extra", es parte integral del aprendizaje moderno

### Siguiente Paso

**Módulo 5, Clase 2**: State Management avanzado (Context, Zustand, React Query) con orquestación de agentes IA.

---

**¿Tienes dudas?** Usa los agentes educacionales o pregunta directamente:

```
Explica [concepto] usando analogías del mundo real y ejemplos de esta app.
```

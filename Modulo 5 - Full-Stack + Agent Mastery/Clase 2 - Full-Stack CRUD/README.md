# Módulo 5 - Clase 2: Full-Stack CRUD Completo

Esta clase lleva el desarrollo full-stack al siguiente nivel implementando un **CRUD completo** con las mejores prácticas modernas: **React Hook Form + Zod** para validación, **React Query** para data fetching con optimistic updates, y manejo robusto de estados de carga y error.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Nuevas Tecnologías](#nuevas-tecnologías)
3. [Arquitectura](#arquitectura)
4. [Instalación y Ejecución](#instalación-y-ejecución)
5. [Conceptos Clave](#conceptos-clave)
6. [🤖 AI Integration (40% del contenido)](#-ai-integration-40-del-contenido)
7. [Diferencias con Clase 1](#diferencias-con-clase-1)
8. [Ejercicios y Mejoras](#ejercicios-y-mejoras)

---

## Descripción del Proyecto

Una aplicación de gestión de tareas (TODO list) con CRUD completo que demuestra:

### Backend Mejorado

- ✅ **API RESTful completa** con todos los endpoints CRUD
- ✅ **Validación robusta** con Pydantic (min/max length)
- ✅ **Error handling mejorado** con excepciones personalizadas
- ✅ **Estadísticas** endpoint adicional
- ✅ **HTTP status codes correctos** (201, 204, 404, etc.)
- ✅ **Documentación automática** con OpenAPI

### Frontend Avanzado

- ✅ **React Hook Form** para formularios con validación
- ✅ **Zod** para schemas de validación type-safe
- ✅ **React Query** para data fetching, caching y sincronización
- ✅ **Optimistic Updates** UI instantánea sin esperar al servidor
- ✅ **Loading states** granulares por operación
- ✅ **Error handling** robusto con mensajes amigables
- ✅ **Modal de edición** para actualizar tareas
- ✅ **Estadísticas en tiempo real**

---

## Nuevas Tecnologías

### React Hook Form

**¿Qué es?** Biblioteca de gestión de formularios con mínimo re-rendering.

**¿Por qué usarla?**
- ✅ Menos re-renders = mejor performance
- ✅ Integración nativa con Zod
- ✅ Validación en tiempo real
- ✅ API simple y declarativa

**Alternativas**: Formik, React Final Form, manual con useState

### Zod

**¿Qué es?** Schema validation con TypeScript-first approach.

**¿Por qué usarla?**
- ✅ Type inference automático (types desde schemas)
- ✅ Validaciones declarativas y composables
- ✅ Mensajes de error personalizables
- ✅ Runtime + compile-time safety

**Alternativas**: Yup, Joi, class-validator

### React Query (TanStack Query)

**¿Qué es?** Biblioteca de data fetching con caching, sincronización y más.

**¿Por qué usarla?**
- ✅ Cache automático inteligente
- ✅ Optimistic updates out-of-the-box
- ✅ Retry lógica configurable
- ✅ Loading/error states automáticos
- ✅ Revalidación en background
- ✅ Menos código boilerplate

**Alternativas**: SWR, Apollo Client (GraphQL), RTK Query

---

## Arquitectura

### Backend (FastAPI)

```
backend/
├── api/
│   ├── api.py                    # Endpoints REST con error handling
│   ├── servicio_tareas.py        # Lógica de negocio + validaciones
│   ├── repositorio_base.py       # Protocol (abstracción)
│   └── repositorio_memoria.py    # Implementación in-memory
├── tests/
│   ├── conftest.py
│   └── test_api.py               # 20+ tests (CRUD + edge cases)
└── requirements.txt
```

**Endpoints disponibles**:
- `GET /` - Health check
- `POST /tareas` - Crear tarea (201 Created)
- `GET /tareas` - Listar todas las tareas
- `GET /tareas/{id}` - Obtener tarea específica (404 si no existe)
- `PATCH /tareas/{id}` - Actualizar tarea (parcial)
- `DELETE /tareas/{id}` - Eliminar tarea (204 No Content)
- `GET /tareas-estadisticas` - Estadísticas (total, completadas, pendientes)

### Frontend (React + TypeScript)

```
frontend/
├── src/
│   ├── components/
│   │   ├── TareasLista.tsx       # Componente principal con React Query
│   │   ├── TareaItem.tsx         # Item con acciones (editar/eliminar)
│   │   ├── CrearTareaForm.tsx    # Formulario con RHF + Zod
│   │   └── EditarTareaModal.tsx  # Modal de edición
│   ├── hooks/
│   │   └── useTareas.ts          # Custom hooks con React Query
│   ├── services/
│   │   └── tareas.service.ts     # Cliente API con Axios
│   ├── types/
│   │   └── tarea.ts              # Tipos TypeScript
│   ├── App.tsx
│   ├── App.css                   # Estilos con estados de loading
│   └── main.tsx                  # Setup de QueryClient
├── package.json
└── vite.config.ts
```

---

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
pytest --cov=api --cov-report=term-missing -v
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

Abrir navegador en `http://localhost:5173`.

---

## Conceptos Clave

### React Hook Form + Zod

#### ¿Por qué esta combinación?

**Problema con useState para forms**:
```tsx
// ❌ Mucho código boilerplate
const [nombre, setNombre] = useState('');
const [error, setError] = useState('');

const handleSubmit = (e) => {
  e.preventDefault();
  if (!nombre.trim()) {
    setError('Nombre requerido');
    return;
  }
  // ...
};
```

**Solución con RHF + Zod**:
```tsx
// ✅ Declarativo y type-safe
const schema = z.object({
  nombre: z.string().min(1, 'Nombre requerido').max(200),
});

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema),
});
```

#### Ventajas

1. **Type inference**: TypeScript infiere tipos desde el schema
2. **Menos re-renders**: RHF usa refs internamente
3. **Validación declarativa**: Define reglas, no lógica imperativa
4. **Reutilizable**: Schemas se pueden componer y reutilizar

#### Ejemplo completo (CrearTareaForm.tsx)

```tsx
const tareaSchema = z.object({
  nombre: z
    .string()
    .min(1, 'El nombre es requerido')
    .max(200, 'Máximo 200 caracteres')
    .trim(),
});

type TareaFormData = z.infer<typeof tareaSchema>;

export function CrearTareaForm() {
  const crearTarea = useCrearTarea();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<TareaFormData>({
    resolver: zodResolver(tareaSchema),
  });

  const onSubmit = async (data: TareaFormData) => {
    await crearTarea.mutateAsync(data);
    reset(); // Limpiar form
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('nombre')} />
      {errors.nombre && <span>{errors.nombre.message}</span>}
      <button type="submit">Crear</button>
    </form>
  );
}
```

### React Query

#### ¿Por qué React Query?

**Problema con useState + useEffect**:
```tsx
// ❌ Código imperativo, sin cache, sin retry
const [tareas, setTareas] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  setLoading(true);
  fetch('/api/tareas')
    .then(r => r.json())
    .then(setTareas)
    .catch(setError)
    .finally(() => setLoading(false));
}, []);
```

**Solución con React Query**:
```tsx
// ✅ Declarativo, con cache, retry automático
const { data: tareas, isLoading, isError } = useQuery({
  queryKey: ['tareas'],
  queryFn: tareasService.listar,
});
```

#### Características principales

##### 1. Caching automático

React Query cachea los datos y los reutiliza:
```tsx
// Primera llamada: fetch del servidor
const { data } = useTareas(); // HTTP request

// Segunda llamada (mismo componente o diferente): cache hit
const { data } = useTareas(); // Cache (sin HTTP)
```

##### 2. Revalidación en background

Mantiene los datos actualizados sin notificar al usuario:
```tsx
useQuery({
  queryKey: ['tareas'],
  queryFn: tareasService.listar,
  staleTime: 60000, // Considerar data "fresca" por 1 minuto
  refetchOnWindowFocus: true, // Refetch al volver a la pestaña
});
```

##### 3. Retry automático

Reintentos configurables en caso de error:
```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1, // 1 reintento en caso de fallo
    },
  },
});
```

##### 4. Optimistic Updates

Actualiza la UI inmediatamente sin esperar al servidor:

```tsx
export function useCrearTarea() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: tareasService.crear,

    onMutate: async (nuevaTarea) => {
      // 1. Cancelar queries en progreso
      await queryClient.cancelQueries({ queryKey: ['tareas'] });

      // 2. Snapshot del estado actual
      const tareasPrevias = queryClient.getQueryData(['tareas']);

      // 3. Actualizar cache optimísticamente
      queryClient.setQueryData(['tareas'], (old) => [...old, nuevaTarea]);

      // 4. Retornar snapshot para rollback
      return { tareasPrevias };
    },

    onError: (error, variables, context) => {
      // Rollback en caso de error
      queryClient.setQueryData(['tareas'], context.tareasPrevias);
    },

    onSettled: () => {
      // Siempre refrescar al final
      queryClient.invalidateQueries({ queryKey: ['tareas'] });
    },
  });
}
```

**Flujo visual**:
```
User crea tarea → UI se actualiza INMEDIATAMENTE (optimistic)
                     ↓
                  Enviar request al servidor
                     ↓
                ¿Success o Error?
                     ↓
    Success: Cache se confirma
    Error: Rollback al estado anterior
```

##### 5. Estados granulares

React Query provee estados detallados:

```tsx
const {
  data,
  isLoading,      // Primera carga
  isFetching,     // Refetch en background
  isError,        // Hubo error
  error,          // Objeto de error
  isSuccess,      // Query exitosa
} = useTareas();
```

**Diferencia entre `isLoading` e `isFetching`**:
- `isLoading`: No hay data y está cargando (spinner grande)
- `isFetching`: Ya hay data pero está refrescando (spinner pequeño)

---

## 🤖 AI Integration (40% del contenido)

Esta sección demuestra cómo usar **IA como co-piloto** para implementar features complejas de forma rápida y correcta.

### 1. Generación de Formularios con React Hook Form + Zod

#### Prompt para generar formulario completo:

```
Crea un formulario React con React Hook Form + Zod para editar una tarea que tenga:
- Campo nombre (string, 1-200 caracteres, requerido)
- Campo descripción (string, opcional, max 500 caracteres)
- Campo prioridad (enum: "baja", "media", "alta")
- Campo fecha límite (date, opcional)
- Validación completa con Zod
- Mensajes de error en español
- TypeScript con tipos inferidos del schema
- onSubmit que reciba los datos tipados
```

**La IA generará**:
1. Schema Zod completo con validaciones
2. Tipos TypeScript inferidos
3. Formulario con `register()` para cada campo
4. Manejo de errores por campo
5. Submit handler tipado

#### Prompt para migrar formulario existente:

```
Tengo este formulario con useState:
[código actual]

Migralo a React Hook Form + Zod manteniendo:
- Las mismas validaciones
- Los mismos mensajes de error
- El mismo comportamiento de submit
- Mejora la UX con validación en tiempo real
```

### 2. Implementación de React Query con Optimistic Updates

#### Prompt para custom hook con React Query:

```
Crea un custom hook useProductos usando React Query que:
- Tenga query para listar productos
- Tenga mutation para crear con optimistic update
- Tenga mutation para actualizar con optimistic update
- Tenga mutation para eliminar con optimistic update
- Implemente rollback en caso de error
- Invalide cache automáticamente
- Use TypeScript con tipos Product

API:
- GET /productos → Product[]
- POST /productos → Product
- PATCH /productos/:id → Product
- DELETE /productos/:id → void
```

**La IA generará**:
1. Setup de queries con `useQuery`
2. Mutations con `useMutation`
3. Lógica de `onMutate`, `onError`, `onSettled`
4. Manejo de cache con `queryClient`
5. TypeScript types correctos

#### Prompt para debugging de optimistic updates:

```
Mi optimistic update no funciona correctamente:
- UI se actualiza pero luego se revierte
- Cache no se sincroniza con el servidor
- Errores no hacen rollback

Código:
[pegar código del hook]

Identifica el problema y explica:
1. Qué está mal
2. Por qué falla
3. Cómo arreglarlo con código corregido
```

### 3. Manejo Robusto de Estados de Loading/Error

#### Prompt para mejorar UX de loading:

```
Mi componente muestra un spinner global mientras carga.
Mejóralo para:
- Mostrar skeleton loading en lugar de spinner
- Mantener datos antiguos mientras refresca (no mostrar loading)
- Mostrar loading solo en acciones del usuario (crear/actualizar)
- Diferenciar entre "primera carga" y "refetch"

Componente actual:
[código]
```

**La IA sugerirá**:
1. Usar `isFetching` vs `isLoading`
2. Implementar skeleton components
3. Deshabilitar botones durante mutations
4. Mostrar spinners inline en botones

#### Prompt para error handling mejorado:

```
Implementa error handling robusto en esta app:
- Toast notifications para errores
- Diferentes mensajes según tipo de error (network, validation, server)
- Retry manual para el usuario
- Fallback UI cuando falla una query
- Log de errores a Sentry

Usa React Query error boundaries y error states.
```

### 4. Agentes Educacionales Recomendados

Para esta clase, usa los siguientes agentes (desde `.claude/agents/educational/`):

#### 1. React Integration Coach

Revisa patrones avanzados de React:

```bash
"Revisa src/hooks/useTareas.ts con React Integration Coach"
```

**Detecta**:
- Anti-patterns en custom hooks
- Problemas de re-renders
- Errores en gestión de estado
- Falta de memoization donde es necesaria

#### 2. Performance Optimizer

Optimiza performance de la app:

```bash
"Analiza la app completa con Performance Optimizer para encontrar bottlenecks"
```

**Identifica**:
- Re-renders innecesarios
- Cálculos costosos sin `useMemo`
- Callbacks sin `useCallback`
- Queries que se ejecutan demasiado frecuentemente

#### 3. API Design Reviewer

Valida diseño de endpoints REST:

```bash
"Revisa backend/api/api.py con API Design Reviewer"
```

**Verifica**:
- HTTP status codes correctos
- Naming de endpoints (RESTful)
- Estructura de responses consistente
- Error handling apropiado

### 5. Debugging Avanzado con IA

#### Prompt para debuggear React Query:

```
Mi query de React Query se ejecuta infinitas veces.

Código del hook:
[código]

Componente que lo usa:
[código]

¿Qué está causando el loop infinito?
Explica el problema y muestra la solución.
```

**La IA detectará**:
- `queryKey` que cambia en cada render
- Dependencias faltantes en `useEffect`
- Estado actualizado durante render
- Referencias que cambian (funciones sin `useCallback`)

#### Prompt para debuggear Zod validation:

```
Mi validación de Zod no funciona como espero:

Schema:
[código del schema]

Input del usuario:
[ejemplo de input]

Error recibido:
[mensaje de error]

Esperaba:
[comportamiento esperado]

¿Qué está mal en mi schema?
```

### 6. Testing Avanzado con IA

#### Prompt para tests de React Query:

```
Genera tests completos para este custom hook que usa React Query:
[código del hook]

Casos a cubrir:
- Query exitosa retorna datos
- Query en loading muestra estado correcto
- Query con error maneja error correctamente
- Mutation con optimistic update actualiza cache
- Rollback funciona si mutation falla
- Cache invalidation después de mutation

Usa:
- @testing-library/react
- @testing-library/react-hooks
- Jest
- MSW (Mock Service Worker) para API
```

**La IA generará**:
1. Setup de QueryClient para tests
2. Mocks de API con MSW
3. Tests para cada caso
4. Asserts de estado de cache
5. Tests de rollback

#### Prompt para tests de formularios:

```
Genera tests para este formulario con React Hook Form + Zod:
[código del componente]

Casos:
- Validación de campo vacío
- Validación de max length
- Submit con datos válidos llama a callback
- Submit con datos inválidos muestra errores
- Reset limpia el formulario
- Validación en tiempo real funciona

Usa React Testing Library y user-event.
```

### 7. Refactoring Guiado por IA

#### Prompt para extraer lógica a custom hooks:

```
Este componente tiene demasiada lógica:
[código del componente con useState + useEffect + handlers]

Refactorízalo:
1. Extrae data fetching a custom hook useTareas()
2. Extrae form logic a useFormTareas()
3. Extrae filtros a useFiltroTareas()
4. Mantén el componente como "presentational"
5. Asegura que no hay pérdida de funcionalidad
6. Agrega TypeScript types apropiados

Muestra el código antes/después con explicaciones.
```

#### Prompt para optimización de performance:

```
Optimiza este componente para performance:
[código]

Aplica:
- React.memo donde sea apropiado
- useMemo para cálculos costosos
- useCallback para callbacks pasados como props
- Lazy loading de componentes pesados
- Code splitting si es necesario

IMPORTANTE: Explica CUÁNDO SÍ y CUÁNDO NO aplicar cada optimización.
No sobre-optimices.
```

### 8. Migración de Clase 1 a Clase 2 con IA

#### Prompt para migración completa:

```
Tengo una app (Clase 1) con:
- useState + useEffect para data fetching
- Formularios manuales con useState
- Error handling básico con try/catch

Quiero migrarla a (Clase 2):
- React Query para data fetching
- React Hook Form + Zod para formularios
- Optimistic updates
- Error/loading states robustos

Guíame paso a paso:
1. Qué instalar (dependencias)
2. Cómo configurar QueryClient
3. Cómo migrar cada parte (con código)
4. Qué testear para validar la migración
5. Pros/cons de la migración

Código actual:
[pegar código de Clase 1]
```

### 9. Generación de Documentación con IA

#### Prompt para documentar custom hook:

```
Genera documentación completa para este custom hook:
[código de useTareas.ts]

Incluye:
- Descripción de qué hace
- Parámetros y retorno (JSDoc)
- Ejemplos de uso en componentes
- Casos edge que maneja
- Diagrama de flujo (Mermaid) de optimistic update
- Consideraciones de performance
```

#### Prompt para README de feature:

```
Genera sección de README explicando la feature "Optimistic Updates" en esta app.

Incluye:
- Qué es un optimistic update
- Por qué lo usamos
- Cómo funciona en esta app (código + flujo)
- Qué pasa si el server falla
- Beneficios de UX
- Comparación con enfoque tradicional
- GIF o diagrama mostrando el flujo

Audiencia: Estudiantes de master que conocen React básico.
```

### 10. Prompts para Aprender Conceptos Avanzados

#### Entender cache de React Query:

```
Explica el sistema de cache de React Query:
1. ¿Cómo decide cuándo usar cache vs hacer request?
2. ¿Qué es staleTime vs cacheTime?
3. ¿Cómo funcionan las query keys?
4. ¿Cuándo invalida cache automáticamente?
5. ¿Cómo forzar un refetch?

Usa analogías del mundo real y ejemplos de esta app.
Dibuja un diagrama de flujo mostrando el ciclo de vida de una query.
```

#### Entender Zod vs TypeScript types:

```
Explica la diferencia entre Zod y TypeScript types:

TypeScript types:
interface User {
  name: string;
  age: number;
}

Zod schema:
const userSchema = z.object({
  name: z.string(),
  age: z.number(),
});

Preguntas:
1. ¿Cuándo se validan tipos de TS vs Zod?
2. ¿Por qué necesitamos ambos?
3. ¿Cuándo usar Zod y cuándo solo TS?
4. ¿Cómo hacer que trabajen juntos (z.infer)?

Dame ejemplos de casos reales donde Zod previene bugs que TS no puede.
```

---

## Diferencias con Clase 1

| Aspecto | Clase 1 | Clase 2 |
|---------|---------|---------|
| **Formularios** | Manual con `useState` | React Hook Form + Zod |
| **Validación** | Imperativa con `if` | Declarativa con schemas |
| **Data Fetching** | `useState` + `useEffect` | React Query |
| **Cache** | Sin cache | Cache automático |
| **Optimistic Updates** | No implementados | Sí, con rollback |
| **Loading States** | Global (un spinner) | Granular por operación |
| **Error Handling** | Básico con `try/catch` | Robusto con retry y fallbacks |
| **CRUD** | Solo crear y toggle | Completo (crear, editar, eliminar) |
| **Estadísticas** | No | Sí, en tiempo real |
| **Modal** | No | Sí, para editar |

### ¿Cuándo usar Clase 1 vs Clase 2?

**Usa enfoque de Clase 1** si:
- Proyecto muy pequeño (1-2 features simples)
- No necesitas cache ni sync
- Formularios triviales (1-2 campos sin validación compleja)
- Prototipo rápido o POC

**Usa enfoque de Clase 2** si:
- App de producción
- Múltiples formularios con validaciones
- Necesitas UX fluida con optimistic updates
- Performance es importante (cache, menos re-renders)
- Equipo grande (código más mantenible)

---

## Ejercicios y Mejoras

### 🎯 Ejercicios Guiados (con IA)

#### Ejercicio 1: Agregar Campo de Descripción

**Objetivo**: Extender las tareas con un campo de descripción opcional.

**Prompt sugerido**:
```
Agrega un campo "descripción" (opcional, max 500 caracteres) a las tareas:
1. Actualiza backend (modelo + endpoints)
2. Actualiza schema de Zod
3. Agrega textarea al formulario
4. Muestra descripción en TareaItem (expandible)
5. Actualiza tests

Guíame paso a paso con código.
```

#### Ejercicio 2: Filtros y Búsqueda

**Objetivo**: Filtrar tareas por estado y buscar por texto.

**Prompt sugerido**:
```
Implementa filtros en TareasLista:
- Filtro: Todas / Activas / Completadas
- Búsqueda por nombre (debounced)
- Query params en React Query para cada filtro
- Persistir filtros en localStorage
- UI con botones y search input

¿Cómo estructurar las query keys para que el cache funcione correctamente?
```

#### Ejercicio 3: Drag & Drop para Reordenar

**Objetivo**: Permitir reordenar tareas con drag & drop.

**Prompt sugerido**:
```
Agrega drag & drop para reordenar tareas usando react-beautiful-dnd:
1. Instalar y configurar la librería
2. Agregar campo "orden" en el modelo
3. Implementar onDragEnd con optimistic update
4. Persistir nuevo orden en backend
5. Manejar errores y rollback

Muestra código completo con TypeScript.
```

### 🚀 Mejoras Avanzadas

#### 1. Paginación con React Query

**Prompt**:
```
Implementa paginación infinita en la lista de tareas usando:
- useInfiniteQuery de React Query
- Infinite scroll con Intersection Observer
- Loading skeleton mientras carga más
- Backend que soporte paginación (?page=1&limit=20)
```

#### 2. Mutaciones en Batch

**Prompt**:
```
Implementa "marcar todas como completadas" con:
- Un solo request al backend (PATCH /tareas/batch)
- Optimistic update de todas las tareas
- Rollback individual si alguna falla
- Progress indicator mostrando N/M completadas
```

#### 3. Persistencia Local como Fallback

**Prompt**:
```
Agrega modo offline:
- Detectar cuando no hay conexión (navigator.onLine)
- Guardar mutations en cola (indexedDB)
- Sincronizar cuando vuelve la conexión
- Mostrar badge "offline" al usuario
- React Query persistence plugins
```

#### 4. Real-time con WebSockets

**Prompt**:
```
Convierte la app en real-time colaborativa:
- Backend con WebSockets (FastAPI + WebSockets)
- Frontend escucha cambios de otros usuarios
- Invalidar cache cuando llega update externo
- Notificaciones "Usuario X creó una tarea"
- Evitar conflictos de edición simultánea
```

#### 5. Migracion a Zustand + React Query

**Prompt**:
```
Migra state management a Zustand:
- Store de Zustand para filtros, UI state
- React Query para server state
- Separación clara entre client state y server state
- Persistence de filtros con Zustand middleware
- Comparación antes/después
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [React Hook Form Docs](https://react-hook-form.com/) - API completa y ejemplos
- [Zod Docs](https://zod.dev/) - Schemas y validaciones
- [TanStack Query (React Query)](https://tanstack.com/query/latest) - Guías y ejemplos
- [React Query Comparison](https://tanstack.com/query/latest/docs/react/comparison) - vs SWR, RTK Query

### Tutoriales Recomendados

- **TkDodo's Blog on React Query** - Serie completa sobre React Query
- **React Hook Form + Zod Tutorial** - Video paso a paso
- **Optimistic Updates Explained** - Visualización interactiva

### Herramientas de Desarrollo

- **React Query Devtools** - Inspector de cache y queries
- **React Hook Form Devtools** - Debug de formularios
- **Zod Error Map** - Mensajes de error personalizados

---

## 🎓 Aprendizajes Clave de esta Clase

1. ✅ **React Hook Form + Zod**: Validación declarativa y type-safe
2. ✅ **React Query**: Data fetching moderno con cache inteligente
3. ✅ **Optimistic Updates**: UX instantánea con rollback automático
4. ✅ **Loading States**: Granulares por operación, no globales
5. ✅ **Error Handling**: Robusto con retry y mensajes amigables
6. ✅ **CRUD Completo**: Create, Read, Update, Delete con best practices
7. ✅ **IA como Co-Piloto**: Acelerar desarrollo con prompts efectivos

---

## 🤖 Conclusión: Nivel Profesional con IA

Esta clase demuestra:

- **React Hook Form + Zod** elimina boilerplate de formularios
- **React Query** simplifica data fetching de forma dramática
- **Optimistic Updates** crean UX fluida sin complejidad
- **IA** acelera implementación de patterns complejos
- **Agentes educacionales** enseñan mejores prácticas en contexto

### ¿Qué sigue?

**Módulo 5, Clase 3**: State Management global (Zustand), autenticación JWT, y orquestación de múltiples agentes IA especializados.

---

## 📊 Comparación de Código: Clase 1 vs Clase 2

### Formulario de Creación

**Clase 1** (11 líneas de lógica):
```tsx
const [nombre, setNombre] = useState('');
const [error, setError] = useState('');

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!nombre.trim()) {
    setError('Nombre requerido');
    return;
  }
  // crear tarea...
};
```

**Clase 2** (5 líneas de lógica):
```tsx
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(tareaSchema),
});

const onSubmit = async (data) => await crearTarea.mutateAsync(data);
```

### Data Fetching

**Clase 1** (20+ líneas):
```tsx
const [tareas, setTareas] = useState<Tarea[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<Error | null>(null);

useEffect(() => {
  const cargarTareas = async () => {
    try {
      setLoading(true);
      const data = await tareasService.listar();
      setTareas(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };
  cargarTareas();
}, []);
```

**Clase 2** (3 líneas):
```tsx
const { data: tareas, isLoading, isError } = useQuery({
  queryKey: ['tareas'],
  queryFn: tareasService.listar,
});
```

**Reducción de código**: ~70% menos líneas con más funcionalidad (cache, retry, revalidación).

---

**¿Tienes dudas?** Usa los agentes educacionales o pregunta directamente:

```
Explica [concepto] de Clase 2 usando analogías y ejemplos de código.
```

## 🧠 Glosario – Clase 2: Seguridad básica en tu API

### 🔐 `.env`

Archivo donde se guardan variables sensibles fuera del código.

Ejemplo: claves API, configuración del entorno, rutas secretas.

🔸 **Por qué es útil:** no subes secretos a GitHub y puedes cambiar valores sin tocar el código.

---

### 📦 `python-dotenv`

Librería que carga automáticamente las variables definidas en `.env`.

```python
from dotenv import load_dotenv
load_dotenv()

```

🔸 Te permite usar `os.getenv("API_KEY")` como si fuera una constante definida en tu código.

---

### 🧪 `x-api-key`

Cabecera HTTP (header) estándar personalizada para autenticación básica.

Va en cada petición protegida, por ejemplo:

```bash
curl -H "x-api-key: miclave123" http://localhost:8000/tareas

```

🔸 Si no la mandas o es incorrecta, el servidor te lanza un `401 Unauthorized`.

---

### 🧱 `verificar_api_key()`

Función que **valida la clave de acceso** antes de ejecutar el endpoint.

Debe estar en su propio archivo (ej. `api/dependencias.py`) para respetar SRP.

Devuelve error 401 si la clave no es válida.

🔸 Esta función se inyecta como dependencia en los endpoints con `Depends(...)`.

---

### 📌 `Depends()`

Mecanismo de FastAPI para declarar **dependencias inyectadas**.

Sirve para:

- Validar permisos (`Depends(verificar_api_key)`).
- Cargar usuarios.
- Inyectar servicios configurados, etc.

🔸 Es el equivalente a "pasa por este filtro antes de ejecutar la función".

---

### 🔒 `Field(...)`, `constr(...)`, `pattern=...`

Decoradores de Pydantic que **validan los datos de entrada** automáticamente.

```python
class CrearTareaRequest(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    prioridad: str = Field("media", pattern="^(alta|media|baja)$")

```

🔸 Así tu API rechaza tareas con nombre vacío o prioridades inventadas antes de que entren al sistema.

---

### 🧠 SRP – *Single Responsibility Principle*

**Un archivo o función debe tener un solo motivo para cambiar**.

En esta clase lo aplicamos así:

- `api/api.py`: solo define endpoints.
- `api/dependencias.py`: valida seguridad.
- `servicio_tareas.py`: maneja la lógica de negocio (crear/listar tareas).

---

### 🔌 Inversión de dependencias (adelanto)

Aunque no lo tocamos aún, la **inyección de `verificar_api_key()`** es un mini ejemplo de **Dependency Injection**:

Tu función no pregunta directamente “¿es segura esta petición?”; eso lo delega a una dependencia externa.

---

### ✅ `@app.get(..., dependencies=[...])`

FastAPI te permite aplicar validaciones **sin modificar el cuerpo de la función**.

Ideal para filtros globales o repetitivos como la clave API.

---

### 🧪 Adaptación de tests

Cuando proteges rutas, tus tests deben **añadir la cabecera `x-api-key`**.

Si no, fallarán con error 401.

La clave se puede inyectar desde `.env` o fijar en los tests directamente.

---

### 🤖 Rol de la IA en esta clase

La IA actúa como **auditor y copiloto**:

- Puede generar la función de validación y darte sugerencias de validación con Pydantic.
- Puedes usarla para revisar tu código con prompts del tipo:

```
Rol: Revisor de seguridad API.
Contexto: Tengo una FastAPI con autenticación por API key.
Objetivo: Revisa si tengo fugas de seguridad, errores en la validación o dependencias mal inyectadas.

```

---

## 🧭 Mini resumen mental

| Capa | Responsabilidad | Archivo |
| --- | --- | --- |
| API | Orquestar rutas | `api/api.py` |
| Seguridad | Validar credenciales | `api/dependencias.py` |
| Entorno | Configuración sensible | `.env` |
| Lógica | Crear / listar tareas | `servicio_tareas.py` |
| Tests | Verificar que todo funciona | `tests/` |
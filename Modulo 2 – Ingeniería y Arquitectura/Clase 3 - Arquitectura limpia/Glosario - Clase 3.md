### Arquitectura limpia

Forma de organizar el código para que las **dependencias fluyan hacia dentro**:

- La capa externa (API, CLI, interfaz) conoce a la capa interna (servicio).
- La interna no sabe nada de la externa.
    
    Así puedes cambiar la interfaz sin tocar la lógica ni los tests.
    

---

### Capa API (presentación)

Donde “entra el mundo exterior”: recibe peticiones HTTP, valida datos y devuelve respuestas.

- No contiene reglas de negocio.
- Solo **orquesta** llamadas al servicio.
- En FastAPI, está compuesta por los endpoints y los modelos de entrada/salida (Pydantic).

**Ejemplo:**

```python
@app.post("/tareas")
def crear_tarea(cuerpo: CrearTareaRequest):
    return servicio.crear(cuerpo.nombre).model_dump()

```

---

### Capa de servicio (lógica de negocio)

Encapsula las **reglas del dominio**: cómo se crean, modifican o consultan las tareas.

- No sabe de HTTP, ni de JSON, ni de bases de datos.
- Se prueba fácilmente con tests unitarios.

**Ejemplo:**

```python
def crear(self, nombre: str) -> Tarea:
    self._contador += 1
    tarea = Tarea(id=self._contador, nombre=nombre)
    self._tareas.append(tarea)
    return tarea

```

---

### Repositorio (persistencia)

Capa responsable de **guardar y recuperar datos**.

Por ahora usamos un repositorio en memoria (`self._tareas`), pero más adelante lo sustituiremos por uno que lea y escriba en JSON o en una base de datos.

---

### Pydantic

Librería usada por FastAPI para **definir modelos de datos tipados y validados**.

- `BaseModel` declara campos y tipos.
- `.model_dump()` convierte el modelo a `dict` listo para serializar a JSON.

---

### SRP – *Single Responsibility Principle*

Primer principio de SOLID: cada clase o función debe tener **un único motivo para cambiar**.

Aquí lo aplicamos así:

- La API cambia si cambian los endpoints o las validaciones.
- El servicio cambia si cambian las reglas de negocio.
- El repositorio cambia si cambia el modo de persistencia.

---

### Dependency Inversion (adelanto)

En lugar de que el servicio **dependa de una implementación concreta** (por ejemplo, “repositorio en memoria”), dependerá de **una interfaz abstracta**.

Eso permite intercambiar repositorios sin romper el servicio ni los tests.

---

### Model Dump

Método de Pydantic v2 que devuelve los datos del modelo como `dict`.

Sustituye al antiguo `.dict()` de Pydantic v1.

---

### Flujo típico de una petición

1. **Cliente** envía POST `/tareas`.
2. **API** valida con `CrearTareaRequest`.
3. **Servicio** crea la tarea.
4. **Repositorio** la guarda (en memoria o JSON).
5. **API** devuelve el `dict` serializado como JSON.

---

### Tests verdes

Cuando refactorizas separando capas pero los tests siguen pasando, significa que:

- No rompiste el **contrato externo** (mismo comportamiento).
- Solo cambió la **estructura interna** (mejor arquitectura).

---

### Metáfora de la clase

- **API = mostrador del taller.**
- **Servicio = mecánico.**
- **Repositorio = almacén de piezas.**
    
    Cada uno tiene su trabajo. Si cambias el almacén, el mecánico y el mostrador siguen funcionando igual.
    

---

### Aprendizaje emocional

Pasar de “hacer que funcione” a “hacer que crezca sin romperse”.

Entender el código no como un bloque, sino como **una conversación entre capas**.
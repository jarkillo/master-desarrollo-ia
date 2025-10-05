# 🎬 Clase 5 - **Integración y pruebas de arquitectura**.

Entramos en **la Clase 5 del Módulo 2**, justo donde todo empieza a sentirse como un proyecto “de verdad”.

Para situarnos:

- En la **Clase 1**, aprendiste cómo planificar el trabajo (backlog, historias, sprints).
- En la **Clase 2**, aplicaste **TDD y SRP** en tu primer endpoint con FastAPI.
- En la **Clase 3**, separaste **API / servicio / repositorio** y diste forma a tu primera arquitectura limpia.
- En la **Clase 4**, aplicaste **Open/Closed y Dependency Inversion**: tu servicio ya no depende de detalles, sino de contratos.

Ahora llega **la Clase 5 – Integración y pruebas de arquitectura**.

El objetivo: **ver si toda esta estructura realmente se comporta como esperábamos**.

Aquí empieza el oficio de **ingeniero**, no solo programador.

Antes de empezar a meter más contigo, PARATE UN SEGUNDO

Ahora mismo deberias tener un mapa mental de que hace cada archivo del proyecto, cada linea. Esto no significa que seas capaz de escribirla en un papel en blanco. Esto significa que si lees el codigo entiendes lo que esta ocurriendo.

Si esto no es así, no avances mas porque se te va a empezar a hacer bola (si no se te ha hecho ya)

Abre tu IA de confianza (Ej. ChatGPT 5) y pasale el codigo que hicimos en la clase 1 y que te lo explique linea a linea. Preguntale todas las dudas que tengas y no avances hasta tenerlo claro.

Lo mismo con las clases 2, 3, 4. El objetivo es que antes de continuar entiendas todo y tengas el mapa mental. (*Tomate esto como una tutoria con el profesor, solo que este no se frustra al explicarte las cosas 1000 veces*)

Ahora si. Continuamos

## 🎯 Concepto

Hasta ahora escribías tests de comportamiento (que el endpoint devuelva 201, que las tareas se guarden…).

Pero ¿qué pasa si alguien cambia una parte interna —por ejemplo, sustituye el repositorio en memoria por uno JSON— y la API sigue respondiendo igual?

Esa es la prueba de fuego de la **arquitectura limpia**:

> “Cambiar dentro sin romper fuera.”
> 

Hoy aprenderás a escribir **tests de integración** que crucen capas:

API → Servicio → Repositorio.

Así comprobamos que los contratos entre capas están bien definidos y que tu sistema es **coherente y extensible**.

---

## 🧠 Historia para entenderlo

Imagina que eres el jefe técnico y tienes dos devs:

- Ana ha implementado `RepositorioMemoria`.
- Luis crea `RepositorioJSON`.

Ambos prometen que sus clases cumplen el mismo contrato (`guardar()` y `listar()`), pero ¿cómo lo verificas sin abrir el código?

Con un **test de integración**, que trate ambos repositorios como cajas negras.

Si ambos pasan los mismos tests, tu arquitectura está viva y saludable.

---

Pero antes, vamos a crear **`RepositorioJSON`**

Vamos a hacerlo juntos, sin prisas y sin romper nada.

### 1) ¿Qué necesitamos que haga?

Igual que `RepositorioMemoria`, debe cumplir el **contrato** (`guardar`, `listar`). Solo que, en vez de una lista en RAM, **lee/escribe un archivo `.json`**.

### 2) Crea el archivo

Ruta sugerida: `api/repositorio_json.py`

```python
# api/repositorio_json.py
from __future__ import annotations
import json, os
from typing import List
from api.servicio_tareas import Tarea  # usamos el mismo modelo Pydantic

class RepositorioJSON:
    """Repositorio que persiste tareas en un archivo JSON sencillo."""

    def __init__(self, ruta_archivo: str = "tareas.json"):
        self._ruta = ruta_archivo
        # si no existe, lo creamos vacío
        if not os.path.exists(self._ruta):
            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def listar(self) -> List[Tarea]:
        with open(self._ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            datos = json.loads(contenido) if contenido else []
        # devolvemos objetos Tarea (Pydantic), no dicts
        return [Tarea(**d) for d in datos]

    def guardar(self, tarea: Tarea) -> None:
        # leemos lo existente
        tareas = self.listar()
        # generamos ID robusto (max + 1)
        nuevo_id = (max((t.id for t in tareas), default=0) + 1)
        tarea.id = nuevo_id
        tareas.append(tarea)
        # guardamos todo
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump([t.model_dump() for t in tareas], f, ensure_ascii=False, indent=2)

```

Puntos clave, en cristiano:

- Si el archivo **no existe**, lo creamos con `[]`.
- `listar()` **lee el JSON** y convierte cada item a `Tarea`.
- `guardar()` **calcula el siguiente id** (`max + 1`), asigna y **reescribe** el archivo completo (simple y suficiente ahora).

### 3) Usarlo en la API

En `api/api.py`, donde eliges repositorio:

```python
from api.repositorio_memoria import RepositorioMemoria
from api.repositorio_json import RepositorioJSON

# repositorio = RepositorioMemoria()
repositorio = RepositorioJSON("data/tareas.json")  # por ejemplo, dentro de /data
servicio = ServicioTareas(repositorio)
```

No cambias nada más. Esa es la gracia de DIP: **una línea y listo**.

Simplemente cambiamos el repo que le damos al servicio y BOOM, ya lo tenemos funcionando en JSON sin escribir nada mas. Y los test pasando en verde.

### 5) Eliminar estado compartido

Vamos a modificar el test crear_tarea por:

```python
from fastapi.testclient import TestClient
from api import api as api_mod  # accedemos al módulo, no solo al app
from api.servicio_tareas import ServicioTareas
from api.repositorio_memoria import RepositorioMemoria

def test_crear_tarea_minima_devuelve_201_y_cuerpo_esperado():
    # 1. Resetear el servicio a uno limpio
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    # 2. Crear el cliente justo después
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre = cliente.post("/tareas", json={"nombre": "Estudiar SOLID"})
    assert respuesta_con_nombre.status_code == 201
    cuerpo = respuesta_con_nombre.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Estudiar SOLID"
    assert cuerpo["completada"] is False

def test_crear_tarea_con_nombre_vacio_devuelve_422():
    api_mod.servicio = ServicioTareas(RepositorioMemoria())
    cliente = TestClient(api_mod.app)

    respuesta_con_nombre_vacio = cliente.post("/tareas", json={"nombre": ""})
    assert respuesta_con_nombre_vacio.status_code == 422

```

## 🧠 Traducción para humanos

- Ya **no hay `cliente_http` global** que se quede con el repo sucio.
- Cada test **crea un cliente después de inyectar un repo limpio**.
- El `id` siempre arranca en 1. La API es predecible.

### 5) Test rápido de integración (para dormir tranquilo)

Crea (o añade) un test muy pequeño que pruebe memoria y json igual:

```python
# tests/test_crear_tarea_json.py
import tempfile, os
from fastapi.testclient import TestClient
from api import api as api_mod
from api.servicio_tareas import ServicioTareas
from api.repositorio_json import RepositorioJSON

def test_crear_tarea_con_repositorio_json_temporal():
    # Crear archivo temporal vacío
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()

    try:
        # Inyectar el servicio con RepositorioJSON usando el archivo temporal
        api_mod.servicio = ServicioTareas(RepositorioJSON(tmp.name))

        # Lanzar cliente HTTP contra la API
        cliente = TestClient(api_mod.app)
        r = cliente.post("/tareas", json={"nombre": "Aprender tests con IA"})

        # Verificar respuesta
        assert r.status_code == 201
        tarea = r.json()
        assert tarea["id"] == 1
        assert tarea["nombre"] == "Aprender tests con IA"
        assert tarea["completada"] is False

    finally:
        # Borrar archivo después del test
        os.remove(tmp.name)

```

Si esto pasa en verde, estás listo: **misma historia, distinto almacén**.

Fijate bien en una cosa, porque es un error muy tipico:

- Ahora estamos creando un archivo temporal para el test y eliminandolo al terminar. Hay que tener cuidado de no escribir el json real en los test, y la IA mete mucho la gamba en esto.

---

## 🤖 Aplicación con IA

Prompt ejemplo:

```
Rol: QA Engineer Python.

Contexto: Tengo una API con ServicioTareas y varios repositorios (memoria, JSON).
Objetivo: Genera tests de integración que verifiquen que todas las implementaciones del repositorio cumplen el mismo contrato.

Formato: Código pytest limpio y explicaciones breves.

Restricciones: No modificar el código de producción.
```

La IA puede proponerte una **prueba parametrizada** con `pytest.mark.parametrize`, o incluso generar fixtures automáticas.

Pero el punto es que tú entiendas *qué está comprobando*: consistencia de comportamiento entre implementaciones.

Es importante que compruebes el flujo que está siguiendo la IA, te irás dando cuenta de los típicos errores que comete y estarás preparado para evitarlos.

---

## 🧩 Ejercicio práctico

1. Rama: `feature/test-integracion-repositorios`.
2. Añade los tests genéricos como el ejemplo.
3. Corre toda la suite (`pytest -v`).
4. Documenta en `notes.md`:
    - Qué descubriste sobre tu arquitectura.
    - Qué rompería si cambiaras el contrato del repositorio.
    - Qué significa “extensible pero estable” en tu código.

---

## ✅ Checklist final

- [ ]  Entiendes la diferencia entre test unitario e integración.
- [ ]  Has comprobado que distintos repositorios se comportan igual.
- [ ]  Tu arquitectura puede cambiar internamente sin romper los contratos.
- [ ]  Has documentado la reflexión en `notes.md`.

---

En la próxima clase daremos un paso más: añadiremos **repositorios externos y adaptadores (JSON/DB)** y hablaremos de cómo preparar tu proyecto para **tests de aceptación y CI/CD**.
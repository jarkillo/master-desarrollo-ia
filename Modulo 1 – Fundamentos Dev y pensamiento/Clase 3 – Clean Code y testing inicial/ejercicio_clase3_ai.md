# Ejercicio Clase 3: Testing con IA

## 🎯 Objetivo

Alcanzar 80%+ coverage en tu CLI de tareas usando el **Test Coverage Strategist agent** para identificar edge cases y gaps de cobertura.

---

## 📋 Pre-requisitos

Antes de empezar:

1. **Código funcional**: Tienes `tareas.py` con funciones:
   - `cargar_tareas(ruta)`
   - `guardar_tareas(ruta, tareas)`
   - `agregar_tarea(ruta, nombre)`
   - `completar_tarea(ruta, id)`
   - `listar_tareas(ruta)`

2. **pytest instalado**:
   ```bash
   pip install pytest pytest-cov
   ```

3. **Tests básicos**: Has escrito al menos `test_agregar_tarea` manualmente

---

## 🚀 Tareas

### Tarea 1: Escribir test happy path (Manual - 15 min)

**Objetivo**: Interiorizar la estructura de un test pytest.

**Instrucciones**:

1. Abre `test_tareas_pytest.py`
2. Escribe MANUALMENTE el test `test_agregar_tarea` (sin copiar del README):

```python
def test_agregar_tarea(archivo_temporal):
    # Arrange: prepara el contexto (fixture ya lo hace)

    # Act: ejecuta la función a testear
    agregar_tarea(archivo_temporal, "Estudiar IA")

    # Assert: verifica el resultado
    tareas = cargar_tareas(archivo_temporal)
    assert len(tareas) == 1
    assert tareas[0]["nombre"] == "Estudiar IA"
```

3. Ejecuta el test:
   ```bash
   pytest test_tareas_pytest.py::test_agregar_tarea -v
   ```

**Validación**: Test pasa ✅

---

### Tarea 2: Pedir lista de edge cases a IA (Con IA - 10 min)

**Objetivo**: Aprender a usar el Test Coverage Strategist para descubrir casos que no habías pensado.

**Prompt para Claude Code**:

```
Rol: Test Coverage Strategist
Contexto: Tengo una función agregar_tarea(ruta, nombre) que guarda tareas en JSON.

Código:
[pega la función agregar_tarea de tareas.py]

Objetivo: Lista de edge cases que debería testear (NO generes el código aún).
Categoriza por criticidad (Alta/Media/Baja).
```

**Resultado esperado de la IA**:

```markdown
## Edge Cases para agregar_tarea

### Criticidad ALTA:
1. Nombre vacío ("") - debe rechazar o usar default
2. Nombre con solo espacios ("   ") - debe validar
3. Archivo JSON corrupto - debe manejar error

### Criticidad MEDIA:
4. Nombre muy largo (1000+ caracteres) - puede causar problemas
5. Caracteres especiales en nombre (\n, \t, emojis)

### Criticidad BAJA:
6. Agregar múltiples tareas muy rápido (concurrencia)
```

**Acción TU**:

1. Lee la lista que te dio la IA
2. Anota en tu `notes.md`:
   - ¿Qué casos SÍ habías pensado?
   - ¿Qué casos NO se te habían ocurrido?
   - ¿Cuáles crees que son realmente importantes?

---

### Tarea 3: Implementar edge cases de criticidad ALTA (Manual - 20 min)

**Objetivo**: Escribir TÚ MISMO los tests críticos para interiorizar el patrón.

**Instrucciones**:

Escribe tests para los 2-3 edge cases de criticidad ALTA:

```python
def test_agregar_tarea_nombre_vacio(archivo_temporal):
    """
    Edge case: Nombre vacío debe ser rechazado o usar default.
    """
    # ¿Qué debería pasar?
    # Opción A: Lanzar error
    # Opción B: Usar nombre default "Sin título"

    # Decide TÚ qué comportamiento quieres y escribe el test
    ...


def test_agregar_tarea_json_corrupto(archivo_temporal):
    """
    Edge case: Si el JSON está corrupto, no debe crashear.
    """
    # Escribe JSON inválido en el archivo
    with open(archivo_temporal, 'w') as f:
        f.write("{esto no es json válido")

    # Intenta agregar tarea
    # ¿Debería funcionar? ¿Lanzar error controlado?
    ...
```

**⚠️ IMPORTANTE**:
- NO copies el código completo del README
- Escribe línea por línea, pensando qué hace cada assert
- Si te atascas, pide ayuda a la IA para UN test específico

---

### Tarea 4: Pedir ayuda para UN edge case complejo (Con IA - 10 min)

**Objetivo**: Aprender a pedir ayuda específica a la IA para casos difíciles.

**Escenario**: El edge case de "JSON corrupto" es complejo de testear.

**Prompt efectivo**:

```
Ayúdame a escribir el test para este caso específico:

Edge case: Intentar agregar tarea cuando el archivo JSON está corrupto.

Comportamiento esperado: La función cargar_tareas debe devolver lista vacía (no crashear).

Código actual de cargar_tareas:
[pega la función]

Dame el código pytest para este test, explicando cada parte.
```

**Acción TÚ**:

1. Lee el código generado línea por línea
2. Entiende QUÉ hace cada parte
3. Modifícalo si es necesario para que se ajuste a tu código
4. Ejecuta el test y verifica que pasa

---

### Tarea 5: Validar coverage (Verificación - 10 min)

**Objetivo**: Medir cuánto coverage has alcanzado.

**Comando**:

```bash
pytest --cov=. --cov-report=term-missing
```

**Resultado esperado**:

```
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
tareas.py        42      8    81%   23-25, 67, 89-91
test_tareas_pytest.py    28      0   100%
-------------------------------------------
TOTAL            70      8    89%
```

**Preguntas para reflexionar** (anota en `notes.md`):

1. ¿Llegaste a 80%+?
2. Si NO: ¿Qué líneas/funciones faltan? (mira columna "Missing")
3. ¿Son críticas esas líneas o son casos raros?
4. ¿Vale la pena testear el 10% restante?

---

## 📝 Entregable

Al final de este ejercicio, debes tener:

### Archivos

1. **test_tareas_pytest.py** con 5+ tests:
   - Al menos 2 escritos 100% manualmente
   - Al menos 1 con ayuda de IA (documentado)

2. **notes.md** con reflexiones:
   ```markdown
   # Clase 3 - Testing con IA

   ## Edge cases descubiertos con IA
   - [Lista de casos que la IA te sugirió y no habías pensado]

   ## Tests escritos
   - `test_agregar_tarea`: Manual ✅
   - `test_nombre_vacio`: Manual (con sugerencia de IA para assert)
   - `test_json_corrupto`: Con ayuda de IA (entendí cada línea)

   ## Coverage alcanzado
   - X% (objetivo 80%+)

   ## Aprendizajes
   - [Qué aprendiste sobre testing con pytest]
   - [Qué aprendiste sobre usar IA como asistente (no como copiador)]
   ```

### Validación

```bash
# Todos los tests pasan
pytest test_tareas_pytest.py -v

# Coverage 80%+
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

---

## ✅ Criterios de Éxito

Has completado el ejercicio si:

- [ ] Escribiste al menos 2 tests 100% manual (sin copiar)
- [ ] Usaste IA para descubrir edge cases (lista de casos)
- [ ] Implementaste al menos 1 test con ayuda de IA (entendiendo cada línea)
- [ ] Alcanzaste 80%+ coverage
- [ ] Documentaste en notes.md qué aprendiste

---

## 🚫 Antipatrones a Evitar

❌ **NO HAGAS ESTO**:
- Copiar todos los tests del README sin entenderlos
- Pedir a la IA "genera todos los tests" y copiar sin leer
- Alcanzar 80% sin saber qué estás testeando

✅ **HAZ ESTO**:
- Escribe tests manualmente para interiorizar
- Usa IA para DESCUBRIR casos, no para copiar código
- Entiende cada assert que escribes
- Documenta qué aprendiste

---

## 🎓 Siguientes Pasos

Cuando completes este ejercicio, estarás listo para:

- **Clase 4**: Testing ampliado (90%+ coverage, parametrización)
- **TDD con IA**: Escribir tests ANTES de implementar funciones
- **Refactoring seguro**: Cambiar código sabiendo que tests te protegen

---

**Recuerda**: El objetivo no es alcanzar un número, es **entender qué estás testeando y por qué**.

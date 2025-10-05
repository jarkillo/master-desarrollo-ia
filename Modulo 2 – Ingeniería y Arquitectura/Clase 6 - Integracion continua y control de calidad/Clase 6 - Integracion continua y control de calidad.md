# 🧠 Clase 6 - Integración continua y control de calidad arquitectónica

*(Módulo 2 – Ingeniería y Arquitectura)*

## 🧠 Antes de empezar

Hasta ahora has construido una API que no solo funciona, sino que **se sostiene con dignidad**:

- Tiene capas separadas (API, servicio, repositorio).
- Los tests cubren sus funcionalidades básicas.
- Puedes cambiar de memoria a JSON sin romper nada.

Pero te falta lo más importante si quieres que este proyecto crezca:

> Que nadie (ni tú mismo en 3 semanas) pueda romperlo sin enterarse.
> 

Aquí entra en juego la **Integración Continua (CI)**:

Un sistema que lanza los tests automáticamente **cada vez que haces push o abres un PR**.

Si todo va bien → ✅

Si algo se rompe → ❌ GitHub te lo canta sin que nadie lo tenga que revisar a mano.

---

## 🎯 ¿Qué vamos a montar hoy?

Una mini-fábrica que se encargue de:

1. Ejecutar los tests automáticamente.
2. Avisarte si algo falla.
3. (Más adelante) Medir cobertura, pasar linters, y desplegar.

No más “¡en mi máquina funciona!” ni “se me olvidó correr los tests”.

---

## 🧪 Paso a paso (a mano)

### 1. Crea la carpeta donde viven los workflows de GitHub:

```bash
mkdir -p .github/workflows

```
Importante, esto es en la raiz de tu proyecto

Y… ¿recuerdas que en la clase 2 generamos un requirements.txt? metelo tambien en la raiz

### 2. Dentro, crea el archivo `ci.yml`:

```yaml
name: CI - Tests automáticos

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Clonar el repo
        uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Ejecutar tests
        run: pytest -v

```

Guarda, haz commit, empuja la rama y abre PR.

GitHub va a lanzar automáticamente el workflow y te dirá si todo está OK o si se ha roto algo.

---

## 🤖 ¿Y cómo entra la IA?

Ahora que tú sabes lo que hace este `.yml`, puedes pedírselo a la IA de forma estructurada.

Prompt ejemplo:

```
Rol: DevOps Python.
Contexto: Tengo un proyecto FastAPI con tests en pytest.
Objetivo: Crea un pipeline de GitHub Actions que:
- Ejecute los tests.
- Calcule cobertura con pytest-cov.
- No permita merge si falla.
- Use Python 3.12.

Formato: YAML limpio y comentado.

```

Así te devuelve una versión más pro con cobertura, artefactos, etc.

Pero ya sabes leerla y adaptarla. No te fías a ciegas.

---

## 🧭 ¿Por qué esto importa?

Hasta hoy, **tú ejecutabas los tests**.

A partir de ahora, **los tests se ejecutan solos**. Siempre.

Eso es ingeniería de verdad. No confiar en la memoria, sino en procesos automáticos.

> Si alguien cambia RepositorioTareas y se carga el contrato, el PR no pasa.
> 
> 
> Si alguien olvida un test, la cobertura lo avisa.
> 
> Si alguien comete una burrada, la máquina lo frena.
> 

---

## 🛠️ Mini-ejercicio práctico

1. Crea la rama `feature/ci`.
2. Añade `.github/workflows/ci.yml`.
3. Haz push y abre PR.
4. Comprueba que GitHub lanza el workflow y los tests pasan.
5. Escribe en `notes.md`:
    - Qué hace el pipeline.
    - Qué protegerá en el futuro.
    - Qué te gustaría automatizar más adelante.

---

## ✅ Checklist de la clase

- [x]  Entiendes qué es CI y para qué sirve.
- [x]  Has creado un pipeline funcional con GitHub Actions.
- [x]  Tu repo ahora lanza los tests automáticamente al hacer push o PR.
- [x]  Has documentado lo que aprendiste en `notes.md`.

---

## 🌱 Qué sigue

En el próximo módulo, entramos de lleno en **Calidad y Seguridad**:

- Vamos a añadir seguridad real (validación, JWT, .env…).
- Fortalecer la cobertura de tests.
- Auditar con IA.
- Preparar el despliegue real.

Porque una API que no se rompe es genial.

Pero una API que **no te hackean** y **se despliega sola**... eso ya es otro nivel.

---

¿Listo para que tu código empiece a vivir solo?

Haz el PR de esta clase y pasamos al siguiente bloque.

## Posibles errores

En nuestro caso, como estamos dividiendo cada clase en carpetas diferentes, nuestro CI daba problemas. Asi que directamente hemos modificado nuestro CI para que haga los test por carpeta de forma independiente.

En nuestro caso, en la clase 1 solo esta hecho lo que explicamos en esa clase, para que podais ir viendo como va cambiando el archivo y los test a medida que avanzamos. Esto me provocaba un problema de carpetas.

Si en tu caso estas copiando el repo tal cual, pon el ci asi:

```sql
name: CI - Tests por clase

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        class_dir:
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 2 - Principios SOLID y paradigmas de programacion"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 3 - Arquitectura limpia"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 4 - Open_Closed y Dependency Inversion"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 5 - Integracion y pruebas de arquitectura"
          - "Modulo 2 – Ingeniería y Arquitectura/Clase 6 - Integracion continua y control de calidad"

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Pytest (tests)
        working-directory: ${{ matrix.class_dir }}
        run: |
          # Opcional: limpiar cachés por si vinieran del repo
          find . -type d -name "__pycache__" -exec rm -rf {} +
          find . -type f -name "*.pyc" -delete
          pytest -q

```

Si no es tu caso, deberian pasar los test como ya lo habiamos explicado.

Haz el PR de esta clase y pasamos al siguiente bloque.


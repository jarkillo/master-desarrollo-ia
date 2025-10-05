# 📘 Glosario – Clase 3: Auditoría continua y defensa inteligente

# 🧩 Auditoría de seguridad

Proceso de análisis del código fuente para detectar **vulnerabilidades, malas prácticas o patrones de riesgo** antes de que lleguen a producción.

En esta clase se automatiza usando **Bandit**, integrado en el pipeline CI.

---

### 🧠 Bandit

Herramienta de análisis estático desarrollada por la comunidad OpenStack.

Lee tu código Python y busca errores comunes de seguridad como:

- Contraseñas o claves escritas en texto plano.
- Uso inseguro de `os.system()` o `eval()`.
- Archivos o sockets abiertos sin cierre seguro.

Ejemplo de uso manual:

```bash
bandit -r api/

```

---

### ⚙️ Análisis estático

Tipo de auditoría que **no ejecuta el código**, sino que lo inspecciona leyendo los archivos fuente.

Busca patrones sospechosos (por sintaxis, imports o funciones conocidas).

Complementa a los tests, que son análisis **dinámico** (el código se ejecuta y se observa su comportamiento).

---

### 🚦 Severidad

Clasificación del impacto potencial de un problema detectado.

Los niveles más comunes son:

- **Low:** detalles menores o recomendaciones.
- **Medium:** potenciales vulnerabilidades con bajo riesgo.
- **High:** fallos críticos que pueden comprometer el sistema.

---

### 📊 Confianza

Indica la certeza que tiene la herramienta de que el hallazgo es realmente un problema:

- **Low:** podría ser un falso positivo.
- **Medium:** probable riesgo real.
- **High:** muy probable que sea un fallo genuino.

Bandit muestra ambos valores (severidad y confianza) en cada informe.

---

### 🧰 CI/CD de calidad

Extensión del pipeline de Integración Continua donde no solo se ejecutan tests, sino también **auditorías y linters**.

El objetivo es que **GitHub rechace automáticamente** un PR si contiene vulnerabilidades o código inseguro.

---

### 🤖 Auditoría con IA

Uso de modelos como ChatGPT o agentes automáticos para generar **informes de calidad y seguridad**.

El objetivo no es reemplazar al auditor humano, sino tener una capa adicional que:

- Señale riesgos lógicos o de diseño que Bandit no detecta.
- Proponga refactorizaciones.
- Cree documentación o issues automáticamente.

---

### 🛡️ Defensa inteligente

Filosofía de diseño donde el código no solo **funciona**, sino que **se protege**:

- Tests automáticos → evitan romper lo que ya existía.
- CI/CD → evita merges sin control.
- Auditoría estática → busca patrones de riesgo.
- IA → revisa la estructura y legibilidad.

---

### 🧾 Resultado esperado

Al final de esta clase tu repositorio debe:

- Pasar Bandit sin errores.
- Tener un pipeline CI que incluya la auditoría.
- Contar con un informe o `notes.md` con los hallazgos y próximos pasos.
- Entender cómo usar la IA para automatizar la revisión continua.
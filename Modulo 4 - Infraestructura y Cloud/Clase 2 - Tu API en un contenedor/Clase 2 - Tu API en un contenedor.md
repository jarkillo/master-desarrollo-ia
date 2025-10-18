# Clase 2 - Tu API en un contenedor: reproducibilidad sin dolor

## 🎬 El problema

Hasta ahora, tu API vive bien en tu máquina.

Pero cada vez que otro dev intenta ejecutarla, pasa esto:

> “En mi PC sí funciona…”
> 

¿Por qué ocurre?

Porque tu entorno (librerías, versión de Python, variables, sistema operativo) **no es igual al de los demás**, ni al de producción.

Para solucionar eso nació **Docker**: empaquetar tu aplicación con todo lo que necesita para funcionar, igual en cualquier lugar.

---

## 🧠 Concepto

Piensa en Docker como una **caja transparente**: dentro metes tu API, Python, las dependencias, y un pequeño sistema operativo.

Cuando la ejecutas, el mundo exterior solo ve la caja, no lo que hay dentro.

Por eso:

- nadie rompe nada instalando cosas raras,
- los tests se ejecutan siempre igual,
- y desplegar en la nube es tan simple como mover la caja.

## 🧩 Instalación previa: Docker Desktop

Antes de escribir una sola línea, asegúrate de tener Docker instalado.

### Windows / macOS

- Descarga **Docker Desktop**

Sigue el instalador y, cuando termine, abre una terminal y ejecuta:

```bash
docker --version
```

Deberías ver algo como:

```
Docker version 27.1.1, build abc123
```

Si no, reinicia el sistema o abre Docker Desktop manualmente.

### Linux (O si tienes un servidor VPS con Linux)

Instala con tu gestor de paquetes (por ejemplo, en Ubuntu):

```bash
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

```

Y prueba también con `docker --version`.

⚠️ Si te da un error tipo “permission denied”, ejecuta:

```bash
sudo usermod -aG docker $USER
```

y reinicia la sesión.

---

## 🛠️ Aplicación manual

1. Crea un archivo `Dockerfile` en la raíz del proyecto:

```docker
# Imagen base con Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Comando por defecto
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]

```

1. Crea un archivo `.dockerignore` para no copiar cosas innecesarias:

```
__pycache__/
.env
.git
.github/
tests/

```

1. Construye y ejecuta tu contenedor:

```bash
docker build -t api-tareas .
docker run -p 8000:8000 api-tareas

```

Ahora tu API corre igual que en tu máquina, pero **aislada**.

---

## 🤖 Aplicación con IA

Prompt reutilizable:

```
Rol: Ingeniero DevOps con experiencia en FastAPI.
Contexto: API funcional con CI/CD y .env configurado.
Objetivo: Crear un Dockerfile reproducible para entorno dev y despliegue.
Restricciones: no usar Docker Compose todavía. Optimizar tamaño e instalación.

Entrega: Dockerfile y .dockerignore listos para CI.
```

La IA puede:

- optimizar capas del Dockerfile,
- crear imágenes más ligeras con Alpine,
- o añadir versiones separadas para desarrollo y producción.

---

## 🧪 Mini-proyecto de esta clase

1. Rama: `feature/docker-base`
2. Archivos:
    - `Dockerfile` y `.dockerignore` creados.
    - Prueba local: `docker run` funcionando en puerto 8000.
3. Modifica tu CI (`.github/workflows/ci.yml`) para añadir:
    
    ```yaml
    - name: Build Docker image
      run: docker build -t api-tareas .
    
    ```
    
4. En `notes.md`, documenta:
    - Qué aprendiste del contenedor.
    - Qué diferencias viste respecto al entorno local.
    - Qué parte automatizarías con IA.

---

## ✅ Checklist de la Clase 2

- [ ]  Dockerfile funcional y probado.
- [ ]  CI capaz de construir la imagen.
- [ ]  .dockerignore configurado.
- [ ]  Entiendes qué significa “entorno reproducible”.
- [ ]  Tu API corre igual en local y en contenedor.
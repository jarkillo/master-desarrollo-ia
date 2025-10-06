## 📘 Glosario – Clase 2

**Docker:**

Plataforma que permite crear, ejecutar y compartir contenedores. Garantiza que una aplicación se ejecute igual en cualquier entorno.

**Contenedor:**

Un “miniordenador” aislado que contiene todo lo necesario para que tu aplicación funcione: código, librerías y dependencias.

Es como una caja que siempre se comporta igual, sin importar el sistema operativo donde la uses.

**Imagen Docker:**

La “receta” o plantilla para crear contenedores.

Se construye a partir de un archivo `Dockerfile`.

Una vez creada, puedes ejecutar tantos contenedores como quieras desde esa imagen.

**Dockerfile:**

Archivo de texto con las instrucciones que Docker usa para construir una imagen (qué instalar, qué copiar, qué ejecutar).

Es al contenedor lo que `requirements.txt` es al entorno Python.

**.dockerignore:**

Archivo que le dice a Docker qué cosas **no debe copiar** dentro de la imagen (como `.git`, `__pycache__`, `.env`, etc.).

Evita que la imagen sea más pesada o insegura.

**Docker Desktop:**

Aplicación gráfica (para Windows y macOS) que instala y gestiona Docker.

Incluye el motor de contenedores y herramientas para construir y ejecutar imágenes.

**`docker build`:**

Comando que lee el `Dockerfile` y crea una imagen.

**`docker run`:**

Comando que ejecuta un contenedor a partir de una imagen.

**Puerto (ej. `-p 8000:8000`):**

Permite conectar el puerto del contenedor con el del ordenador anfitrión, para poder acceder a la API desde el navegador.

**Reproducibilidad:**

Propiedad que garantiza que el software se comporta igual sin importar dónde o quién lo ejecute.

Docker la logra al aislar el entorno.

**CI/CD:**

Siglas de *Continuous Integration / Continuous Deployment*.

Automatizan los procesos de test y despliegue. En esta clase solo añadimos la parte de “Build Docker image” dentro del CI.
# 🧭 Glosario – Clase 1

**Infraestructura** → todo lo que hace posible que tu aplicación funcione cuando tú no estás mirando: servidores, contenedores, bases de datos, pipelines de despliegue, logs y monitoreo.

**Cloud (Nube)** → servicios de infraestructura remota (servidores, bases de datos, almacenamiento) que alquilas por uso, sin gestionar hardware físico. Ejemplos: AWS, Render, Railway, Vercel, Heroku.

**Servidor** → máquina (física o virtual) que ejecuta tu aplicación y responde a requests HTTP. Puede ser tu laptop, un servidor dedicado, o una máquina virtual en la nube.

**Contenedor** → entorno aislado y portable que empaqueta tu aplicación con todas sus dependencias. Más ligero que una máquina virtual. Docker es la herramienta estándar.

**Docker** → herramienta para crear, ejecutar y gestionar contenedores. Permite empaquetar tu app de forma que funcione igual en tu laptop, en CI y en producción.

**Infraestructura como Código (IaC - Infrastructure as Code)** → práctica de definir infraestructura usando archivos de configuración (código) en lugar de configuración manual. Ejemplos: `Dockerfile`, `docker-compose.yml`, Terraform.

**Terraform** → herramienta de IaC para provisionar infraestructura en la nube (crear servidores, bases de datos, redes) usando código declarativo.

**Pipeline CI/CD** → sistema automatizado que:
- **CI (Continuous Integration)**: ejecuta tests en cada push/PR
- **CD (Continuous Deployment)**: despliega automáticamente a producción si los tests pasan

```yaml
# .github/workflows/ci.yml
- run: pytest
- run: docker build
- run: deploy to Railway  # CD
```

**Deploy (Despliegue)** → proceso de llevar tu código desde tu máquina o GitHub hasta un servidor en producción donde los usuarios pueden acceder.

**Entorno** → configuración específica donde corre tu app. Tipos comunes:
- **Local**: Tu laptop (desarrollo)
- **CI**: GitHub Actions (testing)
- **Staging**: Entorno de pruebas pre-producción
- **Production**: Donde están los usuarios reales

**Variables de entorno** → configuración que cambia según el entorno sin modificar código. Se definen fuera del código (archivo `.env`, GitHub Secrets, panel de Railway).

```python
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
```

**.env** → archivo local (NUNCA en git) que contiene variables de entorno con valores sensibles para desarrollo.

```bash
# .env (NO hacer commit)
DATABASE_URL=postgresql://localhost/dev
JWT_SECRET=secret-local-123
```

**.env.template** → plantilla (SÍ en git) que documenta qué variables necesita tu proyecto, sin incluir valores reales.

```bash
# .env.template (SÍ hacer commit)
DATABASE_URL=your_database_url_here
JWT_SECRET=your_jwt_secret_here
API_KEY=your_api_key_here
```

**Secretos** → información sensible que nunca debe estar en código ni en git: passwords, API keys, JWT secrets, tokens. Se almacenan en:
- Local: archivo `.env`
- CI: GitHub Secrets
- Cloud: Panel de configuración del servicio (Railway, Render)

**check_env.py** → script de validación que verifica que tu archivo `.env` tiene todas las variables definidas en `.env.template`. Previene errores por variables faltantes.

```bash
python infra/check_env.py
# ✅ Variables sincronizadas correctamente
```

**DATABASE_URL** → variable estándar que indica cómo conectarse a la base de datos. Formato: `driver://user:password@host:port/database`

```bash
# SQLite (local)
DATABASE_URL=sqlite:///./tareas.db

# PostgreSQL (producción)
DATABASE_URL=postgresql://user:pass@host/db
```

**Portable** → código que funciona igual en cualquier entorno (local, CI, staging, producción) sin modificaciones. Docker ayuda a lograr esto.

**Escalable** → sistema diseñado para crecer: más usuarios, más requests, más datos, sin reescribir todo. Se logra con arquitectura adecuada (APIs stateless, bases de datos separadas, caching).

**DevOps** → práctica y cultura que une desarrollo (Dev) y operaciones (Ops): automatizar deploys, monitorear apps, gestionar infraestructura como código.

**docker-compose.yml** → archivo que define múltiples contenedores y cómo se conectan. Útil para desarrollo local con múltiples servicios (API + Base de datos + Redis).

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
  db:
    image: postgres:15
```

**Sincronización .env** → asegurar que `.env` y `.env.template` tienen las mismas variables (aunque con valores diferentes). El CI puede validarlo automáticamente.

**Monitoreo y logs** → sistemas que te informan del estado de tu aplicación en producción:
- **Logs**: Registros de eventos (requests, errores, debug)
- **Monitoreo**: Métricas (CPU, memoria, requests/segundo, errores)
- Herramientas: Sentry (errores), CloudWatch (AWS), Railway logs

**Railway** → plataforma cloud que simplifica el despliegue de aplicaciones. Conectas tu repo de GitHub, configuras variables, y despliega automáticamente.

**Render** → plataforma cloud similar a Railway, con plan gratuito. Soporta APIs, bases de datos, workers, cron jobs.

**AWS (Amazon Web Services)** → proveedor cloud más grande. Ofrece cientos de servicios: EC2 (servidores), RDS (bases de datos), S3 (almacenamiento), Lambda (funciones serverless). Más flexible pero más complejo.

**Infraestructura física vs virtual**:
- **Física**: Servidores reales en un datacenter
- **Virtual**: Máquinas virtuales (VMs) o contenedores corriendo en servidores físicos compartidos

**Capas de infraestructura**:
1. **Física/Virtual**: Máquinas reales o cloud
2. **IaC**: Archivos de configuración (Dockerfile, Terraform)
3. **Pipeline CI/CD**: Automatización de tests y deploy
4. **Entorno y configuración**: Variables `.env`, secretos
5. **Monitoreo y logs**: Sentry, CloudWatch, Railway logs

**"Mi máquina funciona" (It works on my machine)** → problema clásico donde el código funciona en desarrollo pero falla en producción por diferencias de entorno. Docker y variables de entorno correctas resuelven esto.

**Carpeta /infra** → convención para agrupar archivos de infraestructura:
- `infra/.env.template`
- `infra/check_env.py`
- `infra/docker-compose.yml`
- `infra/README.md` (cómo levantar el entorno)

**GitHub Actions para deploy** → workflow que detecta push a `main`, ejecuta tests, construye contenedor, y despliega a Railway/Render automáticamente.

```yaml
- name: Deploy to Railway
  if: github.ref == 'refs/heads/main'
  run: railway up
```

**Ingeniero DevOps asistido por IA** → enfoque donde la IA genera configuraciones (Dockerfiles, workflows) pero tú validas, entiendes y ajustas según tu contexto.

## 🧠 GLOSARIO CLASE 6 – Defensa completa y CI/CD inteligente

**DevSecOps**

Integración de *desarrollo (Dev)*, *operaciones (Ops)* y *seguridad (Sec)* en un mismo flujo. No se “añade seguridad al final”, sino que se construye dentro del ciclo de vida del software.

**Pipeline CI/CD**

Secuencia automatizada que ejecuta *tests, auditorías, build y despliegue*. CI (Integración Continua) verifica el código cada vez que haces un cambio. CD (Entrega/Despliegue Continua) lo publica o lo prepara para producción.

**Secrets**

Variables cifradas que GitHub guarda en “Settings → Secrets and variables → Actions”. Permiten usar claves, tokens o contraseñas sin escribirlas en el código ni en el YAML.

**Variables de entorno (env)**

Parámetros que el código lee desde el sistema en tiempo de ejecución (`os.getenv()`).

Separan la configuración del código fuente, para evitar exponer datos sensibles.

**Notificaciones CI/CD**

Alertas automáticas (por ejemplo, Slack, Discord o correo) que se activan cuando un test o pipeline falla. Evitan depender de revisar manualmente los logs de GitHub.

**Despliegue simulado**

Etapa del pipeline que emula un despliegue real (por ejemplo, ejecutando los tests finales). Sirve para comprobar que la build y el entorno están listos antes de subirlos a producción.

**Dependabot / Safety / Gitleaks**

- *Dependabot:* actualiza dependencias automáticamente en GitHub.
- *Safety:* analiza librerías Python buscando vulnerabilidades.
- *Gitleaks:* detecta secretos o tokens subidos por error en commits.

**Rollback**

Proceso de revertir una versión a un estado anterior si el despliegue falla. En DevSecOps se automatiza para no dejar al sistema en un estado inseguro.

**Observabilidad**

Capacidad del sistema para reportar su propio estado. Incluye logs, métricas, y alertas (por ejemplo, integrando Sentry o reportes de IA).

**CI/CD Inteligente (con IA)**

Uso de la IA como asistente dentro del pipeline: resume logs, detecta patrones de error, genera informes de auditoría o propone mejoras al YAML.

La IA no despliega: **vigila y documenta.**
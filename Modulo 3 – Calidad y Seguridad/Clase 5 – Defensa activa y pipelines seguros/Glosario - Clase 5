### 🧩 Glosario

**DevSecOps**

Práctica que integra **seguridad (Sec)** en todas las fases del ciclo **DevOps** (desarrollo y operaciones). No se trata de añadir auditorías al final, sino de que el código, los tests y el pipeline sean seguros desde el principio.

**Pipeline CI/CD**

Secuencia automatizada que ejecuta tests, revisa el código y despliega. En DevSecOps también analiza vulnerabilidades, dependencias y secretos. CI = *Continuous Integration* (integración continua); CD = *Continuous Delivery* (entrega continua).

**Safety**

Herramienta que compara tus dependencias de Python con una base de datos de vulnerabilidades conocidas. Muestra si estás usando librerías con fallos de seguridad. Se integra fácilmente en el pipeline CI.

**Gitleaks**

Escáner que busca **claves, contraseñas o tokens** dentro del repositorio. Sirve para detectar fugas accidentales antes de hacer push o PR. Muy usado junto a `safety` en auditorías automáticas.

**Branch Protection Rules**

Reglas de protección de ramas en GitHub. Evitan merges directos a `main` si los tests fallan o si no hay revisión humana. Son el candado de tu pipeline: sin luz verde, no se integra el código.

**Dependabot / pip-audit / trivy**

Servicios y herramientas opcionales que amplían el escaneo de seguridad. Dependabot abre PRs automáticos para actualizar dependencias vulnerables. `pip-audit` revisa el `requirements.txt`. `Trivy` analiza imágenes Docker y entornos.

**Secretos (Secrets)**

Variables sensibles (claves, tokens, contraseñas) almacenadas fuera del código. En GitHub se guardan en *Settings → Secrets and variables → Actions*. Se inyectan como variables de entorno en el pipeline sin exponerse en el YAML.

**Auditoría continua**

Mecanismo que revisa el proyecto automáticamente (tests, linters, seguridad, dependencias). El objetivo no es encontrar errores, sino garantizar que si los hay, **no pasan desapercibidos**.

**Fallo controlado**

Estrategia de diseño del CI donde, si algo no pasa (test, lint, escaneo), el pipeline **rompe** antes de integrar. Así, los fallos ocurren en un entorno seguro, no en producción.

**notes.md**

Documento de reflexión por clase donde registras descubrimientos, decisiones y mejoras. Es parte de la trazabilidad del aprendizaje y, en la práctica, actúa como “bitácora de ingeniero”.

---

Con este glosario deberías poder navegar cómodamente por la clase, el pipeline y los conceptos de DevSecOps sin perderte.

La clave: **tu código ya no solo se prueba, ahora se vigila a sí mismo.**
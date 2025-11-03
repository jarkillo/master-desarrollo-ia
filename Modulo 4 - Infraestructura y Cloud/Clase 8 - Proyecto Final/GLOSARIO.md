# 📖 Glosario - Proyecto Final Módulo 4

Términos técnicos utilizados en el Proyecto Final de gestión de tareas.

---

## A

**Alembic**
Herramienta de migraciones de base de datos para SQLAlchemy. Permite versionar cambios en el schema de la BD sin perder datos.

**API (Application Programming Interface)**
Interfaz que permite la comunicación entre diferentes sistemas de software mediante endpoints HTTP.

**API Layer**
Capa de la aplicación que expone endpoints REST y maneja requests/responses. En este proyecto: FastAPI con endpoints como `/tareas`, `/auth/login`.

**Autenticación**
Proceso de verificar la identidad de un usuario (quién eres). En este proyecto: JWT tokens.

**Autorización**
Proceso de verificar qué puede hacer un usuario autenticado (qué permisos tienes). Ejemplo: solo puedes ver TUS tareas.

---

## B

**Bcrypt**
Algoritmo de hashing de passwords diseñado para ser lento (computacionalmente costoso), lo que dificulta ataques de fuerza bruta.

**Bearer Token**
Método de autenticación HTTP donde el token se envía en el header `Authorization: Bearer <token>`.

---

## C

**CASCADE**
Regla de foreign key que propaga operaciones. Ejemplo: `ondelete="CASCADE"` elimina las tareas cuando se elimina el usuario.

**CI/CD (Continuous Integration/Continuous Deployment)**
Práctica de automatizar tests y deployment. En este proyecto: GitHub Actions que ejecuta tests en cada push.

**Clean Architecture**
Patrón arquitectónico que separa la aplicación en capas con responsabilidades bien definidas. Permite cambiar implementaciones sin afectar otras capas.

**Coverage (Code Coverage)**
Porcentaje de código ejecutado por los tests. Este proyecto requiere 80% mínimo.

---

## D

**Database Layer**
Capa más baja de la arquitectura que maneja la persistencia física de datos. En este proyecto: PostgreSQL en producción, SQLite en desarrollo.

**Declarative Base**
Clase base de SQLAlchemy de la cual heredan todos los modelos ORM.

**Dependency Injection**
Patrón de diseño donde las dependencias se inyectan en lugar de crearse internamente. En FastAPI: `Depends(get_db)`.

**Docker**
Plataforma de contenedores que empaqueta una aplicación con todas sus dependencias en una imagen portable.

**Docker Compose**
Herramienta para definir y ejecutar aplicaciones Docker multi-contenedor. En este proyecto: PostgreSQL local para desarrollo.

**Dockerfile**
Archivo de texto con instrucciones para construir una imagen Docker.

---

## E

**Eager Loading**
Técnica de SQLAlchemy que carga relaciones en la misma query (usando JOINs) para evitar N+1 queries. Ejemplo: `joinedload(Tarea.usuario)`.

**Engine (SQLAlchemy)**
Objeto que gestiona conexiones a la base de datos. Se crea una vez al iniciar la aplicación.

**Environment Variables**
Variables de configuración del sistema operativo. En este proyecto: `DATABASE_URL`, `JWT_SECRET`, `ENVIRONMENT`.

---

## F

**FastAPI**
Framework web moderno de Python para crear APIs con validación automática, documentación interactiva y alto rendimiento.

**Fixture (pytest)**
Función que provee datos o configuración reutilizable para tests. Ejemplo: `test_db`, `auth_headers`.

**Foreign Key**
Columna que referencia la primary key de otra tabla, estableciendo una relación. Ejemplo: `usuario_id` en tareas.

---

## G

**GitHub Actions**
Servicio de CI/CD de GitHub que ejecuta workflows automáticos (tests, linting, deployment).

---

## H

**Hash (Password Hash)**
Transformación unidireccional de una contraseña en una cadena fija. No se puede revertir (no se puede obtener el password del hash).

**Health Check**
Endpoint que verifica el estado de la aplicación. En este proyecto: `GET /health` verifica conexión a BD.

**HTTP Status Code**
Código numérico que indica el resultado de un request. Ejemplos: 200 (OK), 201 (Created), 401 (Unauthorized), 404 (Not Found).

---

## I

**Index (Database Index)**
Estructura de datos que mejora la velocidad de búsquedas en una tabla. Ejemplo: índice en `usuario_id + completada`.

**Integration Test**
Test que verifica la interacción entre múltiples componentes (ej: repositorio con BD real).

---

## J

**JWT (JSON Web Token)**
Estándar para tokens de autenticación que contienen información cifrada. Formato: `header.payload.signature`.

---

## L

**Lazy Loading**
Comportamiento por defecto de SQLAlchemy donde las relaciones se cargan solo cuando se acceden (genera queries adicionales).

**Lifespan Events**
Funciones que se ejecutan al iniciar y cerrar la aplicación FastAPI. Ejemplo: crear tablas en startup.

---

## M

**Mapped (SQLAlchemy 2.0)**
Type hint que indica que un atributo está mapeado a una columna de BD. Ejemplo: `id: Mapped[int]`.

**Migration (Alembic)**
Archivo con cambios incrementales en el schema de BD. Permite actualizar la estructura sin perder datos.

**Multi-Stage Build (Docker)**
Técnica de Docker que usa múltiples stages para reducir el tamaño de la imagen final (builder + runtime).

---

## N

**N+1 Query Problem**
Anti-pattern donde se hace 1 query inicial + N queries adicionales en un loop. Solución: eager loading.

---

## O

**ORM (Object-Relational Mapper)**
Herramienta que mapea objetos Python a tablas de BD. En este proyecto: SQLAlchemy convierte `TareaModel` en tabla `tareas`.

---

## P

**Paginación**
Técnica de dividir resultados grandes en páginas. Parámetros: `page` (número) y `page_size` (tamaño).

**Payload (JWT)**
Parte del token que contiene los datos (claims) como `sub` (subject), `exp` (expiration), `user_id`.

**Protocol (Python)**
Tipo de Python para definir interfaces/contratos. En este proyecto: `RepositorioTareas` define qué métodos debe tener un repositorio.

**Pydantic**
Librería de validación de datos usando type hints. Valida requests/responses automáticamente.

**Pydantic Settings**
Extensión de Pydantic para gestionar configuración desde variables de entorno.

---

## Q

**Query (SQLAlchemy)**
Objeto que representa una consulta SQL. Ejemplo: `db.query(TareaModel).filter(...).all()`.

---

## R

**Railway**
Plataforma de cloud que simplifica el deployment de aplicaciones con conexión automática a PostgreSQL.

**Render**
Plataforma de cloud similar a Railway con soporte para `render.yaml` (infrastructure as code).

**Repository Pattern**
Patrón de diseño que abstrae el acceso a datos. El servicio habla con el repositorio, no con SQLAlchemy directamente.

**REST (Representational State Transfer)**
Estilo arquitectónico para APIs que usa HTTP methods (GET, POST, PUT, DELETE) y recursos (`/tareas`, `/usuarios`).

**Ruff**
Linter moderno de Python extremadamente rápido. Reemplaza flake8, isort, pyupgrade.

---

## S

**Schema (Pydantic)**
Modelo de datos para validación. Define la estructura de requests y responses. Ejemplo: `TareaCreate`, `TareaResponse`.

**Seed Data**
Datos iniciales para poblar la BD en desarrollo o testing.

**Service Layer**
Capa que contiene la lógica de negocio. Orquesta operaciones entre repositorios. Ejemplo: `ServicioTareas`.

**Session (SQLAlchemy)**
Objeto que gestiona una "conversación" con la BD. Se crea por request y se cierra al terminar.

**Soft Delete**
Marcar registros como eliminados sin borrarlos físicamente. Ejemplo: campo `eliminada=True` en tareas.

**SQLAlchemy**
ORM de Python para interactuar con bases de datos relacionales usando objetos Python.

**SQLite**
Base de datos embebida (archivo `.db`). Perfecta para desarrollo y tests, no para producción con alto tráfico.

---

## T

**TestClient (FastAPI)**
Cliente HTTP de testing que simula requests a la API sin iniciar un servidor real.

**Type Hint**
Anotación de tipos en Python. Ejemplo: `def crear(titulo: str) -> TareaModel:`. Mejora el IDE y detecta errores.

---

## U

**Unit Test**
Test que verifica un componente aislado (ej: un método del servicio) usando mocks para dependencias.

**Uvicorn**
Servidor ASGI de alto rendimiento para ejecutar aplicaciones FastAPI.

---

## V

**Validation (Pydantic)**
Proceso de verificar que los datos cumplen con el schema. Ejemplo: `titulo` debe tener min_length=1.

---

## W

**Workflow (GitHub Actions)**
Archivo YAML que define jobs automáticos (tests, linting, deployment).

---

## Términos de Arquitectura

**API → Service → Repository → Database**
Flujo de capas en la aplicación:
1. **API**: Recibe request, valida formato
2. **Service**: Aplica reglas de negocio
3. **Repository**: Abstrae acceso a datos
4. **Database**: Persiste físicamente

---

## Términos de Testing

**AAA (Arrange-Act-Assert)**
Patrón de escritura de tests:
- **Arrange**: Preparar datos de prueba
- **Act**: Ejecutar la acción a testear
- **Assert**: Verificar el resultado

**Fixture Scope**
Alcance de vida de una fixture:
- `function`: Se crea nueva por cada test (default)
- `module`: Se comparte entre tests del mismo archivo
- `session`: Se comparte entre todos los tests

---

## Términos de Deployment

**Blue-Green Deployment**
Estrategia donde mantienes 2 entornos (blue, green) y switcheas tráfico entre ellos para zero-downtime deploys.

**Rollback**
Revertir a una versión anterior del código o de la BD. Con Alembic: `alembic downgrade -1`.

**Zero-Downtime Deployment**
Deployment sin interrumpir el servicio. Requiere migraciones backward-compatible.

---

## Términos de Seguridad

**CORS (Cross-Origin Resource Sharing)**
Mecanismo que permite que un frontend en un dominio acceda a una API en otro dominio.

**Salt (Password Salt)**
Datos aleatorios agregados a un password antes de hashearlo. Previene ataques con rainbow tables.

**Secret Key (JWT_SECRET)**
Clave secreta usada para firmar y verificar JWT tokens. Debe ser de al menos 256 bits y mantenerse secreta.

---

## Siglas y Acrónimos

- **API**: Application Programming Interface
- **ASGI**: Asynchronous Server Gateway Interface
- **CRUD**: Create, Read, Update, Delete
- **DDL**: Data Definition Language (CREATE, ALTER, DROP)
- **DML**: Data Manipulation Language (INSERT, UPDATE, DELETE)
- **FK**: Foreign Key
- **HTTP**: HyperText Transfer Protocol
- **JSON**: JavaScript Object Notation
- **JWT**: JSON Web Token
- **ORM**: Object-Relational Mapper
- **PK**: Primary Key
- **REST**: Representational State Transfer
- **SOLID**: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **SQL**: Structured Query Language
- **TDD**: Test-Driven Development
- **URL**: Uniform Resource Locator

---

## Referencias

Para profundizar en estos conceptos:

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/en/20/
- **Alembic**: https://alembic.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **Docker**: https://docs.docker.com/
- **JWT**: https://jwt.io/
- **REST**: https://restfulapi.net/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

---

## ¿Falta algún término?

Si encuentras un término técnico en el proyecto que no está aquí, agrégalo siguiendo este formato:

```markdown
**Término**
Definición clara y concisa. Ejemplo de uso en el proyecto si es relevante.
```

Pull requests bienvenidos!

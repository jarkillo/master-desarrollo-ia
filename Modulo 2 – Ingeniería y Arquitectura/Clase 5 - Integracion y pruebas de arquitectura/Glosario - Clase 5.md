### 🧠 Glosario Clase 5 – Integración, estado y contratos

| Término | Significado claro |
| --- | --- |
| **Test de integración** | Prueba que **múltiples partes del sistema funcionen bien juntas** (ej. API + servicio + repositorio). No se enfoca en funciones individuales, sino en el flujo completo. |
| **Estado compartido** | Cuando un componente (como el repositorio) guarda cosas que afectan a otros tests si no se limpia. Es el origen de bugs fantasma. |
| **RepositorioMemoria** | Implementación del repositorio que guarda las tareas en una lista dentro de la propia app. Perfecto para tests rápidos y sin disco. |
| **RepositorioJSON** | Repositorio que guarda las tareas en un archivo `.json`. Simula persistencia real. Ideal para tests de integración más realistas. |
| **Servicio global** | Variable `servicio` definida fuera de las funciones, usada por la API. Si no se resetea entre tests, se acumula la mierda (estado). |
| **TestClient** | Herramienta de FastAPI que simula peticiones HTTP a tu API, sin levantar un servidor real. Útil para testear endpoints de forma rápida. |
| **Archivo temporal (`tempfile`)** | Archivo creado solo para el test, que se borra al terminar. Sirve para probar sin tocar archivos de producción. |
| **Inyección manual** | Reemplazar el `servicio` en la API antes de lanzar el test, para controlar qué repositorio se usa. Sin esto, el test depende del entorno. |
| **cliente vs app** | `app` es la instancia FastAPI; `cliente = TestClient(app)` es quien le envía peticiones. Debes crear el cliente después de inyectar el repo. |
| **respuesta** | Objeto que representa lo que devuelve un endpoint. Siempre mejor usar nombres como `respuesta_creacion` o `respuesta_listado`, no `r`. |

---

### ⚠️ Errores comunes que has vencido

| Error | Por qué pasa | Cómo lo solucionaste |
| --- | --- | --- |
| El test espera `id = 1`, pero recibe `id = 7` | El repositorio mantiene tareas previas | Inyectaste un repositorio limpio antes de cada test |
| El test pisa el archivo `tareas.json` de producción | El test y la app usan el mismo archivo | Usaste un archivo temporal (`tempfile`) |
| Los tests usan `cliente_http` global | El cliente se conecta a una API sucia | Mueves `TestClient(app)` dentro de cada test |
| El código tiene variables crípticas (`r`, `t`) | Pereza o copiar IA sin pensar | Refactorizas |
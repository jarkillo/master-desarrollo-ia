### **Principio Abierto/Cerrado (OCP – Open/Closed Principle)**

Es el segundo principio de SOLID.

Dice que *un módulo debe estar abierto a la extensión, pero cerrado a la modificación.*

Significa que cuando quieras añadir una nueva funcionalidad (por ejemplo, guardar tareas en un archivo JSON), **no deberías tocar el código existente**, sino **añadir una nueva clase o módulo** que cumpla la misma interfaz.

Así evitas romper lo que ya funciona.

> Ejemplo: en vez de editar ServicioTareas, creas RepositorioJSON que cumple la misma interfaz que RepositorioMemoria.
> 

---

### **Principio de Inversión de Dependencias (DIP – Dependency Inversion Principle)**

El quinto principio de SOLID.

Establece que los módulos de alto nivel (como tu servicio) **no deben depender de los módulos de bajo nivel** (como los repositorios concretos), sino **de abstracciones** (interfaces o protocolos).

Esto se logra **inyectando dependencias**: el servicio recibe un repositorio “desde fuera” en lugar de crearlo dentro.

> Así puedes cambiar el tipo de almacenamiento sin tocar el servicio ni la API.
> 

---

### **Inyección de dependencias**

Patrón de diseño que consiste en **pasar a una clase los objetos que necesita** (sus dependencias) en lugar de crearlos dentro.

Hace que tu código sea más flexible, testeable y extensible.

> Ejemplo: ServicioTareas recibe un RepositorioTareas como parámetro en el constructor.
> 

---

### **Abstracción / Contrato / Interfaz**

Una **abstracción** define *qué debe hacer algo*, pero no *cómo lo hace*.

En Python se suele expresar con `Protocol` (de `typing`) o clases base abstractas (`ABC`).

Cualquier clase que implemente los métodos definidos en ese protocolo puede sustituir a otra.

> Ejemplo: RepositorioTareas define guardar() y listar().
> 
> 
> `RepositorioMemoria` y `RepositorioJSON` los implementan con distintos mecanismos.
> 

---

### **Repositorio**

Es una **capa de acceso a datos**.

Su función es aislar el resto del sistema de los detalles sobre cómo se guardan los datos (en memoria, en disco, en base de datos…).

Permite cambiar la persistencia sin reescribir la lógica del negocio.

> RepositorioMemoria → guarda en listas en RAM.
> 
> 
> `RepositorioJSON` → guarda en un archivo `.json`.
> 

---

### **Servicio (o capa de negocio)**

Es la parte que contiene la **lógica del dominio**: las reglas y acciones principales del sistema.

En nuestro caso, `ServicioTareas` crea y lista tareas.

No sabe nada del mundo externo (HTTP, FastAPI, ni bases de datos).

> Su único objetivo es aplicar las reglas de negocio sobre los datos.
> 

---

### **API / Capa de presentación**

Es la **interfaz que comunica el sistema con el exterior**.

Recibe peticiones HTTP, valida los datos y delega el trabajo al servicio.

En este curso se usa **FastAPI**, pero el mismo principio aplica a cualquier framework.

> La API no decide cómo guardar ni cómo calcular nada; solo traduce “entrada/salida”.
> 

---

### **Inversión de control**

Concepto general del que deriva la inyección de dependencias.

Significa que el flujo de control ya no lo decide el módulo superior (“yo creo mis objetos”), sino un **contenedor externo o el framework** (“yo te paso tus dependencias”).

En frameworks como FastAPI, esto se maneja de forma natural cuando defines dependencias en los endpoints.

---

### **Protocol (Python typing)**

Herramienta de tipado que permite definir una interfaz sin necesidad de herencia formal.

Si una clase tiene los mismos métodos que el protocolo declara, Python la considera compatible.

Ideal para aplicar SOLID sin complicar la arquitectura.

> Ejemplo:
> 
> 
> ```python
> class RepositorioTareas(Protocol):
>     def guardar(self, tarea: Tarea) -> None: ...
>     def listar(self) -> list[Tarea]: ...
> 
> ```
> 

---

### **Extensibilidad**

Propiedad del código que permite **añadir nuevas funcionalidades sin modificar lo existente**.

Es la consecuencia natural de aplicar OCP y DIP.

Un proyecto extensible crece con nuevas piezas, no con cirugías dolorosas.

---

### **Test de integración**

Tipo de test que verifica que distintas capas (por ejemplo, API + Servicio + Repositorio) funcionan juntas correctamente.

En esta clase, puedes probar tu API con FastAPI usando `TestClient`, verificando que responde igual con `RepositorioMemoria` o `RepositorioJSON`.

---

### **Arquitectura limpia**

Estructura que separa el código en capas independientes (API, servicio, repositorio).

Cada capa tiene una única responsabilidad y se comunica con las demás mediante contratos.

Permite mantener y escalar el sistema sin miedo a romperlo.

---

## 🧩 Conclusión mental

Tu objetivo con esta clase es **entender la libertad del código bien diseñado**:

puedes cambiar cómo se guarda, se valida o se lista una tarea sin reescribir toda la app.

Esa es la diferencia entre *“un programa que funciona”* y *“un sistema que puede crecer”*.
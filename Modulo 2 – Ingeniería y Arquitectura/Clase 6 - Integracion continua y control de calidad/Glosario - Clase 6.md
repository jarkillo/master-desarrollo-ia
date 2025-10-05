### **Integración continua (CI)**

Proceso automatizado que ejecuta los tests de tu proyecto cada vez que haces `push` o abres un PR.

Garantiza que nadie (ni tú) rompa nada sin darse cuenta. Se configura con workflows (ej. GitHub Actions).

### **GitHub Actions**

Sistema de automatización integrado en GitHub.

Puedes programarlo para que haga cosas al hacer push, PR, merge, etc.

Ejemplo: instalar dependencias, ejecutar tests, desplegar tu app…

### **Workflow (.yml)**

Archivo donde defines lo que quieres que GitHub Actions haga.

Vive en `.github/workflows/` y se escribe en YAML.

Ejemplo: `ci.yml` que corre los tests automáticamente.

### **Push**

Cuando subes tus cambios al servidor remoto (ej. GitHub). Si tienes un workflow configurado, lo dispara.

### **Pull Request (PR)**

Solicitud para fusionar una rama con otra. En un proyecto con CI, **nunca deberías hacer merge sin pasar los tests**.

### **pytest**

Framework de testing en Python.

Con `pytest -v` ejecutas todos los tests de tu proyecto y ves qué pasa.

### **requirements.txt**

Archivo donde defines todas las dependencias de tu proyecto en Python.

El CI lo usará para instalar lo necesario antes de correr los tests.

### **Artefactos**

Archivos generados durante un workflow (como reportes de cobertura) que GitHub puede guardar para que los descargues o analices.

### **Coverage (Cobertura de código)**

Porcentaje de tu código que está cubierto por tests.

No mide calidad, pero sí visibilidad: si algo no está cubierto, puede romperse sin que lo detectes.

### **Inmutabilidad de la arquitectura**

Idea central del módulo: si haces bien la separación en capas y contratos, puedes cambiar el interior sin que nada externo se rompa.

La CI lo valida constantemente.

### **notes.md**

Archivo de reflexión personal por clase.

No es documentación técnica, es donde anotas *qué entendiste*,
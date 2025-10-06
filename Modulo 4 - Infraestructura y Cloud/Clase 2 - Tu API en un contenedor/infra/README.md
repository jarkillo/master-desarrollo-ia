# 📦 Carpeta /infra

Esta carpeta contiene los archivos relacionados con la infraestructura y el despliegue del proyecto.

## Contenido

- **.env.template** → Plantilla de variables de entorno (sin valores reales).  
- **check_env.py** → Script que verifica que tu `.env` contenga todas las variables necesarias.  
- *(Más adelante se añadirá)* `docker-compose.yml`, `deploy.yml`, etc.

## Uso

1. Copia `.env.template` a `.env` y completa los valores.
2. Ejecuta el validador:
   ```bash
   python infra/check_env.py
    ```
Si todo está correcto, verás:
```bash
✅ Variables sincronizadas correctamente
```

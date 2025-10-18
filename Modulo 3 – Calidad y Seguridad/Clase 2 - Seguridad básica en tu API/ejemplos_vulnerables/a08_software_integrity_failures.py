# ejemplos_vulnerables/a08_software_integrity_failures.py
"""
CÓDIGO VULNERABLE - A08: Software and Data Integrity Failures

Este código fue generado por IA sin contexto de seguridad.
Demuestra vulnerabilidades de integridad de software y datos.

VULNERABILIDADES:
1. Dependencias sin versiones pinneadas
2. No auditadas con Safety
3. Instalación de paquetes desde fuentes no verificadas
4. Deserialización insegura con pickle
5. Sin verificación de integridad de datos
"""

import pickle
from typing import Any

# ========================================
# VULNERABLE 1: requirements.txt sin versiones pinneadas
# ========================================

"""
❌ requirements.txt VULNERABLE:

fastapi
uvicorn
pydantic
requests
sqlalchemy
redis

PROBLEMA:
- No especifica versiones exactas
- pip install puede instalar versiones con vulnerabilidades conocidas
- Builds no son reproducibles (diferentes versiones en dev/prod)

ESCENARIO DE ATAQUE:
1. Dependencia "requests" tiene vulnerabilidad crítica en versión 2.25.0
2. requirements.txt no especifica versión, instala 2.25.0
3. Aplicación vulnerable a CVE-2021-XXXXX ❌


✅ requirements.txt SEGURO:

fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.10.3
requests==2.32.3  # ✅ Versión sin vulnerabilidades conocidas
sqlalchemy==2.0.36
redis==5.2.1

# ✅ Versiones exactas
# ✅ Auditado con `safety check`
# ✅ Builds reproducibles
"""

# ========================================
# VULNERABLE 2: Deserialización insegura con pickle
# ========================================


class TareaSerializada:
    """Ejemplo de deserialización insegura"""

    @staticmethod
    def guardar_tarea(tarea: Any, archivo: str):
        """
        VULNERABILIDAD CRÍTICA: Usa pickle para serializar objetos.

        pickle puede ejecutar código arbitrario al deserializar.
        """
        with open(archivo, 'wb') as f:
            # ❌ pickle permite ejecución de código arbitrario
            pickle.dump(tarea, f)

    @staticmethod
    def cargar_tarea(archivo: str) -> Any:
        """
        VULNERABILIDAD CRÍTICA: Deserializa con pickle.

        ESCENARIO DE ATAQUE:
        1. Atacante crea archivo pickle malicioso que ejecuta código
        2. Archivo se sube a la aplicación
        3. Al hacer pickle.load(), se ejecuta código del atacante ❌
        4. Compromiso total del servidor
        """
        with open(archivo, 'rb') as f:
            # ❌ NUNCA deserializar datos no confiables con pickle
            return pickle.load(f)


# Ejemplo de payload malicioso con pickle:
"""
import pickle
import os

class MaliciousPayload:
    def __reduce__(self):
        # Este código se ejecuta al hacer pickle.load()
        return (os.system, ('rm -rf /',))  # ❌ Elimina archivos del servidor

# Atacante crea archivo malicioso
with open('malicious.pkl', 'wb') as f:
    pickle.dump(MaliciousPayload(), f)

# Víctima carga archivo
with open('malicious.pkl', 'rb') as f:
    pickle.load(f)  # ❌ Ejecuta rm -rf / en el servidor
"""

# ========================================
# VULNERABLE 3: Instalación de paquetes no verificados
# ========================================

"""
❌ VULNERABLE: Instalar paquetes sin verificar

pip install paquete-sospechoso
pip install git+https://github.com/desconocido/repo.git  # ❌ Fuente no confiable


ESCENARIO DE ATAQUE (Typosquatting):
1. Atacante crea paquete "requets" (typo de "requests")
2. Desarrollador hace: pip install requets  # ❌ Typo
3. Paquete malicioso se instala
4. Roba credenciales, variables de entorno, código ❌


✅ SEGURO: Verificar integridad

# Usar pip con hash verification
pip install --require-hashes -r requirements.txt

# requirements.txt con hashes:
fastapi==0.115.0 \\
    --hash=sha256:abc123...

# O usar pip-audit para auditar
pip-audit
"""

# ========================================
# VULNERABLE 4: Sin verificación de integridad de datos
# ========================================

from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/importar-tareas")
async def importar_tareas(archivo: UploadFile):
    """
    VULNERABILIDAD: No valida integridad del archivo subido.

    ESCENARIO DE ATAQUE:
    1. Atacante sube archivo JSON manipulado
    2. Aplicación lo procesa sin validación
    3. Datos corruptos en la base de datos ❌
    """
    contenido = await archivo.read()

    # ❌ No valida checksum/hash del archivo
    # ❌ No valida firma digital
    # ❌ Confía ciegamente en datos externos

    return {"message": "Tareas importadas", "warning": "Sin verificación de integridad"}


# ========================================
# VULNERABLE 5: Dependencias desactualizadas
# ========================================

"""
❌ VULNERABLE: No auditar dependencias regularmente

# requirements.txt con versiones antiguas vulnerables
fastapi==0.68.0  # ❌ Versión de 2021 con vulnerabilidades conocidas
pydantic==1.8.0  # ❌ Versión antigua
requests==2.25.0  # ❌ CVE-2021-43138


PROBLEMA:
- No se ejecuta `safety check` regularmente
- No se actualizan dependencias
- Vulnerabilidades conocidas quedan sin parchar


✅ SEGURO: Auditar regularmente

# CI/CD pipeline debe incluir:
safety check --json
pip-audit
bandit -r .

# Actualizar dependencias trimestralmente
pip list --outdated
pip install --upgrade fastapi pydantic
"""

# ========================================
# CÓDIGO CORREGIDO (para comparación)
# ========================================

"""
CORRECCIÓN 1: requirements.txt con versiones pinneadas y auditadas

# requirements.txt
# Auditado con `safety check` el 2025-01-15
# Sin vulnerabilidades conocidas

fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.10.3
requests==2.32.3
sqlalchemy==2.0.36
redis==5.2.1

# Para desarrollo
pytest==8.4.2
pytest-cov==6.0.0
safety==3.2.11
bandit==1.8.0


CORRECCIÓN 2: Usar JSON en vez de pickle

import json
from pydantic import BaseModel

class Tarea(BaseModel):
    id: int
    nombre: str
    completada: bool

def guardar_tarea_seguro(tarea: Tarea, archivo: str):
    with open(archivo, 'w') as f:
        # ✅ JSON es seguro para deserialización
        json.dump(tarea.model_dump(), f)

def cargar_tarea_seguro(archivo: str) -> Tarea:
    with open(archivo, 'r') as f:
        datos = json.load(f)
        # ✅ Pydantic valida la estructura
        return Tarea(**datos)


CORRECCIÓN 3: Verificar integridad de archivos subidos

import hashlib
from fastapi import UploadFile, HTTPException

@app.post("/importar-tareas")
async def importar_tareas_seguro(
    archivo: UploadFile,
    checksum_esperado: str  # ✅ Cliente proporciona hash esperado
):
    contenido = await archivo.read()

    # ✅ Calcular hash del archivo
    hash_calculado = hashlib.sha256(contenido).hexdigest()

    # ✅ Verificar integridad
    if hash_calculado != checksum_esperado:
        raise HTTPException(
            status_code=400,
            detail="Integridad del archivo comprometida"
        )

    # ✅ Ahora es seguro procesar
    return {"message": "Tareas importadas con integridad verificada"}


CORRECCIÓN 4: CI/CD con auditoría de seguridad

# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -r requirements.txt

      # ✅ Auditar dependencias
      - name: Safety check
        run: safety check --json

      # ✅ Auditar código
      - name: Bandit scan
        run: bandit -r . -ll

      # ✅ Verificar versiones
      - name: pip-audit
        run: pip-audit
"""

# ========================================
# EJERCICIO
# ========================================

"""
1. Identifica las 5 vulnerabilidades de integridad en este código
2. Explica el riesgo de pickle.load() con datos no confiables
3. Crea requirements.txt con versiones pinneadas
4. Ejecuta `safety check` y corrige vulnerabilidades encontradas
5. Reemplaza pickle por JSON + Pydantic
6. Implementa verificación de checksum en uploads
7. Escribe tests:
   - test_dependencias_sin_vulnerabilidades()
   - test_archivo_con_checksum_invalido_rechazado()
   - test_no_usa_pickle()
"""

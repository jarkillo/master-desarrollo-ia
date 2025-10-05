# api/dependencias.py
import os
from fastapi import Header, HTTPException


def verificar_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    esperada = os.getenv("API_KEY")  # leer en cada petición
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key inválida")

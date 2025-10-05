# api/dependencias.py
from fastapi import Header, HTTPException, Depends
import os

API_KEY_ESPERADA = os.getenv("API_KEY")


def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_ESPERADA:
        raise HTTPException(status_code=401, detail="API key inválida")

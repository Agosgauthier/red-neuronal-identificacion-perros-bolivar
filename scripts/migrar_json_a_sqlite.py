"""Migra registros viejos (data/found/datos.json) a SQLite.

Uso: python -m scripts.migrar_json_a_sqlite
"""
import json

from src import config
from src.domain.perro_encontrado import PerroEncontrado
from src.repositories.perros_repository import PerrosRepository

RUTA_JSON = config.RUTA_ENCONTRADOS / "datos.json"


def migrar():
    if not RUTA_JSON.exists():
        print("No se encontró data/found/datos.json.")
        return

    registros = json.loads(RUTA_JSON.read_text(encoding="utf-8"))
    if not isinstance(registros, list):
        raise ValueError("El JSON debe contener una lista de registros.")

    repo = PerrosRepository()
    existentes = {p.imagen for p in repo.listar()}
    migrados = omitidos = 0

    for r in registros:
        nombre = r.get("imagen")
        if not nombre or nombre in existentes:
            omitidos += 1
            continue
        repo.registrar(PerroEncontrado(
            imagen=nombre,
            zona=r.get("zona", ""),
            fecha=r.get("fecha", ""),
            descripcion=r.get("descripcion", ""),
            contacto=r.get("contacto", ""),
            fecha_registro=r.get("fecha_registro", ""),
        ))
        migrados += 1

    print(f"Migrados: {migrados} | Omitidos: {omitidos} (el JSON no se modificó)")


if __name__ == "__main__":
    migrar()
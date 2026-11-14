"""RegistroService: valida y guarda un perro encontrado (foto + datos en SQLite)."""
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image

from src import config
from src.domain.errores import ValidacionError
from src.domain.perro_encontrado import PerroEncontrado
from src.repositories.perros_repository import PerrosRepository


class RegistroService:
    def __init__(self, repositorio: PerrosRepository,
                 ruta_encontrados: Path = config.RUTA_ENCONTRADOS):
        self.repositorio = repositorio
        self.ruta_encontrados = Path(ruta_encontrados)

    def registrar(self, imagen, zona, fecha, descripcion, contacto) -> PerroEncontrado:
        self._validar(imagen, zona, fecha, contacto)

        ahora = datetime.now()
        nombre = f"encontrado_{ahora.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        ruta = self._guardar_foto(imagen, nombre)

        perro = PerroEncontrado(
            imagen=nombre, zona=zona.strip(), fecha=fecha.strip(),
            descripcion=(descripcion or "").strip(), contacto=contacto.strip(),
            fecha_registro=ahora.isoformat(),
        )
        try:
            perro.id = self.repositorio.registrar(perro)
        except Exception:
            ruta.unlink(missing_ok=True)  # no dejar la foto huérfana
            raise
        return perro

    @staticmethod
    def _validar(imagen, zona, fecha, contacto) -> None:
        if imagen is None:
            raise ValidacionError("Primero cargá una fotografía del perro.")
        if not (zona or "").strip():
            raise ValidacionError("Indicá dónde encontraste al perro.")
        if not (fecha or "").strip():
            raise ValidacionError("Indicá la fecha en la que lo encontraste.")
        if not (contacto or "").strip():
            raise ValidacionError("Indicá un medio de contacto.")

    def _guardar_foto(self, imagen, nombre: str) -> Path:
        self.ruta_encontrados.mkdir(parents=True, exist_ok=True)
        ruta = self.ruta_encontrados / nombre
        Image.fromarray(np.asarray(imagen).astype(np.uint8)).convert("RGB").save(ruta, "JPEG")
        return ruta
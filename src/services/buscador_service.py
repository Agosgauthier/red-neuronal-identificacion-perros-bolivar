"""BuscadorService: busca coincidencias y registra perros encontrados."""
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image

from src import config
from src.models.perro import Coincidencia, PerroEncontrado, ResultadoBusqueda
from src.services.modelo_service import ModeloService
from src.services.perros_repository import PerrosRepository


class ValidacionError(ValueError):
    """Datos incompletos al registrar un perro."""


class BuscadorService:
    def __init__(
        self,
        modelo: ModeloService,
        repositorio: PerrosRepository,
        ruta_candidatos: Path = config.RUTA_CANDIDATOS,
        ruta_encontrados: Path = config.RUTA_ENCONTRADOS,
        umbral: float = config.UMBRAL_COINCIDENCIA,
        cantidad: int = config.CANTIDAD_RESULTADOS,
    ):
        self.modelo = modelo
        self.repositorio = repositorio
        self.ruta_candidatos = Path(ruta_candidatos)
        self.ruta_encontrados = Path(ruta_encontrados)
        self.umbral = umbral
        self.cantidad = cantidad

    def listar_candidatos(self) -> list:
        rutas = []
        for carpeta in (self.ruta_candidatos, self.ruta_encontrados):
            if carpeta.exists():
                rutas += [
                    r for r in carpeta.iterdir()
                    if r.is_file() and r.suffix.lower() in config.EXTENSIONES_VALIDAS
                ]
        return sorted(rutas)

    def buscar(self, imagen_perdido) -> ResultadoBusqueda:
        candidatos = self.listar_candidatos()
        if not candidatos:
            return ResultadoBusqueda([], 0, False,
                                     mensaje="No se encontraron fotografías candidatas.")

        resultados = []
        for ruta in candidatos:
            try:
                sim = self.modelo.probabilidad_mismo(
                    imagen_perdido, self.modelo.leer_imagen(ruta))
            except Exception as error:  # una foto dañada no frena la búsqueda
                print(f"Error procesando {ruta.name}: {error}")
                continue
            resultados.append(Coincidencia(ruta, sim))

        if not resultados:
            return ResultadoBusqueda([], 0, False,
                                     mensaje="No se pudieron procesar las fotografías candidatas.")

        resultados.sort(key=lambda c: c.similitud, reverse=True)
        mejor = resultados[0].similitud
        if mejor < self.umbral:
            return ResultadoBusqueda([], len(resultados), False, mejor)

        top = [c for c in resultados if c.similitud >= self.umbral][: self.cantidad]    
        for c in top:
            if c.ruta.parent == self.ruta_encontrados:
                c.datos = self.repositorio.obtener_por_imagen(c.ruta.name)
        return ResultadoBusqueda(top, len(resultados), True, mejor)

    def comparar(self, imagen1, imagen2) -> tuple:
        sim = self.modelo.probabilidad_mismo(imagen1, imagen2)
        return sim >= self.umbral, sim

    def registrar_encontrado(self, imagen, zona, fecha, descripcion, contacto) -> PerroEncontrado:
        if imagen is None:
            raise ValidacionError("Primero cargá una fotografía del perro.")
        if not (zona or "").strip():
            raise ValidacionError("Indicá dónde encontraste al perro.")
        if not (fecha or "").strip():
            raise ValidacionError("Indicá la fecha en la que lo encontraste.")
        if not (contacto or "").strip():
            raise ValidacionError("Indicá un medio de contacto.")

        self.ruta_encontrados.mkdir(parents=True, exist_ok=True)
        ahora = datetime.now()
        nombre = f"encontrado_{ahora.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        ruta = self.ruta_encontrados / nombre
        Image.fromarray(np.asarray(imagen).astype(np.uint8)).convert("RGB").save(ruta, "JPEG")

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
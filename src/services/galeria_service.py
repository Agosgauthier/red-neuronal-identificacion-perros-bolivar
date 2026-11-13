"""GaleriaService: lista las fotos contra las que se busca (candidatas + encontradas)."""
from pathlib import Path
from typing import List

from src import config


class GaleriaService:
    def __init__(self, ruta_candidatos: Path = config.RUTA_CANDIDATOS,
                 ruta_encontrados: Path = config.RUTA_ENCONTRADOS):
        self.ruta_candidatos = Path(ruta_candidatos)
        self.ruta_encontrados = Path(ruta_encontrados)

    def listar(self) -> List[Path]:
        rutas = []
        for carpeta in (self.ruta_candidatos, self.ruta_encontrados):
            if carpeta.exists():
                rutas += [r for r in carpeta.iterdir()
                          if r.is_file() and r.suffix.lower() in config.EXTENSIONES_VALIDAS]
        return sorted(rutas)

    def es_encontrado(self, ruta: Path) -> bool:
        return Path(ruta).parent == self.ruta_encontrados
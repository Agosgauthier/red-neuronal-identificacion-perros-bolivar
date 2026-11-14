"""DescargaDatasetService: baja y descomprime el dataset YT-BB-Dog (trae un zip dentro de otro)."""
import urllib.request
import zipfile
from pathlib import Path

from src import config


class DescargaDatasetService:
    def __init__(self, url: str = config.URL_DATASET, destino: Path = config.RUTA_DESCARGAS):
        self.url = url
        self.destino = Path(destino)

    @property
    def ruta_dataset(self) -> Path:
        return self.destino / "perros" / "YT-BB-Dog"

    def ya_descargado(self) -> bool:
        return (self.ruta_dataset / "train").exists() and (self.ruta_dataset / "test").exists()

    def descargar(self) -> Path:
        """Descarga y descomprime solo si todavía no está. Devuelve la carpeta del dataset."""
        if self.ya_descargado():
            return self.ruta_dataset
        self.destino.mkdir(parents=True, exist_ok=True)
        zip_externo = self.destino / "YT-BB-Dog.zip"
        urllib.request.urlretrieve(self.url, zip_externo)
        return self.descomprimir(zip_externo)

    def descomprimir(self, zip_externo: Path) -> Path:
        with zipfile.ZipFile(zip_externo) as z:
            z.extractall(self.destino)
        zip_interno = self.destino / "YT-BB-dog" / "YT-BB-Dog.zip"
        with zipfile.ZipFile(zip_interno) as z:
            z.extractall(self.destino / "perros")
        return self.ruta_dataset
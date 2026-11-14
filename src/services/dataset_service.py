"""DatasetService: arma pares (mismo perro / distinto perro) separando por IDENTIDAD."""
import random
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.domain.perro_dataset import PerroDataset
from src.services.imagen_service import ImagenService


class DatasetService:
    def __init__(self, base: Path, imagenes: ImagenService = None, semilla: int = 42):
        self.base = Path(base)
        self.imagenes = imagenes or ImagenService()
        self.azar = random.Random(semilla)

    # ---------- identidades ----------
    def listar_perros(self, parte: str) -> List[PerroDataset]:
        """Perros de 'train' o 'test' con al menos 2 fotos."""
        perros = []
        for carpeta in sorted((self.base / parte).iterdir()):
            if carpeta.is_dir():
                fotos = sorted(carpeta.glob("*.jpg"))
                if len(fotos) >= 2:
                    perros.append(PerroDataset(carpeta.name, fotos))
        return perros

    # ---------- pares ----------
    def crear_pares(self, perros: List[PerroDataset], pares_por_perro: int) -> pd.DataFrame:
        pares = []
        for perro in perros:
            for _ in range(pares_por_perro):
                a, b = self.azar.sample(perro.fotos, 2)
                pares.append({"imagen1": str(a), "imagen2": str(b), "label": 1})
        for _ in range(len(pares)):
            p1, p2 = self.azar.sample(perros, 2)  # siempre perros distintos
            pares.append({"imagen1": str(self.azar.choice(p1.fotos)),
                          "imagen2": str(self.azar.choice(p2.fotos)), "label": 0})
        df = pd.DataFrame(pares)
        return df.sample(frac=1, random_state=42).reset_index(drop=True)

    def dividir(self, config: ConfiguracionEntrenamiento = ConfiguracionEntrenamiento()) -> dict:
        """Train y validación salen de la carpeta train (perros distintos); test, de la carpeta test."""
        elegidos = self.azar.sample(self.listar_perros("train"),
                                    config.perros_train + config.perros_val)
        perros_train = elegidos[:config.perros_train]
        perros_val = elegidos[config.perros_train:]
        perros_test = self.azar.sample(self.listar_perros("test"), config.perros_test)

        ids_train = {p.id for p in perros_train}
        ids_val = {p.id for p in perros_val}
        assert ids_train.isdisjoint(ids_val), "Un perro quedó en train y validación"

        n = config.pares_por_perro
        return {
            "train": self.crear_pares(perros_train, n),
            "val": self.crear_pares(perros_val, n),
            "test": self.crear_pares(perros_test, n),
        }

    @staticmethod
    def guardar_pares(conjuntos: dict, carpeta: Path) -> None:
        carpeta = Path(carpeta)
        carpeta.mkdir(parents=True, exist_ok=True)
        for nombre, df in conjuntos.items():
            df.to_csv(carpeta / f"pares_{nombre}.csv", index=False)

    # ---------- carga de imágenes ----------
    def cargar_arrays(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """DataFrame de pares -> (X1, X2, y) listos para la red."""
        x1 = self.imagenes.cargar_lote(df["imagen1"])
        x2 = self.imagenes.cargar_lote(df["imagen2"])
        return x1, x2, df["label"].to_numpy(dtype="float32")

    # ---------- buscador ----------
    def crear_consultas_ranking(self, parte: str, cantidad: int, semilla: int) -> Tuple[list, list]:
        """Por cada perro: una foto 'registrada' (galería) y otra distinta para buscar."""
        azar = random.Random(semilla)
        perros = azar.sample(self.listar_perros(parte), cantidad)
        galeria, consultas = [], []
        for perro in perros:
            registrada, busqueda = azar.sample(perro.fotos, 2)
            galeria.append(registrada)
            consultas.append(busqueda)
        return galeria, consultas
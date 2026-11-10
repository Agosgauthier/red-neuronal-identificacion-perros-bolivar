"""DatasetService: arma pares (mismo perro / distinto perro) separando por IDENTIDAD."""
import random
from pathlib import Path

import pandas as pd


class DatasetService:
    def __init__(self, base: Path, semilla: int = 42):
        self.base = Path(base)
        self.azar = random.Random(semilla)

    def listar_perros(self, parte: str) -> list:
        """Devuelve [(id_perro, [rutas])] con al menos 2 fotos por perro."""
        perros = []
        for carpeta in (self.base / parte).iterdir():
            if carpeta.is_dir():
                fotos = sorted(carpeta.glob("*.jpg"))
                if len(fotos) >= 2:
                    perros.append((carpeta.name, fotos))
        return sorted(perros)

    def crear_pares(self, perros: list, pares_por_perro: int) -> pd.DataFrame:
        pares = []
        for _, fotos in perros:
            for _ in range(pares_por_perro):
                a, b = self.azar.sample(fotos, 2)
                pares.append({"imagen1": str(a), "imagen2": str(b), "label": 1})
        for _ in range(len(pares)):
            (id1, f1), (id2, f2) = self.azar.sample(perros, 2)  # siempre distintos
            pares.append({"imagen1": str(self.azar.choice(f1)),
                          "imagen2": str(self.azar.choice(f2)), "label": 0})
        df = pd.DataFrame(pares)
        return df.sample(frac=1, random_state=42).reset_index(drop=True)

    def dividir(self, n_train=300, n_val=100, n_test=100, pares_por_perro=10) -> dict:
        train_val = self.azar.sample(self.listar_perros("train"), n_train + n_val)
        perros_train, perros_val = train_val[:n_train], train_val[n_train:]
        perros_test = self.azar.sample(self.listar_perros("test"), n_test)

        ids = [{p[0] for p in g} for g in (perros_train, perros_val)]
        assert ids[0].isdisjoint(ids[1]), "Un perro quedó en train y validación"

        return {
            "train": self.crear_pares(perros_train, pares_por_perro),
            "val": self.crear_pares(perros_val, pares_por_perro),
            "test": self.crear_pares(perros_test, pares_por_perro),
        }

    @staticmethod
    def guardar(conjuntos: dict, carpeta: Path):
        carpeta = Path(carpeta)
        carpeta.mkdir(parents=True, exist_ok=True)
        for nombre, df in conjuntos.items():
            df.to_csv(carpeta / f"pares_{nombre}.csv", index=False)
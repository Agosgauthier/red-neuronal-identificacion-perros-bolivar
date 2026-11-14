import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.services.dataset_service import DatasetService
from src.services.evaluacion_service import EvaluacionService


def crear_dataset_falso(base: Path, perros_train=30, perros_test=10, fotos=4):
    for parte, n in (("train", perros_train), ("test", perros_test)):
        for i in range(n):
            carpeta = base / parte / f"{parte}_{i}"
            carpeta.mkdir(parents=True)
            for j in range(fotos):
                (carpeta / f"{i}_{j}.jpg").write_bytes(b"x")


class TestDatasetService(unittest.TestCase):
    def test_pares_balanceados_y_sin_fuga(self):
        with tempfile.TemporaryDirectory() as d:
            crear_dataset_falso(Path(d))
            config = ConfiguracionEntrenamiento(
                perros_train=15, perros_val=5, perros_test=5, pares_por_perro=3)
            c = DatasetService(Path(d)).dividir(config)
            for df in c.values():
                self.assertEqual((df.label == 1).sum(), (df.label == 0).sum())

            def ids(df):
                return {Path(p).parent.name
                        for col in ("imagen1", "imagen2") for p in df[col]}

            self.assertTrue(ids(c["train"]).isdisjoint(ids(c["val"])))

    def test_par_positivo_es_del_mismo_perro(self):
        with tempfile.TemporaryDirectory() as d:
            crear_dataset_falso(Path(d))
            ds = DatasetService(Path(d))
            df = ds.crear_pares(ds.listar_perros("train")[:5], 4)
            pos, neg = df[df.label == 1], df[df.label == 0]
            self.assertTrue(all(Path(a).parent == Path(b).parent
                                for a, b in zip(pos.imagen1, pos.imagen2)))
            self.assertTrue(all(Path(a).parent != Path(b).parent
                                for a, b in zip(neg.imagen1, neg.imagen2)))

    def test_consultas_ranking_son_fotos_distintas_del_mismo_perro(self):
        with tempfile.TemporaryDirectory() as d:
            crear_dataset_falso(Path(d))
            galeria, consultas = DatasetService(Path(d)).crear_consultas_ranking("test", 5, 7)
            self.assertEqual(len(galeria), 5)
            for g, q in zip(galeria, consultas):
                self.assertEqual(g.parent, q.parent)
                self.assertNotEqual(g, q)


class TestEvaluacionService(unittest.TestCase):
    def setUp(self):
        self.servicio = EvaluacionService()

    def test_metricas_y_umbral(self):
        y = np.array([1, 1, 1, 0, 0, 0])
        p = np.array([0.9, 0.8, 0.7, 0.3, 0.2, 0.1])
        u, f1 = self.servicio.elegir_umbral(y, p, 0.05, 0.95, 0.05)
        self.assertEqual(f1, 1.0)
        m = self.servicio.evaluar(y, p, u)
        self.assertEqual(m.accuracy, 1.0)
        self.assertEqual(m.matriz_confusion, [[3, 0], [0, 3]])

    def test_ranking_perfecto(self):
        galeria = np.eye(4)
        r = self.servicio.ranking(galeria, galeria)
        self.assertEqual(r.aciertos, {1: 4, 3: 4, 5: 4})
        self.assertEqual(r.total, 4)

    def test_similitud_coseno(self):
        a = np.array([[1.0, 0.0], [1.0, 0.0]])
        b = np.array([[1.0, 0.0], [0.0, 1.0]])
        np.testing.assert_allclose(self.servicio.similitud_coseno(a, b), [1.0, 0.0])


if __name__ == "__main__":
    unittest.main()
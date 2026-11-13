import tempfile
import unittest
import zipfile
from pathlib import Path

from src.services.descarga_dataset_service import DescargaDatasetService


class TestDescargaDatasetService(unittest.TestCase):
    def test_descomprime_el_zip_dentro_del_zip(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            interno = base / "interno.zip"
            with zipfile.ZipFile(interno, "w") as z:
                z.writestr("YT-BB-Dog/train/1/a.jpg", b"x")
                z.writestr("YT-BB-Dog/test/2/b.jpg", b"x")
            externo = base / "externo.zip"
            with zipfile.ZipFile(externo, "w") as z:
                z.write(interno, "YT-BB-dog/YT-BB-Dog.zip")

            servicio = DescargaDatasetService("http://no-se-usa", base / "dataset")
            self.assertFalse(servicio.ya_descargado())
            ruta = servicio.descomprimir(externo)
            self.assertTrue((ruta / "train" / "1" / "a.jpg").exists())
            self.assertTrue(servicio.ya_descargado())


if __name__ == "__main__":
    unittest.main()
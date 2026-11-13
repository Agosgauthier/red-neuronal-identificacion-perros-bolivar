"""RegistroController: registra un perro encontrado y traduce las fallas técnicas."""
from src.domain.errores import ErrorRegistro, ValidacionError
from src.domain.perro_encontrado import PerroEncontrado
from src.services.registro_service import RegistroService


class RegistroController:
    def __init__(self, registro: RegistroService):
        self.registro = registro

    def registrar(self, imagen, zona, fecha, descripcion, contacto) -> PerroEncontrado:
        try:
            return self.registro.registrar(imagen, zona, fecha, descripcion, contacto)
        except ValidacionError:
            raise
        except Exception as error:
            print(f"Error al registrar el perro: {error}")
            raise ErrorRegistro("No se pudieron guardar los datos del perro.") from error
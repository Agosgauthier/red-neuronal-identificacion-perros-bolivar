"""BuscadorService: busca coincidencias para la foto de un perro perdido y compara dos fotos."""
from src import config
from src.domain.coincidencia import Coincidencia
from src.domain.resultado_busqueda import ResultadoBusqueda
from src.domain.resultado_comparacion import ResultadoComparacion
from src.repositories.perros_repository import PerrosRepository
from src.services.galeria_service import GaleriaService
from src.services.modelo_service import ModeloService


class BuscadorService:
    def __init__(self, modelo: ModeloService, galeria: GaleriaService,
                 repositorio: PerrosRepository,
                 umbral: float = config.UMBRAL_COINCIDENCIA,
                 cantidad: int = config.CANTIDAD_RESULTADOS):
        self.modelo = modelo
        self.galeria = galeria
        self.repositorio = repositorio
        self.umbral = umbral
        self.cantidad = cantidad

    def buscar(self, imagen_perdido) -> ResultadoBusqueda:
        candidatos = self.galeria.listar()
        if not candidatos:
            return ResultadoBusqueda(mensaje="No se encontraron fotografías candidatas.")

        resultados = self._puntuar(imagen_perdido, candidatos)
        if not resultados:
            return ResultadoBusqueda(
                mensaje="No se pudieron procesar las fotografías candidatas.")

        resultados.sort(key=lambda c: c.similitud, reverse=True)
        mejor = resultados[0].similitud
        if mejor < self.umbral:
            return ResultadoBusqueda(analizadas=len(resultados), mejor_similitud=mejor)

        top = [c for c in resultados if c.similitud >= self.umbral][: self.cantidad]
        for c in top:
            if self.galeria.es_encontrado(c.ruta):
                c.datos = self.repositorio.obtener_por_imagen(c.ruta.name)
        return ResultadoBusqueda(top, len(resultados), True, mejor)

    def comparar(self, imagen1, imagen2) -> ResultadoComparacion:
        similitud = self.modelo.probabilidad_mismo(imagen1, imagen2)
        return ResultadoComparacion(similitud >= self.umbral, similitud)

    def _puntuar(self, imagen_perdido, candidatos) -> list:
        resultados = []
        for ruta in candidatos:
            try:
                sim = self.modelo.probabilidad_mismo(
                    imagen_perdido, self.modelo.leer_imagen(ruta))
            except Exception as error:  # una foto dañada no frena la búsqueda
                print(f"Error procesando {ruta.name}: {error}")
                continue
            resultados.append(Coincidencia(ruta, sim))
        return resultados
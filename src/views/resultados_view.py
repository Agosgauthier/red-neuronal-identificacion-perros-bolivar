"""ResultadosView: genera el HTML de resultados y mensajes (parte de la Vista)."""
import base64
import html
from pathlib import Path

from src.domain.coincidencia import Coincidencia
from src.domain.resultado_busqueda import ResultadoBusqueda
from src.domain.resultado_comparacion import ResultadoComparacion


class ResultadosView:
    _MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".png": "image/png", ".webp": "image/webp"}

    def imagen_a_data_uri(self, ruta) -> str:
        try:
            ruta = Path(ruta)
            datos = base64.b64encode(ruta.read_bytes()).decode("utf-8")
            return f"data:{self._MIME.get(ruta.suffix.lower(), 'image/jpeg')};base64,{datos}"
        except OSError as error:
            print(f"Error leyendo imagen {Path(ruta).name}: {error}")
            return ""

    def aviso(self, texto: str) -> str:
        return f'<div class="result-message warning">⚠️ {html.escape(texto)}</div>'

    def estado_vacio(self) -> str:
        return (
            '<div class="empty-state"><div class="empty-paw">🐾</div>'
            '<div class="empty-title">Todavía no hay resultados</div>'
            '<div class="empty-text">Cargá una fotografía del perro perdido '
            "y comenzá la búsqueda.</div></div>"
        )

    def resumen(self, r: ResultadoBusqueda) -> str:
        if r.mensaje:
            return self.aviso(r.mensaje)
        if not r.hay_coincidencia:
            return (
                self.aviso("No se encontró una coincidencia suficientemente alta. "
                           f"La mayor similitud encontrada fue de {r.mejor_similitud * 100:.2f}%.")
                + f'<div class="result-count">Se analizaron {r.analizadas} fotografías candidatas.</div>'
            )
        mejor = r.coincidencias[0]
        return (
            '<div class="result-highlight"><div class="highlight-icon">🏆</div>'
            '<div class="highlight-text"><div class="highlight-title">Principal coincidencia</div>'
            f'<div class="highlight-name">{html.escape(mejor.nombre)}</div></div>'
            f'<div class="highlight-score">{mejor.porcentaje:.2f}%</div></div>'
            f'<div class="result-count">Se analizaron {r.analizadas} fotografías candidatas.</div>'
        )

    def tarjetas(self, coincidencias: list, umbral: float) -> str:
        if not coincidencias:
            return self.estado_vacio()
        items = [self._tarjeta(pos, c, umbral) for pos, c in enumerate(coincidencias, start=1)]
        return f'<div class="results-grid">{"".join(items)}</div>'

    def comparacion(self, r: ResultadoComparacion) -> str:
        titulo = "🐕✅ MISMO PERRO" if r.mismo_perro else "🐕❌ PERROS DIFERENTES"
        return f"{titulo}\n\nSimilitud: {r.porcentaje:.2f}%"

    def _tarjeta(self, pos: int, c: Coincidencia, umbral: float) -> str:
        nombre = html.escape(c.nombre)
        if c.similitud >= umbral:
            nivel_clase, nivel_texto = "medium", "Posible coincidencia"
        else:
            nivel_clase, nivel_texto = "low", "Coincidencia baja"
        return (
            '<div class="candidate-card"><div class="candidate-photo">'
            f'<img src="{self.imagen_a_data_uri(c.ruta)}" alt="{nombre}"/>'
            f'<div class="rank">#{pos}</div></div>'
            '<div class="candidate-content">'
            f'<div class="candidate-status {nivel_clase}">🐾 {nivel_texto}</div>'
            f'<div class="candidate-name">{nombre}</div>'
            f'<div class="candidate-score">{c.porcentaje:.2f}%</div>'
            '<div class="candidate-description">estimación de similitud</div>'
            f"{self._datos_encontrado(c)}</div></div>"
        )

    @staticmethod
    def _datos_encontrado(c: Coincidencia) -> str:
        if not c.datos:
            return ""
        d = c.datos
        return (
            '<div class="found-details">'
            f"<div>📍 <strong>Zona:</strong> {html.escape(d.zona)}</div>"
            f"<div>📅 <strong>Fecha:</strong> {html.escape(d.fecha)}</div>"
            f"<div>📝 <strong>Descripción:</strong> {html.escape(d.descripcion) or 'Sin descripción'}</div>"
            f"<div>📞 <strong>Contacto:</strong> {html.escape(d.contacto)}</div>"
            "</div>"
        )
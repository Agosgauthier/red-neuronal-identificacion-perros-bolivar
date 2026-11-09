"""Genera el HTML de resultados (parte de la Vista)."""
import base64
import html
from pathlib import Path

from src.models.perro import Coincidencia, ResultadoBusqueda

_MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".png": "image/png", ".webp": "image/webp"}


def imagen_a_data_uri(ruta: Path) -> str:
    try:
        datos = base64.b64encode(Path(ruta).read_bytes()).decode("utf-8")
        return f"data:{_MIME.get(Path(ruta).suffix.lower(), 'image/jpeg')};base64,{datos}"
    except OSError as error:
        print(f"Error leyendo imagen {Path(ruta).name}: {error}")
        return ""


def aviso(texto: str) -> str:
    return f'<div class="result-message warning">⚠️ {html.escape(texto)}</div>'


def estado_vacio() -> str:
    return (
        '<div class="empty-state"><div class="empty-paw">🐾</div>'
        '<div class="empty-title">Todavía no hay resultados</div>'
        '<div class="empty-text">Cargá una fotografía del perro perdido '
        "y comenzá la búsqueda.</div></div>"
    )


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


def tarjetas(coincidencias: list, umbral: float) -> str:
    if not coincidencias:
        return estado_vacio()
    items = []
    for pos, c in enumerate(coincidencias, start=1):
        nombre = html.escape(c.ruta.stem.replace("_", " ").title())
        if c.similitud >= umbral:
            nivel_clase, nivel_texto = "medium", "Posible coincidencia"
        else:
            nivel_clase, nivel_texto = "low", "Coincidencia baja"
        items.append(
            '<div class="candidate-card"><div class="candidate-photo">'
            f'<img src="{imagen_a_data_uri(c.ruta)}" alt="{nombre}"/>'
            f'<div class="rank">#{pos}</div></div>'
            '<div class="candidate-content">'
            f'<div class="candidate-status {nivel_clase}">🐾 {nivel_texto}</div>'
            f'<div class="candidate-name">{nombre}</div>'
            f'<div class="candidate-score">{c.porcentaje:.2f}%</div>'
            '<div class="candidate-description">estimación de similitud</div>'
            f"{_datos_encontrado(c)}</div></div>"
        )
    return f'<div class="results-grid">{"".join(items)}</div>'


def resumen(r: ResultadoBusqueda) -> str:
    if r.mensaje:
        return aviso(r.mensaje)
    if not r.hay_coincidencia:
        return (
            aviso("No se encontró una coincidencia suficientemente alta. "
                  f"La mayor similitud encontrada fue de {r.mejor_similitud * 100:.2f}%.")
            + f'<div class="result-count">Se analizaron {r.analizadas} fotografías candidatas.</div>'
        )
    mejor = r.coincidencias[0]
    nombre = html.escape(mejor.ruta.stem.replace("_", " ").title())
    return (
        '<div class="result-highlight"><div class="highlight-icon">🏆</div>'
        '<div class="highlight-text"><div class="highlight-title">Principal coincidencia</div>'
        f'<div class="highlight-name">{nombre}</div></div>'
        f'<div class="highlight-score">{mejor.porcentaje:.2f}%</div></div>'
        f'<div class="result-count">Se analizaron {r.analizadas} fotografías candidatas.</div>'
    )
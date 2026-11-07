"""Vista (la V de MVC): arma la interfaz Gradio. Sin lógica de negocio."""
from src.views import renderizado
from src.views.estilos import CSS

ENCABEZADO = """
<header class="custom-header"><div class="header-inner">
  <div class="brand"><div class="brand-icon">🐾</div><div>
    <h1 class="brand-title">Identificación de Perros en <span>Bolívar</span></h1>
    <div class="brand-subtitle">Buscador de posibles coincidencias</div>
  </div></div>
  <div class="header-message"><strong>Juntos podemos volver a encontrarlos.</strong><br>
  Cada fotografía puede ser una pista.</div>
</div></header>
"""

TITULO_BUSQUEDA = """
<div class="search-title"><div class="search-title-icon">📷</div>
<div>Cargá una fotografía del perro perdido</div></div>
<div class="search-description">Subí una fotografía del perro que estás buscando.
El sistema analizará la imagen y buscará las coincidencias más probables
entre los perros registrados.</div>
"""

TITULO_RESULTADOS = """
<div class="results-heading"><div class="results-heading-icon">🏆</div>
<div>Posibles coincidencias</div></div>
<div class="results-description">Estas son las coincidencias más probables
encontradas entre los perros registrados.</div>
"""

NOTA = """
<div class="info-note"><strong>ℹ️ Importante:</strong> la similitud es una estimación
del modelo y no confirma por sí sola la identidad del perro.</div>
"""

TITULO_REGISTRO = """
<div class="results-heading"><div class="results-heading-icon">🐕</div>
<div>Encontré un perro</div></div>
<div class="results-description">Si encontraste un perro en la calle, podés registrarlo
aunque no seas su dueño. La fotografía quedará disponible para futuras búsquedas.</div>
"""

PIE = """
<div class="project-footer">🐾 <strong>Adopta</strong> &nbsp;•&nbsp; <strong>Cuida</strong>
&nbsp;•&nbsp; <strong>Reencontrá</strong><br>Proyecto académico de Redes Neuronales</div>
"""


class InterfazView:
    def __init__(self, controlador, imagen_decorativa=""):
        self.controlador = controlador
        self.imagen_decorativa = imagen_decorativa

    def _hero(self) -> str:
        return f"""
        <div class="dog-preview">
          <img src="{self.imagen_decorativa}" class="dog-preview-image" alt="Perro candidato"/>
          <div class="dog-preview-overlay"><div class="dog-preview-paw">🐾</div>
          <div class="dog-preview-title">Cada foto puede ser una pista</div>
          <div class="dog-preview-text">La inteligencia artificial ayuda a encontrar
          posibles coincidencias.</div></div></div>"""

    def construir(self):
        import gradio as gr

        with gr.Blocks(
            title="Identificación de Perros en Bolívar", css=CSS,
            theme=gr.themes.Base(primary_hue="cyan", neutral_hue="slate"),
            fill_width=True,
        ) as demo:
            gr.HTML(ENCABEZADO)
            with gr.Column(elem_classes="page-content"):
                with gr.Row(elem_classes="search-panel"):
                    with gr.Column(elem_classes="search-main"):
                        gr.HTML(TITULO_BUSQUEDA)
                        perdido = gr.Image(type="numpy", show_label=False, label="",
                                           elem_id="lost-dog-image", height=500, width="100%")
                    gr.HTML(self._hero())

                boton_buscar = gr.Button("🔎  Buscar coincidencias", variant="primary",
                                         elem_id="search-button")

                with gr.Group(elem_classes="results-panel"):
                    gr.HTML(TITULO_RESULTADOS)
                    resumen = gr.HTML(
                        '<div class="result-message">Cargá una fotografía para comenzar la búsqueda.</div>',
                        elem_id="result-summary")
                    tarjetas = gr.HTML(renderizado.estado_vacio(), elem_id="candidate-results")
                    gr.HTML(NOTA)

                with gr.Group(elem_classes="results-panel"):
                    gr.HTML(TITULO_REGISTRO)
                    foto = gr.Image(type="numpy", label="Fotografía del perro encontrado",
                                    elem_id="found-dog-image", height=350)
                    zona = gr.Textbox(label="¿Dónde lo encontraste?",
                                      placeholder="Ejemplo: Barrio San José, Bolívar")
                    fecha = gr.Textbox(label="¿Cuándo lo encontraste?",
                                       placeholder="Ejemplo: 08/10/2026")
                    descripcion = gr.Textbox(label="Descripción", lines=3,
                                             placeholder="Ejemplo: perro mediano, collar azul, muy tranquilo")
                    contacto = gr.Textbox(label="Medio de contacto",
                                          placeholder="Ejemplo: WhatsApp 2314-123456")
                    boton_registrar = gr.Button("🐕 Registrar perro encontrado", variant="primary")
                    resultado = gr.Textbox(label="Resultado", interactive=False)

                gr.HTML(PIE)

            boton_buscar.click(self.controlador.buscar, inputs=perdido, outputs=[resumen, tarjetas])
            boton_registrar.click(self.controlador.registrar,
                                  inputs=[foto, zona, fecha, descripcion, contacto],
                                  outputs=resultado)
        return demo
from pathlib import Path
import base64
import html

import gradio as gr
import numpy as np
import tensorflow as tf


# --------------------------------------------------
# Capa utilizada por nuestro modelo
# --------------------------------------------------

@tf.keras.utils.register_keras_serializable(package="Perros")
class AbsDifference(tf.keras.layers.Layer):
    def call(self, inputs):
        return tf.abs(inputs[0] - inputs[1])


# --------------------------------------------------
# Rutas del proyecto
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_MODELO = (
    BASE_DIR
    / "model"
    / "modelo_perros_bolivar_final.keras"
)

RUTA_CANDIDATOS = (
    BASE_DIR
    / "data"
    / "candidates"
)


# --------------------------------------------------
# Cargar modelo
# --------------------------------------------------

modelo_final = tf.keras.models.load_model(
    RUTA_MODELO,
    custom_objects={"AbsDifference": AbsDifference},
    safe_mode=False,
    compile=False
)

print("Modelo cargado correctamente.")


# --------------------------------------------------
# Preparar imagen
# --------------------------------------------------

def preparar_imagen(imagen):
    imagen = np.array(imagen)

    if imagen.ndim == 2:
        imagen = np.stack(
            [imagen, imagen, imagen],
            axis=-1
        )

    if imagen.shape[-1] == 4:
        imagen = imagen[:, :, :3]

    imagen = tf.image.resize(
        imagen,
        (128, 128)
    )

    imagen = tf.cast(
        imagen,
        tf.float32
    ) / 255.0

    imagen = tf.expand_dims(
        imagen,
        axis=0
    )

    return imagen


# --------------------------------------------------
# Comparar dos perros
# --------------------------------------------------

def comparar_perros(imagen1, imagen2):

    if imagen1 is None or imagen2 is None:
        return "⚠️ Cargá las dos imágenes."

    imagen1 = preparar_imagen(imagen1)
    imagen2 = preparar_imagen(imagen2)

    prediccion = modelo_final.predict(
        [imagen1, imagen2],
        verbose=0
    )[0][0]

    probabilidad_mismo = float(prediccion)
    probabilidad_diferente = 1 - probabilidad_mismo

    if probabilidad_mismo >= 0.5:
        return (
            "🐕✅ MISMO PERRO\n\n"
            f"Probabilidad de mismo perro: "
            f"{probabilidad_mismo * 100:.2f}%"
        )

    return (
        "🐕❌ PERROS DIFERENTES\n\n"
        f"Probabilidad de perros diferentes: "
        f"{probabilidad_diferente * 100:.2f}%"
    )


# --------------------------------------------------
# Obtener candidatos
# --------------------------------------------------

def obtener_candidatos():

    extensiones_validas = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    if not RUTA_CANDIDATOS.exists():
        return []

    return sorted(
        [
            ruta
            for ruta in RUTA_CANDIDATOS.iterdir()
            if ruta.is_file()
            and ruta.suffix.lower() in extensiones_validas
        ]
    )


# --------------------------------------------------
# Cargar candidato
# --------------------------------------------------

def cargar_candidato(ruta):

    contenido = tf.io.read_file(
        str(ruta)
    )

    imagen = tf.image.decode_image(
        contenido,
        channels=3,
        expand_animations=False
    )

    imagen.set_shape(
        [None, None, 3]
    )

    return imagen.numpy()


# --------------------------------------------------
# Obtener probabilidad
# --------------------------------------------------

def obtener_probabilidad_mismo(imagen1, imagen2):

    imagen1 = preparar_imagen(imagen1)
    imagen2 = preparar_imagen(imagen2)

    prediccion = modelo_final.predict(
        [imagen1, imagen2],
        verbose=0
    )[0][0]

    return float(prediccion)


# --------------------------------------------------
# Convertir imagen a Data URI
# --------------------------------------------------

def imagen_a_data_uri(ruta):

    try:
        extension = ruta.suffix.lower()

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp"
        }

        mime_type = mime_types.get(
            extension,
            "image/jpeg"
        )

        datos = ruta.read_bytes()

        contenido = base64.b64encode(
            datos
        ).decode("utf-8")

        return (
            f"data:{mime_type};base64,"
            f"{contenido}"
        )

    except Exception as error:
        print(
            f"Error leyendo imagen {ruta.name}: {error}"
        )
        return ""


# --------------------------------------------------
# Imagen decorativa
# --------------------------------------------------

def obtener_imagen_decorativa():

    candidatos = obtener_candidatos()

    if not candidatos:
        return ""

    return imagen_a_data_uri(
        candidatos[0]
    )


HERO_IMAGE = obtener_imagen_decorativa()


# --------------------------------------------------
# Generar tarjetas
# --------------------------------------------------

def generar_tarjetas(resultados):

    if not resultados:
        return """
        <div class="empty-state">

            <div class="empty-paw">
                🐾
            </div>

            <div class="empty-title">
                Todavía no hay resultados
            </div>

            <div class="empty-text">
                Cargá una fotografía del perro perdido
                y comenzá la búsqueda.
            </div>

        </div>
        """

    tarjetas = []

    for posicion, resultado in enumerate(
        resultados,
        start=1
    ):

        ruta = resultado["ruta"]

        probabilidad = (
            resultado["probabilidad"] * 100
        )

        nombre = html.escape(
            ruta.stem.replace("_", " ").title()
        )

        imagen = imagen_a_data_uri(
            ruta
        )

        if probabilidad >= 80:
            nivel_clase = "high"
            nivel_texto = "Alta coincidencia"
        elif probabilidad >= 60:
            nivel_clase = "medium"
            nivel_texto = "Posible coincidencia"
        else:
            nivel_clase = "low"
            nivel_texto = "Coincidencia baja"

        tarjeta = f"""
        <div class="candidate-card">

            <div class="candidate-photo">

                <img
                    src="{imagen}"
                    alt="{nombre}"
                />

                <div class="rank">
                    #{posicion}
                </div>

            </div>

            <div class="candidate-content">

                <div class="candidate-status {nivel_clase}">
                    🐾 {nivel_texto}
                </div>

                <div class="candidate-name">
                    {nombre}
                </div>

                <div class="candidate-score">
                    {probabilidad:.2f}%
                </div>

                <div class="candidate-description">
                    estimación de similitud
                </div>

            </div>

        </div>
        """

        tarjetas.append(
            tarjeta
        )

    return f"""
    <div class="results-grid">
        {''.join(tarjetas)}
    </div>
    """


# --------------------------------------------------
# Buscar coincidencias
# --------------------------------------------------

def buscar_coincidencias(imagen_perdido):

    if imagen_perdido is None:

        return (
            """
            <div class="result-message warning">
                ⚠️ Primero cargá una fotografía del perro perdido.
            </div>
            """,
            generar_tarjetas([])
        )

    candidatos = obtener_candidatos()

    if not candidatos:

        return (
            """
            <div class="result-message warning">
                ⚠️ No se encontraron fotografías candidatas.
            </div>
            """,
            generar_tarjetas([])
        )

    resultados = []

    for ruta in candidatos:

        try:

            imagen_candidato = cargar_candidato(
                ruta
            )

            probabilidad = obtener_probabilidad_mismo(
                imagen_perdido,
                imagen_candidato
            )

            resultados.append(
                {
                    "ruta": ruta,
                    "probabilidad": probabilidad
                }
            )

        except Exception as error:

            print(
                f"Error procesando {ruta.name}: {error}"
            )

    if not resultados:

        return (
            """
            <div class="result-message warning">
                ⚠️ No se pudieron procesar las fotografías candidatas.
            </div>
            """,
            generar_tarjetas([])
        )

    resultados.sort(
        key=lambda resultado: resultado["probabilidad"],
        reverse=True
    )

    mejores = resultados[:5]

    mejor = mejores[0]

    mejor_nombre = html.escape(
        mejor["ruta"].stem.replace("_", " ").title()
    )

    mejor_porcentaje = (
        mejor["probabilidad"] * 100
    )

    resumen = f"""
    <div class="result-highlight">

        <div class="highlight-icon">
            🏆
        </div>

        <div class="highlight-text">

            <div class="highlight-title">
                Principal coincidencia
            </div>

            <div class="highlight-name">
                {mejor_nombre}
            </div>

        </div>

        <div class="highlight-score">
            {mejor_porcentaje:.2f}%
        </div>

    </div>

    <div class="result-count">
        Se analizaron {len(resultados)}
        fotografías candidatas.
    </div>
    """

    return (
        resumen,
        generar_tarjetas(mejores)
    )


# --------------------------------------------------
# CSS
# --------------------------------------------------

CSS = """
:root {

    --navy: #071b2d;
    --navy-2: #0a2439;
    --blue: #103651;
    --blue-2: #12415d;

    --cyan: #39d8e6;
    --cyan-dark: #1599b3;
    --cyan-soft: #a0edf2;

    --white: #f3fbff;
    --text: #e7f6fb;
    --muted: #9fc1d1;

    --border: rgba(
        70,
        205,
        221,
        0.30
    );

    --shadow: rgba(
        0,
        0,
        0,
        0.24
    );
}


/* ==================================================
   GENERAL
   ================================================== */

html,
body {

    margin: 0 !important;
    padding: 0 !important;

    width: 100% !important;
    min-height: 100% !important;

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(
                24,
                103,
                139,
                0.34
            ),
            transparent 27%
        ),
        radial-gradient(
            circle at 90% 95%,
            rgba(
                16,
                126,
                135,
                0.17
            ),
            transparent 26%
        ),
        linear-gradient(
            135deg,
            var(--navy),
            var(--navy-2)
        ) !important;

    color: var(--white) !important;
}


/* ==================================================
   GRADIO
   ================================================== */

.gradio-container {

    width: 100% !important;
    max-width: none !important;

    margin: 0 !important;
    padding: 0 !important;

    background: transparent !important;
}

footer {
    display: none !important;
}


/* ==================================================
   HEADER
   ================================================== */

.custom-header {

    width: 100%;

    box-sizing: border-box;

    padding: 27px 2vw;

    background:
        linear-gradient(
            100deg,
            #0b2941,
            #0f3c56 55%,
            #0b4a55
        );

    border-bottom:
        1px solid
        rgba(
            68,
            202,
            218,
            0.25
        );

    position: relative;

    overflow: hidden;
}

.custom-header::after {

    content: "";

    position: absolute;

    right: -95px;
    top: -170px;

    width: 330px;
    height: 330px;

    border-radius: 50%;

    background:
        rgba(
            44,
            216,
            230,
            0.07
        );
}

.header-inner {

    width: 96%;

    max-width: 1600px;

    margin: 0 auto;

    display: flex;

    justify-content: space-between;

    align-items: center;

    position: relative;

    z-index: 1;
}

.brand {

    display: flex;

    align-items: center;

    gap: 16px;
}

.brand-icon {

    width: 56px;
    height: 56px;

    border-radius: 17px;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        rgba(
            44,
            215,
            229,
            0.12
        );

    border:
        1px solid
        rgba(
            80,
            220,
            231,
            0.34
        );

    font-size: 29px;
}

.brand-title {

    margin: 0;

    font-size: clamp(
        29px,
        3.1vw,
        44px
    );

    line-height: 1.05;

    font-weight: 850;

    color: var(--white);
}

.brand-title span {

    color: var(--cyan);
}

.brand-subtitle {

    margin-top: 8px;

    color: var(--cyan-soft);

    font-size: 16px;
}

.header-message {

    max-width: 240px;

    text-align: right;

    color: var(--muted);

    font-size: 14px;

    line-height: 1.55;
}

.header-message strong {

    color: var(--cyan-soft);
}


/* ==================================================
   CONTENIDO
   ================================================== */

.page-content {

    width: 96%;

    max-width: 1600px;

    margin: 0 auto;

    padding: 30px 0 42px;
}


/* ==================================================
   PANEL DE BÚSQUEDA
   ================================================== */

.search-panel {

    width: 100%;

    box-sizing: border-box;

    display: grid;

    grid-template-columns:
        minmax(0, 1.55fr)
        minmax(300px, 0.75fr);

    gap: 26px;

    padding: 27px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(
                18,
                57,
                83,
                0.98
            ),
            rgba(
                10,
                40,
                62,
                0.98
            )
        );

    border:
        1px solid var(--border);

    box-shadow:
        0 18px 38px var(--shadow);

    margin-bottom: 22px;
}

.search-main {

    min-width: 0;
}

.search-title {

    display: flex;

    align-items: center;

    gap: 12px;

    color: var(--white);

    font-size: 25px;

    font-weight: 800;

    margin-bottom: 8px;
}

.search-title-icon {

    width: 45px;
    height: 45px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background:
        rgba(
            54,
            214,
            229,
            0.12
        );

    border:
        1px solid
        rgba(
            75,
            216,
            230,
            0.28
        );

    font-size: 21px;
}

.search-description {

    color: var(--muted);

    font-size: 14px;

    line-height: 1.55;

    margin-bottom: 18px;
}


/* ==================================================
   UPLOAD
   ================================================== */

#lost-dog-image {

    width: 100% !important;

    min-width: 0 !important;
}

#lost-dog-image .wrap {

    min-height: 330px !important;

    width: 100% !important;

    box-sizing: border-box !important;

    border-radius: 19px !important;

    border:
        2px dashed
        rgba(
            65,
            206,
            224,
            0.58
        ) !important;

    background:
        linear-gradient(
            145deg,
            #0c2940,
            #10384f
        ) !important;

    transition:
        0.2s ease !important;
}

#lost-dog-image .wrap:hover {

    border-color:
        var(--cyan) !important;

    background:
        linear-gradient(
            145deg,
            #10354d,
            #124158
        ) !important;
}


/* ==================================================
   IMAGEN DECORATIVA
   ================================================== */

.dog-preview {

    min-height: 330px;

    border-radius: 20px;

    overflow: hidden;

    position: relative;

    background:
        linear-gradient(
            180deg,
            rgba(
                16,
                63,
                86,
                0.72
            ),
            rgba(
                7,
                29,
                44,
                0.98
            )
        );

    border:
        1px solid
        rgba(
            73,
            194,
            211,
            0.25
        );
}

.dog-preview-image {

    width: 100%;

    height: 100%;

    min-height: 330px;

    object-fit: cover;

    display: block;

    opacity: 0.84;
}

.dog-preview-overlay {

    position: absolute;

    inset: 0;

    display: flex;

    flex-direction: column;

    justify-content: flex-end;

    padding: 22px;

    background:
        linear-gradient(
            180deg,
            transparent 35%,
            rgba(
                4,
                22,
                35,
                0.90
            )
        );
}

.dog-preview-paw {

    font-size: 31px;

    margin-bottom: 5px;
}

.dog-preview-title {

    color: var(--white);

    font-size: 19px;

    font-weight: 800;
}

.dog-preview-text {

    margin-top: 6px;

    color: var(--cyan-soft);

    font-size: 13px;

    line-height: 1.4;
}


/* ==================================================
   BOTÓN
   ================================================== */

#search-button {

    width: 100% !important;

    min-height: 60px !important;

    margin:
        0 0 25px 0 !important;

    border-radius: 17px !important;

    border:
        1px solid
        rgba(
            108,
            235,
            239,
            0.76
        ) !important;

    background:
        linear-gradient(
            90deg,
            #167ea2,
            #20aec3,
            #31d0d9
        ) !important;

    color: white !important;

    font-size: 18px !important;

    font-weight: 800 !important;

    box-shadow:
        0 10px 24px
        rgba(
            25,
            193,
            212,
            0.20
        ) !important;

    transition:
        transform 0.18s ease,
        filter 0.18s ease !important;
}

#search-button:hover {

    transform:
        translateY(-2px) !important;

    filter:
        brightness(1.06) !important;
}


/* ==================================================
   RESULTADOS
   ================================================== */

.results-panel {

    width: 100%;

    box-sizing: border-box;

    padding: 27px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(
                17,
                54,
                79,
                0.98
            ),
            rgba(
                10,
                39,
                59,
                0.98
            )
        );

    border:
        1px solid var(--border);

    box-shadow:
        0 16px 34px var(--shadow);
}

.results-heading {

    display: flex;

    align-items: center;

    gap: 12px;

    margin-bottom: 7px;

    color: var(--white);

    font-size: 24px;

    font-weight: 800;
}

.results-heading-icon {

    width: 45px;
    height: 45px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background:
        rgba(
            54,
            214,
            229,
            0.12
        );

    border:
        1px solid
        rgba(
            75,
            216,
            230,
            0.28
        );

    font-size: 21px;
}

.results-description {

    color: var(--muted);

    font-size: 14px;

    line-height: 1.5;

    margin-bottom: 17px;
}


/* ==================================================
   RESUMEN
   ================================================== */

#result-summary {

    width: 100% !important;

    margin-bottom: 16px !important;
}

.result-highlight {

    display: flex;

    align-items: center;

    gap: 13px;

    width: 100%;

    box-sizing: border-box;

    padding: 13px 16px;

    border-radius: 15px;

    background:
        rgba(
            8,
            34,
            51,
            0.66
        );

    border:
        1px solid
        rgba(
            76,
            207,
            220,
            0.22
        );
}

.highlight-icon {

    font-size: 25px;
}

.highlight-title {

    color: var(--muted);

    font-size: 11px;

    text-transform: uppercase;

    letter-spacing: 0.5px;
}

.highlight-name {

    margin-top: 2px;

    color: var(--white);

    font-size: 17px;

    font-weight: 800;
}

.highlight-text {

    flex: 1;
}

.highlight-score {

    color: var(--cyan);

    font-size: 23px;

    font-weight: 850;
}

.result-count {

    margin-top: 9px;

    color: #81a9bb;

    font-size: 12px;
}


/* ==================================================
   MENSAJE
   ================================================== */

.result-message {

    width: 100%;

    box-sizing: border-box;

    padding: 14px 16px;

    border-radius: 14px;

    color: var(--muted);

    background:
        rgba(
            8,
            32,
            49,
            0.48
        );

    border:
        1px dashed
        rgba(
            74,
            191,
            207,
            0.24
        );
}

.result-message.warning {

    color: var(--cyan-soft);

    border-left:
        3px solid
        var(--cyan);
}


/* ==================================================
   TARJETAS DE CANDIDATOS
   ================================================== */

#candidate-results {

    width: 100% !important;
}

.results-grid {

    width: 100%;

    display: grid;

    grid-template-columns:
        repeat(
            5,
            minmax(
                0,
                1fr
            )
        );

    gap: 17px;
}

.candidate-card {

    min-width: 0;

    overflow: hidden;

    border-radius: 18px;

    background:
        linear-gradient(
            160deg,
            #123d58,
            #0b2c43
        );

    border:
        1px solid
        rgba(
            65,
            191,
            210,
            0.35
        );

    box-shadow:
        0 9px 20px
        rgba(
            0,
            0,
            0,
            0.18
        );

    transition:
        transform 0.18s ease,
        border-color 0.18s ease;
}

.candidate-card:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(
            68,
            219,
            230,
            0.70
        );
}

.candidate-photo {

    position: relative;

    width: 100%;

    aspect-ratio: 1 / 1;

    overflow: hidden;

    background:
        #082135;
}

.candidate-photo img {

    width: 100%;

    height: 100%;

    object-fit: cover;

    display: block;
}

.rank {

    position: absolute;

    top: 9px;
    left: 9px;

    padding: 6px 9px;

    border-radius: 9px;

    color: white;

    font-size: 12px;

    font-weight: 800;

    background:
        rgba(
            5,
            27,
            42,
            0.82
        );

    border:
        1px solid
        rgba(
            86,
            218,
            229,
            0.45
        );
}

.candidate-content {

    padding: 14px;
}

.candidate-status {

    display: inline-block;

    padding: 6px 9px;

    border-radius: 9px;

    margin-bottom: 10px;

    font-size: 10px;

    font-weight: 750;
}

.candidate-status.high {

    color: #073c38;

    background:
        #5fe1bf;
}

.candidate-status.medium {

    color: #083c42;

    background:
        #70dae0;
}

.candidate-status.low {

    color: #bfe6eb;

    background:
        rgba(
            43,
            113,
            130,
            0.48
        );
}

.candidate-name {

    color: var(--white);

    font-size: 15px;

    font-weight: 800;

    margin-bottom: 9px;
}

.candidate-score {

    color: var(--cyan);

    font-size: 24px;

    font-weight: 850;

    line-height: 1;
}

.candidate-description {

    margin-top: 5px;

    color: #7fa7b8;

    font-size: 10px;
}


/* ==================================================
   ESTADO VACÍO
   ================================================== */

.empty-state {

    width: 100%;

    box-sizing: border-box;

    padding: 30px 20px;

    border-radius: 17px;

    text-align: center;

    border:
        1px dashed
        rgba(
            65,
            192,
            210,
            0.28
        );

    background:
        rgba(
            8,
            31,
            47,
            0.35
        );
}

.empty-paw {

    font-size: 28px;

    margin-bottom: 8px;
}

.empty-title {

    color: var(--white);

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 5px;
}

.empty-text {

    color: var(--muted);

    font-size: 13px;
}


/* ==================================================
   AVISO
   ================================================== */

.info-note {

    margin-top: 20px;

    padding: 15px 17px;

    border-radius: 13px;

    border-left: 3px solid
        var(--cyan);

    background:
        rgba(
            8,
            34,
            51,
            0.72
        );

    color: var(--muted);

    font-size: 13px;

    line-height: 1.5;
}


/* ==================================================
   FOOTER
   ================================================== */

.project-footer {

    padding-top: 22px;

    text-align: center;

    color: #749aaa;

    font-size: 12px;

    line-height: 1.7;
}

.project-footer strong {

    color: var(--cyan-soft);
}


/* ==================================================
   RESPONSIVE
   ================================================== */

@media (max-width: 1050px) {

    .search-panel {

        grid-template-columns:
            1fr;
    }

    .dog-preview {

        min-height: 260px;
    }

    .dog-preview-image {

        min-height: 260px;
    }

    .results-grid {

        grid-template-columns:
            repeat(
                3,
                minmax(
                    0,
                    1fr
                )
            );
    }
}

@media (max-width: 760px) {

    .page-content {

        width: 94%;
    }

    .custom-header {

        padding:
            22px 3vw;
    }

    .header-inner {

        width: 94%;
    }

    .header-message {

        display: none;
    }

    .brand-title {

        font-size: 29px;
    }

    .search-panel,
    .results-panel {

        padding: 20px;
    }

    .results-grid {

        grid-template-columns:
            repeat(
                2,
                minmax(
                    0,
                    1fr
                )
            );
    }
}

@media (max-width: 520px) {

    .brand-icon {

        width: 46px;
        height: 46px;
    }

    .brand-title {

        font-size: 24px;
    }

    .brand-subtitle {

        font-size: 13px;
    }

    .results-grid {

        grid-template-columns:
            1fr;
    }
}
"""


# --------------------------------------------------
# Interfaz
# --------------------------------------------------

with gr.Blocks(
    title="Identificación de Perros en Bolívar",
    css=CSS,
    theme=gr.themes.Base(
        primary_hue="cyan",
        neutral_hue="slate"
    ),
    fill_width=True
) as demo:

    # ----------------------------------------------
    # Header
    # ----------------------------------------------

    gr.HTML(
        f"""
        <header class="custom-header">

            <div class="header-inner">

                <div class="brand">

                    <div class="brand-icon">
                        🐾
                    </div>

                    <div>

                        <h1 class="brand-title">
                            Identificación de Perros en
                            <span>Bolívar</span>
                        </h1>

                        <div class="brand-subtitle">
                            Buscador de posibles coincidencias
                        </div>

                    </div>

                </div>

                <div class="header-message">
                    <strong>
                        Juntos podemos volver a encontrarlos.
                    </strong>
                    <br>
                    Cada fotografía puede ser una pista.
                </div>

            </div>

        </header>
        """
    )


    # ----------------------------------------------
    # Contenido
    # ----------------------------------------------

    with gr.Column(
        elem_classes="page-content"
    ):

        # ------------------------------------------
        # Panel de búsqueda
        # ------------------------------------------

        with gr.Row(
            elem_classes="search-panel"
        ):

            with gr.Column(
                elem_classes="search-main"
            ):

                gr.HTML(
                    """
                    <div class="search-title">

                        <div class="search-title-icon">
                            📷
                        </div>

                        <div>
                            Cargá una fotografía del perro perdido
                        </div>

                    </div>

                    <div class="search-description">
                        Subí una fotografía del perro que estás buscando.
                        El sistema analizará la imagen y buscará las
                        coincidencias más probables entre los perros registrados.
                    </div>
                    """
                )

                imagen_perdido = gr.Image(
                    type="numpy",
                    show_label=False,
                    label="",
                    elem_id="lost-dog-image"
                )


            # Imagen decorativa
            gr.HTML(
                f"""
                <div class="dog-preview">

                    <img
                        src="{HERO_IMAGE}"
                        class="dog-preview-image"
                        alt="Perro candidato"
                    />

                    <div class="dog-preview-overlay">

                        <div class="dog-preview-paw">
                            🐾
                        </div>

                        <div class="dog-preview-title">
                            Cada foto puede ser una pista
                        </div>

                        <div class="dog-preview-text">
                            La inteligencia artificial ayuda
                            a encontrar posibles coincidencias.
                        </div>

                    </div>

                </div>
                """
            )


        # ------------------------------------------
        # Botón
        # ------------------------------------------

        boton_buscar = gr.Button(
            "🔎  Buscar coincidencias",
            variant="primary",
            elem_id="search-button"
        )


        # ------------------------------------------
        # Resultados
        # ------------------------------------------

        with gr.Group(
            elem_classes="results-panel"
        ):

            gr.HTML(
                """
                <div class="results-heading">

                    <div class="results-heading-icon">
                        🏆
                    </div>

                    <div>
                        Posibles coincidencias
                    </div>

                </div>

                <div class="results-description">
                    Estas son las coincidencias más probables
                    encontradas entre los perros registrados.
                </div>
                """
            )

            resultado_resumen = gr.HTML(
                value="""
                <div class="result-message">
                    Cargá una fotografía para comenzar la búsqueda.
                </div>
                """,
                elem_id="result-summary"
            )

            resultado_tarjetas = gr.HTML(
                value=generar_tarjetas([]),
                elem_id="candidate-results"
            )

            gr.HTML(
                """
                <div class="info-note">
                    <strong>ℹ️ Importante:</strong>
                    la probabilidad es una estimación del modelo
                    y no confirma por sí sola la identidad del perro.
                </div>
                """
            )


        # ------------------------------------------
        # Footer
        # ------------------------------------------

        gr.HTML(
            """
            <div class="project-footer">

                🐾
                <strong>Adopta</strong>
                &nbsp;•&nbsp;
                <strong>Cuida</strong>
                &nbsp;•&nbsp;
                <strong>Reencontrá</strong>

                <br>

                Proyecto académico de Redes Neuronales

            </div>
            """
        )


    # ----------------------------------------------
    # Evento de búsqueda
    # ----------------------------------------------

    boton_buscar.click(
        fn=buscar_coincidencias,
        inputs=imagen_perdido,
        outputs=[
            resultado_resumen,
            resultado_tarjetas
        ]
    )


# --------------------------------------------------
# Ejecutar
# --------------------------------------------------

if __name__ == "__main__":
    demo.launch()
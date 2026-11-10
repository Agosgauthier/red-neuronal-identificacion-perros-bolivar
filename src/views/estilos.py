"""Estilos de la interfaz (vista)."""

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

    height: 500px !important;
}

#lost-dog-image .wrap {

    width: 100% !important;

    height: 500px !important;

    min-height: 500px !important;

    max-height: 500px !important;

    box-sizing: border-box !important;

    border-radius: 19px !important;

    overflow: hidden !important;

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
}

#lost-dog-image .image-container {

    width: 100% !important;

    height: 100% !important;

    min-height: 0 !important;

    max-height: none !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#lost-dog-image .image-frame {

    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    min-height: 0 !important;

    max-width: none !important;

    max-height: none !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#lost-dog-image .upload-container {

    width: 100% !important;

    height: 100% !important;

    min-height: 0 !important;

    max-height: none !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#lost-dog-image img {

    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    min-height: 0 !important;

    object-fit: contain !important;

    object-position: center !important;

    display: block !important;

}

#found-dog-image {

    width: 100% !important;

    height: 350px !important;
}

#found-dog-image .wrap {

    width: 100% !important;

    height: 350px !important;

    min-height: 350px !important;

    max-height: 350px !important;

    box-sizing: border-box !important;

    border-radius: 19px !important;

    overflow: hidden !important;

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
}

#found-dog-image .image-container {

    width: 100% !important;

    height: 100% !important;

    min-height: 0 !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#found-dog-image .image-frame {

    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    min-height: 0 !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#found-dog-image .upload-container {

    width: 100% !important;

    height: 100% !important;

    min-height: 0 !important;

    padding: 0 !important;

    margin: 0 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    overflow: hidden !important;
}

#found-dog-image img {

    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    min-height: 0 !important;

    object-fit: contain !important;

    object-position: center !important;

    display: block !important;
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

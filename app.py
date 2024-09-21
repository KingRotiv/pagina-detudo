import streamlit as st


# Página inicial
inicio = st.Page("pages/inicio.py", title="Início", icon="👋", default=True)

# Páginas de imagem
converter_imagem = st.Page("pages/converter_imagem.py", title="Converter imagem", icon="📸")
inspecionar_imagem = st.Page("pages/inspecionar_imagem.py", title="Inspecionar imagem", icon="📸")

# Páginas de áudio
converter_audio = st.Page("pages/converter_audio.py", title="Converter áudio", icon="🎵")

# Página de curriculo
gerar_curriculo = st.Page("pages/gerar_curriculo.py", title="Gerar Currículo", icon="📄")

pg = st.navigation({
    "Menu": [inicio],
    "Imagem": [
        converter_imagem,
        inspecionar_imagem
    ],
    "Áudio": [converter_audio],
    "Currículo": [gerar_curriculo],
})
pg.run()
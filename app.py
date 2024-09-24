import streamlit as st


# Página inicial
inicio = st.Page("pages/inicio.py", title="Início", icon="👋", default=True)

# Páginas de imagem
converter_imagem = st.Page("pages/converter_imagem.py", title="Converter imagem", icon="📸")
inspecionar_imagem = st.Page("pages/inspecionar_imagem.py", title="Inspecionar imagem", icon="📸")

# Páginas de áudio
converter_audio = st.Page("pages/converter_audio.py", title="Converter áudio", icon="🎵")

# Páginas de vídeo
converter_video = st.Page("pages/converter_video.py", title="Converter video", icon="🎥")

# Páginas de currículo
gerar_curriculo = st.Page("pages/gerar_curriculo.py", title="Gerar Currículo", icon="📄")

# Páginas de localização
ip_geolocazacao = st.Page("pages/ip_geolocalizacao.py", title="IP Geolocalização", icon="🌎")

pg = st.navigation({
    "Menu": [inicio],
    "Imagem": [
        converter_imagem,
        inspecionar_imagem
    ],
    "Áudio": [converter_audio],
    "Vídeo": [converter_video],
    "Currículo": [gerar_curriculo],
    "Localização": [ip_geolocazacao],
})
pg.run()
from io import BytesIO
import streamlit as st
import exifread


# Informação da página
st.header("Inspecionar imagem")
st.write("Inspecione os metadados da imagem.")

# Página
imagem = st.file_uploader("Escolha uma imagem", type=["png", "jpeg", "jpg"])
if imagem:
    imagem_bytes = BytesIO(imagem.read())

    # Exibir a imagem carregada
    st.image(imagem_bytes)

    # Ler os metadados EXIF
    exif = exifread.process_file(imagem_bytes)

    # Mostrar os metadados EXIF na interface
    if exif:
        st.subheader("Metadados EXIF")
        st.write(exif)
    else:
        st.write("Nenhum dado EXIF encontrado.")

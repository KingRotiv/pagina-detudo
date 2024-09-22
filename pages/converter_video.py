import os
import tempfile
from io import BytesIO

import streamlit as st
from loguru import logger
from moviepy.editor import VideoFileClip

# Informação da página
st.header("Converter vídeo")
st.write("Converta vídeo com rapidez e qualidade.")


def converter_video() -> None:
    if f"video/{converter_para}" == video.type:
        st.toast(
            "Escolha um formato diferente do original para converter.",
            icon="❌",
        )
        return None

    try:
        botao_converter.status("Convertendo o vídeo...")
        botao_baixar_novo_video.empty()

        # Cria um arquivo temporário para salvar o vídeo enviado
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{video.name.rsplit('.', 1)[1]}"
        ) as temp_file:
            temp_file.write(video.read())
            temp_video_path = temp_file.name

        # Carrega o vídeo a partir do arquivo temporário
        video_clip = VideoFileClip(temp_video_path)

        # Cria um novo arquivo temporário para o vídeo convertido
        novo_nome = f"{video.name.rsplit('.', 1)[0]}.{converter_para}"
        novo_video_bytes = BytesIO()

        # Exporta o vídeo para o novo formato e grava temporariamente
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{converter_para}"
        ) as temp_output_file:
            video_clip.write_videofile(
                temp_output_file.name,
                codec="libx264" if converter_para != "webm" else None,
            )
            video_clip.close()
            temp_output_file.seek(0)
            novo_video_bytes.write(temp_output_file.read())

        novo_video_bytes.seek(0)
        novo_formato = f"video/{converter_para}"

        # Botão de download para o vídeo convertido
        st.session_state["converter_video.botao_baixar_novo_video"] = (
            lambda: st.download_button(
                f"Baixar vídeo {converter_para}",
                data=novo_video_bytes.getvalue(),
                file_name=novo_nome,
                mime=novo_formato,
            )
        )
        st.toast(f"Vídeo convertido para {converter_para}.", icon="✅")

        if os.path.exists(temp_video_path):
            logger.debug(f"Excluindo o arquivo temporário: {temp_video_path}")
            os.remove(temp_video_path)
        if os.path.exists(temp_output_file.name):
            logger.debug(f"Excluindo o arquivo temporário: {temp_output_file.name}")
            os.remove(temp_output_file.name)

    except Exception as ex:
        logger.error(ex)
        st.toast(
            "Ocorreu um erro ao converter o vídeo. Tente novamente.",
            icon="❌",
        )


# Opções de formatos de conversão de vídeo
opcoes_conversao = [
    "mp4",
    "avi",
    "mkv",
    "mov",
    "webm",
]

# Página
video = st.file_uploader("Escolha um vídeo", type=opcoes_conversao)
if video:
    st.video(video, format=video.type)
converter_para = st.selectbox(
    "Converter para", options=opcoes_conversao, disabled=not video
)
botao_converter = st.empty()
botao_converter.button("Converter vídeo", on_click=converter_video, disabled=not video)
botao_baixar_novo_video = st.empty()
if _botao_baixar_novo_video := st.session_state.get(
    "converter_video.botao_baixar_novo_video"
):
    with botao_baixar_novo_video.container():
        _botao_baixar_novo_video()

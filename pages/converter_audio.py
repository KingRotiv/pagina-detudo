from io import BytesIO

import streamlit as st
from loguru import logger
from pydub import AudioSegment


# Informação da página
st.header("Converter áudio")
st.write("Converta áudio com rapidez e qualidade.")


def converter_audio() -> None:
    if f"audio/{converter_para}" == audio.type:
        st.toast(
            "Escolha um formato diferente do original para converter.",
            icon="❌",
        )
        return None
    try:
        botao_converter.status("Convertendo áudio...")
        botao_baixar_novo_audio.empty()

        audio_segment = AudioSegment.from_file(audio)
        novo_audio_bytes = BytesIO()
        audio_segment.export(novo_audio_bytes, format=converter_para)
        novo_audio_bytes.seek(0)  # Reseta o ponteiro

        novo_nome = f"{audio.name.rsplit('.', 1)[0]}.{converter_para}"
        novo_formato = f"audio/{converter_para}"
        st.session_state["converter_audio.botao_baixar_novo_audio"] = (
            lambda: st.download_button(
                f"Baixar áudio {converter_para}",
                data=novo_audio_bytes.getvalue(),
                file_name=novo_nome,
                mime=novo_formato,
            )
        )
        st.toast(f"Aúdio convertido para {converter_para}.", icon="✅")
    except Exception as ex:
        logger.error(ex)
        st.toast(
            f"Ocorreu um erro ao converter o aúdio. Tente novamente.",
            icon="❌",
        )


opcoes_conversao = [
    "ac3",
    "aiff",
    "flac",
    "mp3",
    "ogg",
    "opus",
    "wav",
]


# Página
audio = st.file_uploader("Escolha um áudio", type=opcoes_conversao)
if audio:
    st.audio(audio, format=audio.type)
converter_para = st.selectbox(
    "Converter para", options=opcoes_conversao, disabled=not audio
)
botao_converter = st.empty()
botao_converter.button("Converter áudio", on_click=converter_audio, disabled=not audio)
botao_baixar_novo_audio = st.empty()
if _botao_baixar_novo_audio := st.session_state.get(
    "converter_audio.botao_baixar_novo_audio"
):
    with botao_baixar_novo_audio.container():
        _botao_baixar_novo_audio()

from io import BytesIO

import streamlit as st
from loguru import logger
from PIL import Image


# Informação da página
st.header("Converter imagem")
st.write("Converta imagem com rapidez e qualidade.")


def converter_imagem() -> None:
    if f"image/{converter_para}" == imagem.type:
        st.toast(
            "Escolha um formato diferente do original para converter.",
            icon="❌",
        )
        return None
    try:
        botao_converter.status("Convertendo imagem...")
        botao_baixar_nova_imagem.empty()

        with Image.open(imagem) as i:
            # Se a imagem tiver um canal alfa, converta para RGB antes de salvar em JPEG
            if converter_para == "jpeg" and i.mode == "RGBA":
                i = i.convert("RGB")

            nova_imagem_bytes = BytesIO()
            i.save(nova_imagem_bytes, format=converter_para)
            nova_imagem_bytes.seek(0)  # Reseta o ponteiro

            novo_nome = f"{imagem.name.rsplit('.', 1)[0]}.{converter_para}"
            novo_formato = f"image/{converter_para}"
            st.session_state["converter_imagem.botao_baixar_nova_imagem"] = (
                lambda: st.download_button(
                    f"Baixar imagem {converter_para}",
                    data=nova_imagem_bytes.getvalue(),
                    file_name=novo_nome,
                    mime=novo_formato,
                )
            )
            st.toast(f"Imagem convertida para {converter_para}.", icon="✅")
    except Exception as ex:
        logger.error(ex)
        st.toast(
            "Ocorreu um erro ao converter a imagem. Tente novamente.",
            icon="❌",
        )


opcoes_conversao = ["jpeg", "png", "bmp", "webp"]

# Página
imagem = st.file_uploader("Escolha uma imagem", type=opcoes_conversao)
if imagem:
    st.image(imagem, use_column_width=True)
converter_para = st.selectbox(
    "Converter para", options=opcoes_conversao, disabled=not imagem
)
botao_converter = st.empty()
botao_converter.button(
    "Converter imagem", on_click=converter_imagem, disabled=not imagem
)
botao_baixar_nova_imagem = st.empty()
if _botao_baixar_nova_imagem := st.session_state.get(
    "converter_imagem.botao_baixar_nova_imagem"
):
    with botao_baixar_nova_imagem.container():
        _botao_baixar_nova_imagem()

from io import BytesIO

import streamlit as st
from PIL import Image


# Informação da página
st.header("Converter imagem")
st.write("Converta imagens com rapidez e qualidade.")


def converter_imagem() -> None:
    if f"image/{converter_para}" == imagem.type:
        st.toast(
            "Escolha um formato diferente do original para converter.",
            icon="❌",
        )
        return None
    try:
        imagem_bytes = BytesIO(imagem.read())
        with Image.open(imagem_bytes) as i:
            # Se a imagem tiver um canal alfa, converta para RGB antes de salvar em JPEG
            if converter_para == "jpeg" and i.mode == "RGBA":
                i = i.convert("RGB")

            nova_imagem_bytes = BytesIO()
            i.save(nova_imagem_bytes, format=converter_para)
            nova_imagem_bytes.seek(0)  # Reseta o ponteiro

            novo_nome = f"{imagem.name.rsplit('.', 1)[0]}.{converter_para}"
            novo_formato = f"image/{converter_para}"
            placeholder_botao_baixar_nova_imagem.download_button(
                f"Baixar imagem {converter_para}",
                data=nova_imagem_bytes.getvalue(),
                file_name=novo_nome,
                mime=novo_formato,
                key="converter_imagem.botao_baixar_nova_imagem",
            )
            st.toast(f"Imagem convertida para {converter_para}.", icon="✅")
    except Exception:
        st.toast(
            "Ocorreu um erro ao converter a imagem. Tente novamente.",
            icon="❌",
        )


opcoes_conversao = ["jpeg", "png", "bmp", "webp"]

# Página
imagem = st.file_uploader("Escolha uma imagem", type=opcoes_conversao)
converter_para = st.selectbox(
    "Converter para", options=opcoes_conversao, disabled=not imagem
)
botao_converter = st.button(
    "Converter imagem", on_click=converter_imagem, disabled=not imagem
)
if st.session_state.get("converter_imagem.botao_baixar_nova_imagem") is None:
    placeholder_botao_baixar_nova_imagem = st.empty()

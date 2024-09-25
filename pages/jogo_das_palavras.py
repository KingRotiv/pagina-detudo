from random import choice
from typing import Literal
from glob import glob

import streamlit as st
from streamlit_extras.tags import tagger_component
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from loguru import logger
from unidecode import unidecode
from pydantic import BaseModel
from mimesis import Generic
from mimesis.locales import Locale


class LetraDigitada(BaseModel):
    letra: str
    acertou: bool
    automatico: bool = False


class LetrasDigitadas(BaseModel):
    letras_digitadas: list[LetraDigitada]

    @property
    def lista_letras(self) -> list[str]:
        """
        Retorna uma lista contendo todas as letras digitadas.

        Returns:
            list[str]: Lista contendo todas as letras digitadas.
        """
        l = [letra.letra for letra in self.letras_digitadas]
        return l
    
    @property
    def cores_letras(self) -> list[str]:
        """
        Retorna uma lista contendo as cores das letras digitadas.

        Returns:
            list[str]: Lista contendo as cores das letras digitadas.
        """
        l = ["green" if letra.acertou else "red" for letra in self.letras_digitadas]
        return l
    
    def add(self, letra: LetraDigitada) -> None:
        """
        Adiciona uma letra na lista de letras digitadas.

        Params:
            letra (LetraDigitada): Objeto da classe LetraDigitada.
        """
        self.letras_digitadas.append(letra)


class PalavraEscolhida(BaseModel):
    palavra: str
    tipo: str
    subtipo: str
    dica: str

    @property
    def quantidade_letras(self) -> int:
        """
        Retorna a quantidade de letras da palavra.

        Returns:
            int: Quantidade de letras da palavra.
        """
        return len(self.palavra)

    def existe_letra(self, letra: str) -> bool:
        """
        Verifica se uma letra existe na palavra.

        Params:
            letra (str): Letra a ser verificada.

        Returns:
            bool: True se a letra existir na palavra, False caso contrário.
        """
        letra = unidecode(letra.lower()).lower()
        return letra in self.palavra.lower()

    def mostrar(self, letras: list[str]) -> str:
        """
        Retorna a palavra com as letras descosbertas e '?' para as restantes.

        Params:
            letras (list[str]): Lista de letras digitadas.

        Returns:
            str: Palavra com as letras descobertas.
        """
        letras = list(map(unidecode, letras))
        letras = list(map(lambda x: x.lower(), letras))
        p = [self.palavra[i] if l in letras else "?" for i, l in enumerate(unidecode(self.palavra.lower()))]
        return "".join(p)
    
    def acertou(self, letras: list[str]) -> bool:
        """
        Verifica se a palavra foi descoberta.

        Params:
            letras (list[str]): Lista de letras digitadas.

        Returns:
            bool: True se a palavra foi descoberta, False caso contrário.
        """
        return "?" not in self.mostrar(letras)


def get_palavra_escolhida() -> PalavraEscolhida:
    """
    Seleciona uma palavra aleatória de um dicionário de palavras.

    Returns:
        PalavraEscolhida: Objeto da classe PalavraEscolhida.
    """
    generic = Generic(locale=Locale.PT_BR)
    palavras = [
        # Comida
        PalavraEscolhida(
            palavra=generic.food.fruit(),
            tipo="Comida",
            subtipo="Fruta",
            dica="Talvez você goste dessa fruta.",
        ),
        PalavraEscolhida(
            palavra=generic.food.vegetable(),
            tipo="Comida",
            subtipo="Vegetal",
            dica="Talvez você goste desse vegetal.",
        ),
        PalavraEscolhida(
            palavra=generic.food.dish(),
            tipo="Comida",
            subtipo="Prato",
            dica="Talvez você goste desse prato.",
        ),
        PalavraEscolhida(
            palavra=generic.food.drink(),
            tipo="Comida",
            subtipo="Bebida",
            dica="Talvez você goste dessa bebida.",
        ),
        PalavraEscolhida(
            palavra=generic.food.spices(),
            tipo="Comida",
            subtipo="Tempero",
            dica="Talvez você goste desse tempero.",
        ),
        # Local
        PalavraEscolhida(
            palavra=generic.address.city(),
            tipo="Local",
            subtipo="Cidade",
            dica="Talvez você goste desta cidade.",
        ),
        PalavraEscolhida(
            palavra=generic.address.state(),
            tipo="Local",
            subtipo="Estado",
            dica="Talvez você goste desse estado.",
        ),
        PalavraEscolhida(
            palavra=generic.address.country(),
            tipo="Local",
            subtipo="País",
            dica="Talvez você goste desse país.",
        ),
        # Data
        PalavraEscolhida(
            palavra=generic.datetime.day_of_week(),
            tipo="Data",
            subtipo="Dia da semana",
            dica="Talvez você goste desse dia da semana.",
        ),
        PalavraEscolhida(
            palavra=generic.datetime.month(),
            tipo="Data",
            subtipo="Mês",
            dica="Talvez você goste desse mês.",
        ),
    ]
    return choice(palavras)


LETRAS_AUTOMATICAS = [" ", "-", ".", "/"]
TAMANHO_LETRAS_AUTOMATICAS = len(LETRAS_AUTOMATICAS)

def iniciar() -> None:
    """
    Inicializa as variáveis de sessão.
    """
    st.session_state["palavra_escolhida"] = get_palavra_escolhida()
    st.session_state["letras_digitadas"] = LetrasDigitadas(
        letras_digitadas=[LetraDigitada(letra=l, acertou=False, automatico=True) for l in LETRAS_AUTOMATICAS]
    )
    st.session_state["limite_erros"] = 5
    st.session_state["erros"] = 0


def chutar_letra() -> None:
    """
    Verifica se a letra informada existe na palavra. Se existir, adiciona a letra na lista de letras digitadas.

    Params:
        letra (str): Letra a ser verificada.
    """
    letra = st.session_state["letra"]
    if not letra or not letra.isalpha():
        st.toast("Digite uma letra")
        return None 
    letra = unidecode(letra).strip().lower()
    if letra in letras_digitadas.lista_letras:
        st.toast(f"Letra '{letra}' ja foi digitada")
    elif palavra_escolhida.existe_letra(letra):
        st.toast(f"Letra '{letra}' existe na palavra")
        st.session_state["letras_digitadas"].add(LetraDigitada(letra=letra, acertou=True))
    else:
        st.toast(f"Letra '{letra}' não existe na palavra")
        st.session_state["letras_digitadas"].add(LetraDigitada(letra=letra, acertou=False))
        st.session_state["erros"] += 1


def container_letra(class_name: str, cor: str = "red") -> stylable_container:
    """
    Cria um container para uma letra.

    Params:
        class_name (str): Nome da classe do container.
        cor (str, optional): Cor da letra. Defaults to "red".

    Returns:
        stylable_container: Objeto da classe stylable_container.
    """
    css =  f"""
        {{
            border-bottom: 2px solid {cor};
            padding: calc(1em - 2px)
        }}
    """
    return stylable_container(key=class_name, css_styles=css)


@st.cache_data
def get_audios(tipo: Literal["acerto", "erro"]) -> list[bytes]:
    audios_path = glob(f"pages/src/audio/{tipo}-*.*")
    return [open(path, "rb").read() for path in audios_path]


# Página

# Configuração da página
st.title("Jogo das palavras")


# Main
if "palavra_escolhida" not in st.session_state:
    iniciar()
else:
    st.button("Reiniciar", on_click=iniciar)

    palavra_escolhida: PalavraEscolhida = st.session_state["palavra_escolhida"]
    logger.debug(palavra_escolhida)
    letras_digitadas: LetrasDigitadas = st.session_state["letras_digitadas"]
    logger.debug(letras_digitadas)
    limite_erros: int = st.session_state["limite_erros"]
    erros: int = st.session_state["erros"]

    # Ganhou o jogo
    if palavra_escolhida.acertou(letras_digitadas.lista_letras):
        st.success(f"Parabéns! A palavra era: {palavra_escolhida.palavra}")
        rain(
            choice([
                "🥳",
                "🎉",
                "🎆",

            ]),
            animation_length=2
        )
        with st.expander("Nada aqui..."):
            st.audio(choice(get_audios("acerto")), autoplay=True)  
        st.stop()

    # Perdeu o jogo
    if erros == limite_erros: 
        st.error(f"Você perdeu! A palavra era: {palavra_escolhida.palavra}")
        rain(
            choice([
                "💔",
                "😭",
                "🤬"
            ]),
            animation_length=2
        )
        with st.expander("Nada aqui..."):
            st.audio(choice(get_audios("erro")), autoplay=True)
        st.stop()

    # Informação da palavra
    cols_palavra = st.columns(palavra_escolhida.quantidade_letras)
    for i in range(palavra_escolhida.quantidade_letras):
        with cols_palavra[i]:
            cor = "red"
            if palavra_escolhida.mostrar(letras_digitadas.lista_letras)[i] in LETRAS_AUTOMATICAS:
                cor = "orange"
            with container_letra(f"cl{i}", cor=cor):
                st.subheader(palavra_escolhida.mostrar(letras_digitadas.lista_letras)[i])
    st.caption(f'Algo sobre "{palavra_escolhida.tipo}" com {palavra_escolhida.quantidade_letras} letras')

    # Letras digitadas
    tagger_component("Letras digitadas", tags=letras_digitadas.lista_letras[TAMANHO_LETRAS_AUTOMATICAS:], color_name=letras_digitadas.cores_letras[TAMANHO_LETRAS_AUTOMATICAS:])
    st.write(f"Erros: {erros}/{limite_erros}")

    # Form para chutar letra
    with st.form("form_palavra", clear_on_submit=True):
        st.text_input("Letra", max_chars=1, value=None, key="letra")
        st.form_submit_button("Enviar", on_click=chutar_letra)

    # Dica
    with st.expander("Dica"):
        st.write(palavra_escolhida.dica)
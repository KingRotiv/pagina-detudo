import requests
import streamlit as st
from streamlit_extras.tags import tagger_component
from streamlit_extras.stylable_container import stylable_container
from loguru import logger
from pydantic import BaseModel, ValidationError


# API
TTL_CACHE_SEGUNDOS = 60
LOTERIAS = {
  "maismilionaria": {
      "nome": "+Milionária",
      "cor": "blue",
  },
  "megasena": {
      "nome": "Mega-Sena",
      "cor": "green",
  },
  "lotofacil": {
      "nome": "Lotofácil",
      "cor": "purple",
  },
  "quina": {
      "nome": "Quina",
      "cor": "blue",
  },
  "lotomania": {
      "nome": "Lotomania",
      "cor": "orange",
  },
  "timemania": {
      "nome": "Timemania",
      "cor": "green",
  },
  "duplasena": {
      "nome": "Dupla Sena",
      "cor": "red",
  },
  "federal": {
      "nome": "Federal",
      "cor": "blue",
  },
  "diadesorte": {
      "nome": "Dia de Sorte",
      "cor": "orange",
  },
  "supersete": {
      "nome": "Super Sete",
      "cor": "green",
  },
}
LOTERIAS_PARAMS = list(LOTERIAS.keys())

class MuniciopioUFGanhadores(BaseModel):
    ganhadores: int
    municipio: str
    nomeFatansiaUL: str
    posicao: int
    serie: str
    uf: str

class Premiacao(BaseModel):
    descricao: str
    faixa: int
    ganhadores: int
    valorPremio: float

class RespostaAPI(BaseModel):
    acumulou: bool
    loteria: str
    concurso: int
    data: str
    dataProximoConcurso: str
    dezenas: list[str]
    dezenasOrdemSorteio: list[str]
    estadosPremiados: list[str]
    local: str
    localGanhadores: list[MuniciopioUFGanhadores]
    mesSorte: str | None
    observacao: str | None
    premiacoes: list[Premiacao]
    proximoConcurso: int
    timeCoracao: str | None
    trevos: list[str]
    valorAcumuladoConcursoEspecial: float
    valorAcumuladoConcurso_0_5: float
    valorAcumuladoProximoConcurso: float
    valorArrecadado: float
    valorEstimadoProximoConcurso: float

@st.cache_resource(ttl=TTL_CACHE_SEGUNDOS)
def get_loteria(loteria: str, concurso: int = "latest") -> RespostaAPI | None:
    api_url = f"https://loteriascaixa-api.herokuapp.com/api/{loteria}/{concurso}"
    logger.debug(f"URL: {api_url}")
    resposta = requests.get(api_url)
    if resposta.status_code == 200:
        return RespostaAPI.model_validate(resposta.json())
    else:
        msg_erro = f"Erro {resposta.status_code}."
        logger.error(msg_erro)
        raise ConnectionError(msg_erro)

@st.cache_resource(ttl=TTL_CACHE_SEGUNDOS)
def get_loterias(loterias: list[str] = LOTERIAS_PARAMS) -> list[RespostaAPI]:
    return [get_loteria(loteria) for loteria in loterias]

def formatar_valor(valor: float) -> str:
    return f"{valor:_.2f}".replace(".", ",").replace("_", ".")

def container_loto(class_name: str, cor: str = "red") -> stylable_container:
    """
    class_name deve ser um nome válido para o html e css, caso contrário não funcionará.
    """
    css =  f"""
        {{
            border: 1px solid rgba(250, 250, 250, 0.2);
            border-radius: 0.5rem;
            border-left: 6px solid {cor};
            padding: calc(1em - 7px)
        }}
    """
    return stylable_container(key=class_name, css_styles=css)
    

# Página
st.title("Loterias Caixa")
st.write("Veja os resultados das Loterias Caixa.")

# Loterias Selecionadas
loterias_selecionadas = st.multiselect(
    "Loterias Selecionadas",
    options=LOTERIAS_PARAMS,
    default=LOTERIAS_PARAMS,
    format_func=lambda x: LOTERIAS[x]["nome"],
    placeholder="Selecione as Loterias"
)

# Tentando Obter os Dados
try:
    resultados = get_loterias(loterias=loterias_selecionadas)
except ConnectionError as ex:
    st.error(ex)
    st.stop()
except ValidationError as ex:
    st.error("Erro de Validação dos Dados.")
    st.stop()

for resultado in resultados:
    with container_loto(class_name=resultado.loteria, cor=LOTERIAS[resultado.loteria]["cor"]):
        col1, col2 = st.columns(2)

        # Cabeçalho Concurso Atual
        with col1:
            label = f"Concurso: {resultado.concurso} ({resultado.data})"
            value = LOTERIAS[resultado.loteria]["nome"]
            delta = f"Acumulou" if resultado.acumulou else "Não Acumulou"
            delta_color = "normal" if resultado.acumulou else "off"
            st.metric(
                label=label,
                value=value,
                delta=delta,
                delta_color=delta_color
            )

        # Cabeçalho Próximo Concurso
        with col2:
            label = f"Próximo Concurso: {resultado.proximoConcurso} ({resultado.dataProximoConcurso or 'n/a'})"
            value = "n/a"
            if resultado.valorEstimadoProximoConcurso:
                value = f"R$ {formatar_valor(resultado.valorEstimadoProximoConcurso)}"
            st.metric(
                label=label,
                value=value
            )

        # Dezenas Sorteadas ou Bilhetes
        tagger_label = "Bilhetes" if resultado.loteria == "federal" else "Dezenas Sorteadas"
        tagger_component(
            tagger_label,
            tags=resultado.dezenasOrdemSorteio,
            color_name=LOTERIAS[resultado.loteria]["cor"]
        )

        # Mês da Sorte ou Time do Coração
        match resultado.loteria:
            case "maismilionaria":
                tagger_component(
                    "Trevos",
                    tags=resultado.trevos,
                    color_name=LOTERIAS[resultado.loteria]["cor"]
                )
            case "diadesorte":
                tagger_component(
                    "Mês da Sorte",
                    tags=[resultado.mesSorte],
                    color_name=LOTERIAS[resultado.loteria]["cor"]
                )
            case "timemania":
                tagger_component(
                    "Time do Coração",
                    tags=[resultado.timeCoracao],
                    color_name=LOTERIAS[resultado.loteria]["cor"]
                )
        
        # Premiações
        with st.expander("Premiações"):
            for premiacao in resultado.premiacoes:

                descricao_acertos = premiacao.descricao
                if resultado.loteria == "federal":
                    descricao_acertos = f"{premiacao.faixa}º bilhete"
                st.write(f"**{descricao_acertos}**")

                caption = "Não houve ganhadores"

                if premiacao.ganhadores > 0:
                    if resultado.loteria == "federal":
                        caption = f"R$ {formatar_valor(premiacao.valorPremio)}"
                    else:
                        termo = "ganhador" if premiacao.ganhadores == 1 else "ganhadores"
                        caption = f"{premiacao.ganhadores} {termo}, R$ {formatar_valor(premiacao.valorPremio)}"
                st.caption(caption)

        # Locais das Premiações Principais
        with st.expander("Locais das Premiações Principais"):
            for local in resultado.localGanhadores:
                st.write(f"{local.municipio} - {local.nomeFatansiaUL} ({local.uf})")
                if resultado.loteria != "federal":
                    termo = "ganhador" if local.ganhadores == 1 else "ganhadores"
                    st.caption(f"{local.ganhadores} {termo}")
                else:
                    st.caption(f"{local.posicao}° bilhete")

        # Informaçoes Extras
        with st.expander("Informaçoes Extras"):
            if resultado.valorArrecadado:
                st.write(f"Total Arrecadado")
                st.caption(f"R$ {formatar_valor(resultado.valorArrecadado)}")
            if resultado.valorAcumuladoProximoConcurso:
                st.write(f"Acumulado Próximo Concurso")
                st.caption(f"R$ {formatar_valor(resultado.valorAcumuladoProximoConcurso)}")
            if resultado.valorAcumuladoConcurso_0_5:
                st.write(f"Acumulado Concurso Final 0 e 5")
                st.caption(f"R$ {formatar_valor(resultado.valorAcumuladoConcurso_0_5)}")
            if resultado.valorAcumuladoConcursoEspecial:
                st.write(f"Acumulado Concurso Especial")
                st.caption(f"R$ {formatar_valor(resultado.valorAcumuladoConcursoEspecial)}")
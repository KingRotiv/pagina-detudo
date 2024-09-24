from typing import Literal

import requests
import pandas as pd
import streamlit as st
from loguru import logger
from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress


# API
class RespostaAPI(BaseModel):
    status: Literal["success", "fail"] | None = None
    message: str | None = None
    continent: str | None = None
    continentCode: str | None = None
    country: str | None = None
    countryCode: str | None = None
    region: str | None = None
    regionName: str | None = None
    city: str | None = None
    district: str | None = None
    lat: float | None = None
    lon: float | None = None
    timezone: str | None = None
    currency: str | None = None
    isp: str | None = None
    org: str | None = None
    as_: str | None = Field(None, alias="as")
    asname: str | None = None
    reverse: str | None = None
    mobile: bool | None = None
    proxy: bool | None = None
    hosting: bool | None = None
    query: str | None = None


fields_api = ",".join(list(RespostaAPI.model_fields.keys())).replace("as_", "as")


@st.cache_resource(ttl=60)
def obter_info(ip: str | None, lang: str = "pt-BR") -> RespostaAPI:
    if not ip:
        ip = ""

    api_url = "http://ip-api.com/json/"
    params = {"lang": lang, "fields": fields_api}

    resposta = requests.get(api_url + ip, params=params)
    logger.debug(resposta.url)
    if resposta.status_code == 200:
        return RespostaAPI.model_validate(resposta.json())
    else:
        return RespostaAPI(status="fail", message="API indisponível")


# Página
st.title("IP Geolocalização")
st.write("Obtenha a localização e informações de um IP.")

ip = st.text_input("**IP:**")
st.caption(
    "Por favor, digite (deixe vazio para IP atual) o IP que deseja obter a localização. "
)

# Verificar IP
if ip:
    try:
        IPvAnyAddress(ip)
    except ValueError:
        st.error("IP inválido!")
        st.stop()

resposta = obter_info(ip)

# Exibir resposta
if resposta.status == "success":

    # Localização
    if resposta.lat and resposta.lon:
        with st.container(border=True):
            # Cabeçalho
            c_1, c_2, c_3 = st.columns(3)
            c_1.metric("Cidade", value=resposta.city)
            c_2.metric("Estado", value=resposta.regionName)
            c_3.metric("País", value=resposta.country)
            # Mapa
            df = pd.DataFrame(
                [[resposta.lat, resposta.lon]],
                columns=["lat", "lon"],
            )
            st.map(
                data=df,
                latitude=str(resposta.lat),
                longitude=str(resposta.lon),
                zoom=12,
            )

    # Informações adicionais
    with st.container(border=True):
        if resposta.city:
            st.text_input("**Cidade:**", value=resposta.city, disabled=True)
        if resposta.regionName:
            _v = f"{resposta.regionName} ({resposta.region})"
            st.text_input("**Estado:**", value=_v, disabled=True)
        if resposta.country:
            _v = f"{resposta.country} ({resposta.countryCode})"
            st.text_input("**País:**", value=_v, disabled=True)
        if resposta.continent:
            _v = f"{resposta.continent} ({resposta.continentCode})"
            st.text_input("**Continente:**", value=_v, disabled=True)
        if resposta.timezone:
            st.text_input("**Fuso Horário:**", value=resposta.timezone, disabled=True)
        if resposta.currency:
            st.text_input("**Moeda do País:**", value=resposta.currency, disabled=True)
        if resposta.isp:
            st.text_input("**ISP:**", value=resposta.isp, disabled=True)
        if resposta.org:
            st.text_input("**Organização:**", value=resposta.org, disabled=True)
        if resposta.as_:
            st.text_input("**AS:**", value=resposta.as_, disabled=True)
        if resposta.asname:
            st.text_input("**Nome AS:**", value=resposta.asname, disabled=True)
        if resposta.reverse:
            st.text_input("**DNS Reverso:**", value=resposta.reverse, disabled=True)

# Resposta de erro
else:
    st.error(resposta.message)

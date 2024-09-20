import datetime
from html import escape as html_escape

import streamlit as st
from streamlit_tags import st_tags
from weasyprint import HTML


# Informação da página
st.title("Gerar currículo")
st.write("Crie seu currículo profissional de forma fácil e rápida.")

# Variáveis para armazenar dados
dados_basicos = (
    st.session_state.get("gerar_curriculo.dados_basicos")
    if st.session_state.get("gerar_curriculo.dados_basicos")
    else {}
)
experiencias = (
    st.session_state.get("gerar_curriculo.experiencias")
    if st.session_state.get("gerar_curriculo.experiencias")
    else []
)
formacoes = (
    st.session_state.get("gerar_curriculo.formacoes")
    if st.session_state.get("gerar_curriculo.formacoes")
    else []
)
habilidades = (
    st.session_state.get("gerar_curriculo.habilidades")
    if st.session_state.get("gerar_curriculo.habilidades")
    else []
)


# Aba de Dados Básicos
with st.expander("Informações Básicas", expanded=True):
    with st.form("form_dados_basicos", border=False):
        nome_completo = st.text_input("Nome Completo")
        data_nascimento = st.date_input(
            "Data de Nascimento",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            format="DD/MM/YYYY",
        )
        celular = st.text_input("Celular")
        email = st.text_input("Email")
        cargo_desejado = st.text_input("Cargo Desejado")
        salvar_dados_basicos = st.form_submit_button("Salvar")

        if salvar_dados_basicos:
            if not nome_completo or not celular or not email or not cargo_desejado:
                st.error("Por favor, preencha todos os campos.")
            else:
                st.session_state["gerar_curriculo.dados_basicos"] = {
                    "Nome Completo": nome_completo,
                    "Data de Nascimento": data_nascimento,
                    "Celular": celular,
                    "Email": email,
                    "Cargo Desejado": cargo_desejado,
                }
                st.success("Dados básicos salvos com sucesso!")


# Aba de Experiência
@st.dialog("Adicionar/Editar Experiência")
def adicionar_experiencia(index=None, empresa="", cargo="", admisao=None, demisao=None, descricao=""):
    with st.form("form_experiencia"):
        empresa_experiencia = st.text_input("Empresa", value=empresa)
        cargo_experiencia = st.text_input("Cargo", value=cargo)
        admisao_experiencia = st.date_input(
            "Admissão",
            value=admisao,
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            format="DD/MM/YYYY",
        )
        demisao_experiencia = st.date_input(
            "Demissão",
            value=demisao,
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            format="DD/MM/YYYY",
        )
        descricao_experiencia = st.text_area(
            "Descrição das atividades", value=descricao
        )
        salvar_experiencia = st.form_submit_button("Salvar")

        if salvar_experiencia:
            if (
                not empresa_experiencia
                or not cargo_experiencia
                or not admisao_experiencia
                or not descricao_experiencia
            ):
                st.error("Por favor, preencha todos os campos.")
            else:
                nova_experiencia = {
                    "Empresa": empresa_experiencia,
                    "Cargo": cargo_experiencia,
                    "Admissão": admisao_experiencia,
                    "Demissão": demisao_experiencia,
                    "Descrição": descricao_experiencia,
                }
                if index is None:
                    experiencias.append(nova_experiencia)
                else:
                    experiencias[index] = nova_experiencia
                st.session_state["gerar_curriculo.experiencias"] = experiencias
                st.success("Experiência profissional salva com sucesso!")
                st.rerun()


with st.expander("Experiência Profissional", expanded=True):
    if st.button("Adicionar Nova Experiência"):
        adicionar_experiencia()

    for idx, exp in enumerate(experiencias):
        col_info, col_botao = st.columns([.7, .3], vertical_alignment="center")
        with col_info:
            st.write(f"**{exp['Empresa']}** - {exp['Cargo']}")
        with col_botao:
            col_botao_editar, col_botao_remover = st.columns(2, vertical_alignment="center")
            with col_botao_editar:
                if st.button("Editar", key=f"editar_exp_{idx}"):
                    adicionar_experiencia(
                        index=idx,
                        empresa=exp["Empresa"],
                        cargo=exp["Cargo"],
                        admisao=exp["Admissão"],
                        demisao=exp["Demissão"],
                        descricao=exp["Descrição"],
                    )
            with col_botao_remover:
                if st.button("Remover", key=f"remover_exp_{idx}"):
                    experiencias.pop(idx)
                    st.rerun()


# Aba de Formação Acadêmica
@st.dialog("Adicionar/Editar Formação Acadêmica")
def adicionar_formacao(
    index=None,
    instituicao="",
    curso="",
    nivel="Educação Básica",
    ano_inicio=None,
    ano_termino=None,
    situacao="Cursando",
):
    with st.form("form_formacao"):
        instituicao_formacao = st.text_input("Instituição", value=instituicao)
        curso_formacao = st.text_input("Curso", value=curso)
        nivel_formacao = st.selectbox(
            "Nível",
            ["Educação Básica", "Ensino Tecnico", "Ensino Superior"],
            index=["Educação Básica", "Ensino Tecnico", "Ensino Superior"].index(
                nivel
            )
        )
        ano_inicio_formacao = st.number_input("Ano de início", min_value=1900, step=1, value=ano_inicio)
        ano_termino_formacao = st.number_input(
            "Ano de término", min_value=1900, step=1, value=ano_termino
        )
        situacao_formacao = st.selectbox(
            "Situação",
            ["Cursando", "Concluído", "Trancado"],
            index=["Cursando", "Concluído", "Trancado"].index(situacao),
        )
        salvar_formacao = st.form_submit_button("Salvar")

        if salvar_formacao:
            if (
                not instituicao_formacao
                or not curso_formacao
                or not nivel_formacao
                or not ano_inicio_formacao
                or not ano_termino_formacao
            ):
                st.error("Por favor, preencha todos os campos.")
            else:
                nova_formacao = {
                    "Instituição": instituicao_formacao,
                    "Curso": curso_formacao,
                    "Nível": nivel_formacao,
                    "Ano de Início": ano_inicio_formacao,
                    "Ano de Término": ano_termino_formacao,
                    "Situação": situacao_formacao,
                }
                if index is None:
                    formacoes.append(nova_formacao)
                else:
                    formacoes[index] = nova_formacao
                st.session_state["gerar_curriculo.formacoes"] = formacoes
                st.success("Formação acadêmica salva com sucesso!")
                st.rerun()


with st.expander("Formação Acadêmica", expanded=True):
    if st.button("Adicionar Nova Formação"):
        adicionar_formacao()

    for idx, formacao in enumerate(formacoes):
        col_info, col_botao = st.columns([.7, .3], vertical_alignment="center")
        with col_info:
            st.write(f"**{formacao['Instituição']}** - {formacao['Curso']}")
        with col_botao:
            col_botao_editar, col_botao_remover = st.columns(2, vertical_alignment="center")
            with col_botao_editar:
                if st.button("Editar", key=f"editar_formacao_{idx}"):
                    adicionar_formacao(
                        index=idx,
                        instituicao=formacao["Instituição"],
                        curso=formacao["Curso"],
                        nivel=formacao["Nível"],
                        ano_inicio=formacao["Ano de Início"],
                        ano_termino=formacao["Ano de Término"],
                        situacao=formacao["Situação"],
                    )
            with col_botao_remover:
                if st.button("Remover", key=f"remover_formacao_{idx}"):
                    formacoes.pop(idx)
                    st.rerun()


# Aba de habilidades
with st.expander("Habilidades", expanded=True):
    habilidades = st_tags(
        habilidades,
        label="Suas Habilidades",
        text="Adicionar Habilidade",
        maxtags=5,
    )
    st.session_state["gerar_curriculo.habilidades"] = habilidades


# Função para gerar PDF HTML
def gerar_pdf():
    experiencias_html = ""
    for exp in experiencias:
        experiencias_html += f"""
            <ul>
                <li><b>Empresa:</b> {html_escape(exp.get('Empresa'))}</li>
                <li><b>Cargo:</b> {html_escape(exp.get('Cargo'))}</li>
                <li><b>Período:</b> {exp.get('Admissão').strftime('%d/%m/%Y')} - {exp.get('Demissão').strftime('%d/%m/%Y') if exp.get('Demissão') else 'Atual'}</li>
                <li><b>Descrição:</b> {html_escape(exp.get('Descrição'))}</li>
            </ul>
        """

    formacoes_html = ""
    for formacao in formacoes:
        formacoes_html += f"""
            <ul>
                <li><b>Instituição:</b> {html_escape(formacao.get('Instituição'))}</li>
                <li><b>Curso:</b> {html_escape(formacao.get('Curso'))}</li>
                <li><b>Nível:</b> {html_escape(formacao.get('Nível'))}</li>
                <li><b>Ano de Início:</b> {formacao.get('Ano de Início')}</li>
                <li><b>Ano de Término:</b> {formacao.get('Ano de Término')}</li>
                <li><b>Situação:</b> {html_escape(formacao.get('Situação'))}</li>
            </ul>
        """

    habilidades_html = f"""
        <hr>
        <h2>Habilidades</h2>
        <ul>{
            ''.join([f"<li>{html_escape(habilidade.title())}</li>" for habilidade in habilidades])
        }</ul>
    """

    dados_html = f"""
        <center>
            <h1><b>{html_escape(dados_basicos.get('Nome Completo'))}</b></h1>
        </center>
        <p><b>Data de Nascimento:</b> {html_escape(dados_basicos.get('Data de Nascimento').strftime('%d/%m/%Y'))}</p>
        <p><b>Celular:</b> {html_escape(dados_basicos.get('Celular'))}</p>
        <p><b>Email:</b> {html_escape(dados_basicos.get('Email'))}</p>
        <p><b>Cargo Desejado:</b> {html_escape(dados_basicos.get('Cargo Desejado'))}</p>
        <hr>
        <h2>Experiência Profissional</h2>
        {experiencias_html}
        <hr>
        <h2>Formação Académica</h2>
        {formacoes_html}
        {habilidades_html if habilidades else ''}
    """

    pdf = HTML(string=dados_html).write_pdf()
    return pdf


# Progresso de preenchimento
texto_prog = "Preencimento"
valor_prog = 0
prog = st.progress(valor_prog, text=texto_prog)
if dados_basicos:
    valor_prog += 30
    prog = prog.progress(valor_prog, text=texto_prog)
if experiencias:
    valor_prog += 30
    prog = prog.progress(valor_prog, text=texto_prog)
if formacoes:
    valor_prog += 30
    prog = prog.progress(valor_prog, text=texto_prog)
if habilidades:
    valor_prog += 10
    prog = prog.progress(valor_prog, text=texto_prog)


# Botão para gerar o currículo completo em PDF
if st.button("Gerar PDF"):
    if not dados_basicos or not experiencias or not formacoes:
        st.error("Por favor, preencha todas as informações antes de gerar o PDF.")
    else:
        nome_arquivo = f"{dados_basicos.get('Nome Completo')}.pdf"
        st.download_button(
            "Baixar Currículo em PDF",
            data=gerar_pdf(),
            file_name=nome_arquivo,
            mime="application/pdf",
        )

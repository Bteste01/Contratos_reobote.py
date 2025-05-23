import streamlit as st
import json
import os
from PIL import Image

# --- Configurações iniciais ---
ARQUIVO_JSON = "contratos.json"
ARQUIVO_ADMINS = "admins.json"
LOGO_PATH = "logo_empresa.png"  # Coloque o arquivo de logo na mesma pasta deste script

if 'empresa' not in st.session_state:
    st.session_state.empresa = {
        "nome": "Grupo Reobote Serviços",
        "descricao": "Sistema Contratos e Ações",
        "logo": LOGO_PATH
    }

# Inicializar admins e contratos
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {"email": "admin@admin.com", "senha": "admin123"}
if 'admins' not in st.session_state:
    if os.path.exists(ARQUIVO_ADMINS):
        with open(ARQUIVO_ADMINS, "r") as f:
            st.session_state.admins = json.load(f)
    else:
        st.session_state.admins = []
if 'contratos' not in st.session_state:
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r") as f:
            st.session_state.contratos = json.load(f)
    else:
        st.session_state.contratos = []

# Função para salvar contratos em JSON
def salvar_contratos():
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(st.session_state.contratos, f, indent=4, ensure_ascii=False)

# Função para salvar admins em JSON
def salvar_admins():
    with open(ARQUIVO_ADMINS, "w") as f:
        json.dump(st.session_state.admins, f, indent=4, ensure_ascii=False)

# --- Interface ---
st.set_page_config(page_title="Contratos e Ações - Grupo Reobote Serviços")

# Cabeçalho com logo e nome da empresa
col1, col2 = st.columns([1,5])
with col1:
    try:
        img = Image.open(st.session_state.empresa["logo"])
        st.image(img, width=80)
    except:
        st.write("Logo não encontrada.")
with col2:
    st.title(st.session_state.empresa["nome"])
    st.write(st.session_state.empresa["descricao"])
st.markdown("---")

# --------------------------
# Área pública - Cliente
# --------------------------
st.header("Preencha seu Contrato")

tipos_contrato = {
    "Parceria": [
        "Cláusula 1: A parceria será benéfica para ambas as partes.",
        "Cláusula 2: Não há cobrança de valores nesta parceria.",
        "Cláusula 3: A parceria terá prazo determinado conforme selecionado."
    ],
    "Vínculo de Assessoria": [
        "Cláusula 1: O assessorará prestará serviços conforme combinado.",
        "Cláusula 2: O contrato será remunerado conforme a forma de pagamento escolhida.",
        "Cláusula 3: O vínculo terá duração conforme o prazo selecionado."
    ],
    "Contrato de Agendamento de Artistas": [
        "Cláusula 1: O agendamento será confirmado após aprovação.",
        "Cláusula 2: Pagamento deve ser realizado conforme forma escolhida.",
        "Cláusula 3: O contrato é válido para o evento na data e horário informados."
    ]
}

tipo = st.selectbox("Tipo de Contrato", list(tipos_contrato.keys()))

st.subheader("Cláusulas do Contrato")
for c in tipos_contrato[tipo]:
    st.write(f"- {c}")

# Prazo do contrato ou data do evento
if tipo == "Contrato de Agendamento de Artistas":
    data_evento = st.date_input("Data do Evento")
    hora_inicio = st.time_input("Hora de Início")
    hora_fim = st.time_input("Hora de Término")
else:
    prazo = st.selectbox("Prazo do contrato (meses)", [3,6,12])

# Forma de pagamento (somente se não for parceria)
forma_pagamento = None
if tipo != "Parceria":
    forma_pagamento = st.selectbox("Forma de pagamento", ["Boleto", "Cartão de Crédito", "Pix", "Transferência Bancária"])

st.subheader("Dados de Identidade")
nome_cliente = st.text_input("Nome completo")
cpf_cliente = st.text_input("CPF")
doc_cliente = st.text_input("Documento de identificação (RG, CNH etc.)")

st.subheader("Localização")
rua_cliente = st.text_input("Rua")
bairro_cliente = st.text_input("Bairro")
cidade_cliente = st.text_input("Cidade")
numero_cliente = st.text_input("Número")

st.subheader("Contato")
email_cliente = st.text_input("Email")
telefone_cliente = st.text_input("Telefone")

st.subheader("Assinatura Digital")
assinatura_cliente = st.text_input("Digite seu nome completo para assinar")

if st.button("Enviar Contrato"):
    if not (nome_cliente and cpf_cliente and email_cliente and assinatura_cliente):
        st.error("Preencha ao menos nome, CPF, email e assinatura para continuar.")
    else:
        contrato = {
            "tipo": tipo,
            "clausulas": tipos_contrato[tipo],
            "prazo_meses": prazo if tipo != "Contrato de Agendamento de Artistas" else None,
            "data_evento": str(data_evento) if tipo == "Contrato de Agendamento de Artistas" else None,
            "hora_inicio": str(hora_inicio) if tipo == "Contrato de Agendamento de Artistas" else None,
            "hora_fim": str(hora_fim) if tipo == "Contrato de Agendamento de Artistas" else None,
            "forma_pagamento": forma_pagamento if forma_pagamento else "Isento (Parceria)",
            "dados_identidade": {
                "nome": nome_cliente,
                "cpf": cpf_cliente,
                "documento": doc_cliente
            },
            "localizacao": {
                "rua": rua_cliente,
                "bairro": bairro_cliente,
                "cidade": cidade_cliente,
                "numero": numero_cliente
            },
            "contato": {
                "email": email_cliente,
                "telefone": telefone_cliente
            },
            "assinatura": assinatura_cliente
        }
        st.session_state.contratos.append(contrato)
        salvar_contratos()
        st.success("Contrato enviado e salvo com sucesso!")

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
        "Cláusula 3: O contrato é válido pelo prazo selecionado."
    ]
}

tipo = st.selectbox("Tipo de Contrato", list(tipos_contrato.keys()))

st.subheader("Cláusulas do Contrato")
for c in tipos_contrato[tipo]:
    st.write(f"- {c}")

# Prazo do contrato
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
            "prazo_meses": prazo,
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

st.markdown("---")

# --------------------------
# Área de login administrativo
# --------------------------
st.header("Área de Login Administrativo")

if 'admin_logado' not in st.session_state:
    st.session_state.admin_logado = None

email_login = st.text_input("Email", key="login_email")
senha_login = st.text_input("Senha", type="password", key="login_senha")
botao_login = st.button("Entrar")

if botao_login:
    if email_login == st.session_state.admin_principal["email"] and senha_login == st.session_state.admin_principal["senha"]:
        st.session_state.admin_logado = "principal"
        st.success("Logado como Administrador Principal")
    else:
        admin_match = next((a for a in st.session_state.admins if a["email"] == email_login and a["senha"] == senha_login), None)
        if admin_match:
            st.session_state.admin_logado = email_login
            st.success("Logado como Administrador Comum")
        else:
            st.error("Credenciais inválidas")

# --------------------------
# Área administrativa
# --------------------------
if st.session_state.admin_logado:
    st.markdown("---")
    st.header("Painel Administrativo")

    # Botão para logout
    if st.button("Sair"):
        st.session_state.admin_logado = None
        st.experimental_rerun()

    # ADMIN PRINCIPAL
    if st.session_state.admin_logado == "principal":
        st.subheader("Gerenciar Administradores")

        with st.form("form_cadastrar_admin"):
            novo_email = st.text_input("Email do novo administrador")
            nova_senha = st.text_input("Senha do novo administrador", type="password")
            enviar_admin = st.form_submit_button("Cadastrar Administrador")
            if enviar_admin:
                if novo_email.strip() == "" or nova_senha.strip() == "":
                    st.error("Email e senha são obrigatórios.")
                else:
                    if any(a["email"] == novo_email for a in st.session_state.admins):
                        st.error("Já existe um administrador com esse email.")
                    else:
                        st.session_state.admins.append({"email": novo_email, "senha": nova_senha})
                        salvar_admins()
                        st.success(f"Administrador {novo_email} cadastrado!")

        st.markdown("---")

    # Ambos (principal e admins comuns) podem editar contratos
    st.subheader("Contratos Cadastrados")
    if len(st.session_state.contratos) == 0:
        st.info("Nenhum contrato cadastrado ainda.")
    else:
        contratos = st.session_state.contratos
        contrato_ids = list(range(len(contratos)))
        contrato_selecionado = st.selectbox("Selecione um contrato para visualizar/editar", contrato_ids)

        contrato = contratos[contrato_selecionado]

        st.write(f"**Tipo:** {contrato['tipo']}")
        st.write("**Cláusulas:**")
        for c in contrato["clausulas"]:
            st.write(f"- {c}")
        st.write(f"**Prazo (meses):** {contrato['prazo_meses']}")
        st.write(f"**Forma de pagamento:** {contrato['forma_pagamento']}")

        # Campos editáveis (administrador comum edita só contato e localização, principal pode

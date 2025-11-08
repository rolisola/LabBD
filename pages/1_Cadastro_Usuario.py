import streamlit as st

st.set_page_config(page_title="Cadastro de Usuário", page_icon="👤", layout="centered")

# Proteção de acesso
if "auth" not in st.session_state or not st.session_state["auth"].get("logged"):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Ir para Login", icon="🏠") if hasattr(st, "page_link") else st.info("Volte à página inicial para login.")
    st.stop()

st.title("Cadastro de Usuário 👤")

if "users" not in st.session_state:
    st.session_state["users"] = []

with st.form("user_form", clear_on_submit=True):
    nome = st.text_input("Nome completo", placeholder="Seu nome")
    email = st.text_input("Email", placeholder="voce@exemplo.com")
    username = st.text_input("Usuário", placeholder="apelido")
    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("Senha", type="password")
    with col2:
        password2 = st.text_input("Confirmar Senha", type="password")
    submitted = st.form_submit_button("Cadastrar")

if submitted:
    if not (nome and email and username and password):
        st.error("Preencha todos os campos obrigatórios.")
    elif password != password2:
        st.error("As senhas não coincidem.")
    elif any(u["username"] == username for u in st.session_state["users"]):
        st.error("Usuário já existente.")
    else:
        st.session_state["users"].append({
            "nome": nome,
            "email": email,
            "username": username,
            "password": password,
        })
        st.success(f"Usuário '{username}' cadastrado com sucesso!")

st.divider()

st.subheader("Usuários cadastrados")
for u in st.session_state["users"]:
    st.write(f"• {u['username']} - {u.get('nome','(sem nome)')} - {u.get('email','')}")

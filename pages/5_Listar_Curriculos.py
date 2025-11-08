import streamlit as st

st.set_page_config(page_title="Listagem de Currículos", page_icon="🧑\u200d💼", layout="wide")

# Proteção de acesso
if "auth" not in st.session_state or not st.session_state["auth"].get("logged"):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Ir para Login", icon="🏠") if hasattr(st, "page_link") else st.info("Volte à página inicial para login.")
    st.stop()

st.title("Currículos Ativos 🧑\u200d💼")

curriculos = st.session_state.get("curriculos", [])

colf1, colf2 = st.columns(2)
with colf1:
    filtro_idioma = st.text_input("Filtrar por idioma (contém)")
with colf2:
    busca = st.text_input("Busca por nome / email")

filtradas = []
for c in curriculos:
    if filtro_idioma and filtro_idioma.lower() not in (c.get("idiomas", "").lower()):
        continue
    if busca:
        txt = (c.get("nome", "") + " " + c.get("email", "")).lower()
        if busca.lower() not in txt:
            continue
    filtradas.append(c)

st.write(f"Total: {len(filtradas)} currículos")

for c in filtradas:
    with st.expander(f"{c.get('nome')} — {c.get('email')}"):
        st.write(f"Formação: {c.get('formacao')}")
        st.write(f"Experiência: {c.get('experiencia')}")
        st.write(f"Skills: {c.get('skills')}")
        st.write(f"Idiomas: {c.get('idiomas')}")
        st.write(f"Certificações: {c.get('certificacoes')}")
        st.write(f"Resumo: {c.get('resumo')}")
        st.write(f"Empresas Prévias: {c.get('empresas_previas')}")
        st.write(f"IDs Contatos: {c.get('ids_contatos')}")

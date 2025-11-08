import streamlit as st

st.set_page_config(page_title="Listagem de Vagas", page_icon="📋", layout="wide")

# Proteção de acesso
if "auth" not in st.session_state or not st.session_state["auth"].get("logged"):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Ir para Login", icon="🏠") if hasattr(st, "page_link") else st.info("Volte à página inicial para login.")
    st.stop()

st.title("Vagas Abertas 📋")

vagas = st.session_state.get("vagas", [])

# Filtros simples
colf1, colf2, colf3 = st.columns(3)
with colf1:
    filtro_estado = st.selectbox("Estado", options=["(todos)"] + sorted({v.get("estado") for v in vagas if v.get("estado")}), index=0)
with colf2:
    filtro_contrato = st.selectbox("Tipo", options=["(todos)"] + sorted({v.get("tipo_contratacao") for v in vagas if v.get("tipo_contratacao")}), index=0)
with colf3:
    busca = st.text_input("Busca por título / empresa")

filtradas = []
for v in vagas:
    if filtro_estado != "(todos)" and v.get("estado") != filtro_estado:
        continue
    if filtro_contrato != "(todos)" and v.get("tipo_contratacao") != filtro_contrato:
        continue
    if busca:
        txt = (v.get("titulo", "") + " " + v.get("empresa", "")).lower()
        if busca.lower() not in txt:
            continue
    filtradas.append(v)

st.write(f"Total: {len(filtradas)} vagas")

for v in filtradas:
    with st.expander(f"{v.get('titulo')} — {v.get('empresa')} ({v.get('cidade')}/{v.get('estado')})"):
        st.write(v.get("descricao"))
        st.write(f"Tipo: {v.get('tipo_contratacao')} | Salário: {v.get('salario')}")
        st.write(f"Skills: {v.get('skills')}")

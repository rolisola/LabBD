import streamlit as st
import csv
from pathlib import Path

st.set_page_config(page_title="Cadastro de Currículo", page_icon="📄", layout="centered")

BASE_DIR = Path(__file__).resolve().parents[1]
MATERIAL_DIR = BASE_DIR / "material"
CURRICULOS_CSV = MATERIAL_DIR / "curriculos.csv"


def _csv_to_dicts(path: Path, delimiter: str = ";"):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [{k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()} for row in reader]


# Inicializa coleções
if "curriculos" not in st.session_state:
    st.session_state["curriculos"] = _csv_to_dicts(CURRICULOS_CSV)

# Proteção de acesso
if "auth" not in st.session_state or not st.session_state["auth"].get("logged"):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Ir para Login", icon="🏠") if hasattr(st, "page_link") else st.info("Volte à página inicial para login.")
    st.stop()

st.title("Cadastro de Currículo 📄")

# Opções de skills únicas derivadas dos currículos existentes (e também útil para vagas)
skill_set = set()
for c in st.session_state["curriculos"]:
    raw = c.get("skills") or ""
    for s in raw.split(","):
        s = s.strip()
        if s:
            skill_set.add(s)
skills_options = sorted(skill_set)

with st.form("curriculo_form", clear_on_submit=True):
    col0, col1 = st.columns([1, 3])
    with col0:
        id_str = st.text_input("ID", placeholder="(opcional)")
    with col1:
        nome = st.text_input("Nome")

    col2, col3 = st.columns(2)
    with col2:
        email = st.text_input("Email")
    with col3:
        telefone = st.text_input("Telefone")

    formacao = st.text_input("Formação")
    experiencia = st.text_area("Experiência")
    skills = st.multiselect("Skills", options=skills_options)

    col4, col5 = st.columns(2)
    with col4:
        idiomas = st.text_input("Idiomas", placeholder="Ex.: Português, Inglês")
    with col5:
        certificacoes = st.text_input("Certificações", placeholder="Ex.: AWS, Azure, ...")

    resumo = st.text_area("Resumo")

    col6, col7 = st.columns(2)
    with col6:
        empresas_previas = st.text_input("Empresas Prévias")
    with col7:
        ids_contatos = st.text_input("IDs de Contatos")

    submitted = st.form_submit_button("Salvar Currículo")

if submitted:
    novo = {
        "id": id_str,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "formacao": formacao,
        "experiencia": experiencia,
        "skills": ", ".join(skills),
        "idiomas": idiomas,
        "certificacoes": certificacoes,
        "resumo": resumo,
        "empresas_previas": empresas_previas,
        "ids_contatos": ids_contatos,
    }
    if not nome or not email:
        st.error("Nome e Email são obrigatórios.")
    else:
        st.session_state["curriculos"].append(novo)
        st.success("Currículo cadastrado com sucesso!")

st.divider()
st.caption("Exemplo de registros (últimos 5):")
for c in st.session_state.get("curriculos", [])[-5:]:
    st.write(f"• {c.get('nome')} — {c.get('email')}")

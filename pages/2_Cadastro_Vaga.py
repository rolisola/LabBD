import streamlit as st
import csv
from pathlib import Path

st.set_page_config(page_title="Cadastro de Vaga", page_icon="📝", layout="centered")

BASE_DIR = Path(__file__).resolve().parents[1]
MATERIAL_DIR = BASE_DIR / "material"
VAGAS_CSV = MATERIAL_DIR / "vagas.csv"


def _csv_to_dicts(path: Path, delimiter: str = ";"):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [{k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()} for row in reader]


# Inicializa coleções
if "vagas" not in st.session_state:
    st.session_state["vagas"] = _csv_to_dicts(VAGAS_CSV)

# Proteção de acesso
if "auth" not in st.session_state or not st.session_state["auth"].get("logged"):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Ir para Login", icon="🏠") if hasattr(st, "page_link") else st.info("Volte à página inicial para login.")
    st.stop()

st.title("Cadastro de Vaga 📝")

# Opções derivadas das vagas existentes
estados = sorted({v.get("estado", "") for v in st.session_state["vagas"] if v.get("estado")})
contratos = sorted({v.get("tipo_contratacao", "") for v in st.session_state["vagas"] if v.get("tipo_contratacao")})
# Skills únicas (split por vírgula)
skills_set = set()
for v in st.session_state["vagas"]:
    raw = v.get("skills") or ""
    for s in raw.split(","):
        s = s.strip()
        if s:
            skills_set.add(s)
skills_options = sorted(skills_set)

with st.form("vaga_form", clear_on_submit=True):
    titulo = st.text_input("Título", placeholder="Ex.: Desenvolvedor Backend")
    descricao = st.text_area("Descrição")
    col1, col2, col3 = st.columns(3)
    with col1:
        cidade = st.text_input("Cidade")
    with col2:
        estado = st.selectbox("Estado", options=["-"] + estados, index=0)
    with col3:
        tipo_contratacao = st.selectbox("Tipo de contratação", options=["-"] + contratos, index=0)

    col4, col5 = st.columns(2)
    with col4:
        salario = st.text_input("Salário", placeholder="R$ 0,00")
    with col5:
        empresa = st.text_input("Empresa")

    skills = st.multiselect("Skills", options=skills_options)

    submitted = st.form_submit_button("Salvar Vaga")

if submitted:
    if not titulo:
        st.error("Título é obrigatório.")
    else:
        nova = {
            "titulo": titulo,
            "descricao": descricao,
            "cidade": cidade,
            "estado": "" if estado == "-" else estado,
            "tipo_contratacao": "" if tipo_contratacao == "-" else tipo_contratacao,
            "salario": salario,
            "empresa": empresa,
            "skills": ", ".join(skills),
        }
        st.session_state["vagas"].append(nova)
        st.success("Vaga cadastrada com sucesso!")

st.divider()
if st.session_state.get("vagas"):
    st.caption("Exemplo de registros (últimos 5):")
    for v in st.session_state["vagas"][-5:]:
        st.write(f"• {v.get('titulo')} — {v.get('cidade')}/{v.get('estado')} — {v.get('empresa')}")

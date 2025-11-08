import streamlit as st
import csv
from pathlib import Path

# Configurações básicas da página
st.set_page_config(page_title="Portal de Vagas", page_icon="💼", layout="centered")

BASE_DIR = Path(__file__).resolve().parent
MATERIAL_DIR = BASE_DIR / "material"
VAGAS_CSV = MATERIAL_DIR / "vagas.csv"
CURRICULOS_CSV = MATERIAL_DIR / "curriculos.csv"


def _csv_to_dicts(path: Path, delimiter: str = ";"):
	if not path.exists():
		return []
	with path.open("r", encoding="utf-8") as f:
		reader = csv.DictReader(f, delimiter=delimiter)
		rows = [
			{k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
			for row in reader
		]
	return rows


def init_state():
	# Usuários (apenas memória). Usuário demo: admin/admin
	st.session_state.setdefault("users", [
		{"username": "admin", "password": "admin", "email": "admin@example.com", "nome": "Administrador"}
	])
	st.session_state.setdefault("auth", {"logged": False, "user": None})

	# Vagas e Currículos (carrega do CSV apenas uma vez)
	if "vagas" not in st.session_state:
		st.session_state["vagas"] = _csv_to_dicts(VAGAS_CSV)
	if "curriculos" not in st.session_state:
		st.session_state["curriculos"] = _csv_to_dicts(CURRICULOS_CSV)


def page_link(label: str, page_file: str):
	# Tenta usar st.page_link (se disponível). Caso contrário, mostra instrução.
	if hasattr(st, "page_link"):
		st.page_link(f"pages/{page_file}", label=label, icon="➡️")
	else:
		st.markdown(f"- Abra no menu lateral: **{label}**")


def login_view():
	st.title("Portal de Vagas 💼")
	st.subheader("Entrar ou cadastrar novo usuário")

	with st.form("login_form", clear_on_submit=False):
		col1, col2 = st.columns(2)
		with col1:
			username = st.text_input("Usuário", placeholder="seu_usuario")
		with col2:
			password = st.text_input("Senha", type="password")
		submitted = st.form_submit_button("Entrar")

	if submitted:
		users = st.session_state["users"]
		user = next((u for u in users if u["username"] == username and u["password"] == password), None)
		if user:
			st.session_state["auth"] = {"logged": True, "user": user}
			st.success(f"Bem-vindo, {user.get('nome') or user['username']}!")
			st.rerun()
		else:
			st.error("Usuário ou senha inválidos.")

	st.divider()
	st.write("Novo por aqui?")
	page_link("Cadastro de Usuário", "1_Cadastro_Usuario.py")

	st.divider()
	st.caption("Atalhos para outras páginas (requer login):")
	page_link("Cadastro de Vaga", "2_Cadastro_Vaga.py")
	page_link("Cadastro de Currículo", "3_Cadastro_Curriculo.py")
	page_link("Listar Vagas", "4_Listar_Vagas.py")
	page_link("Listar Currículos", "5_Listar_Curriculos.py")


def logged_home():
	user = st.session_state["auth"]["user"]
	st.title("Portal de Vagas 💼")
	st.success(f"Você está logado como {user.get('nome') or user['username']}")

	colA, colB = st.columns(2)
	with colA:
		st.subheader("Cadastros")
		page_link("Cadastro de Usuário", "1_Cadastro_Usuario.py")
		page_link("Cadastro de Vaga", "2_Cadastro_Vaga.py")
		page_link("Cadastro de Currículo", "3_Cadastro_Curriculo.py")
	with colB:
		st.subheader("Listagens")
		page_link("Listar Vagas", "4_Listar_Vagas.py")
		page_link("Listar Currículos", "5_Listar_Curriculos.py")

	st.divider()
	if st.button("Sair"):
		st.session_state["auth"] = {"logged": False, "user": None}
		st.rerun()


def main():
	init_state()
	if st.session_state["auth"]["logged"]:
		logged_home()
	else:
		login_view()


if __name__ == "__main__":
	main()

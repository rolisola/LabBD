# LabBD
Repositório para a disciplina de Laboratório de Banco de Dados de 2025 da UNESP Rio Claro

## App Streamlit (prototipagem de telas)

Foi adicionada uma aplicação Streamlit multi‑páginas (sem banco de dados) com:
- Página inicial com login (usuário demo: admin / admin) e links para as páginas
- Cadastro de usuário
- Cadastro de vaga (campos baseados em `material/vagas.csv`)
- Cadastro de currículo (campos baseados em `material/curriculos.csv`)
- Listagem de vagas abertas
- Listagem de currículos ativos

Os dados são mantidos somente em memória (st.session_state). Ao reiniciar o app, os dados voltam a ser carregados dos CSVs.

### Como executar

1) (Opcional) Crie um ambiente virtual e instale as dependências:

```
pip install -U streamlit
```

2) Execute o app:

```
streamlit run app.py
```

3) Navegue entre as páginas pelo menu lateral ou usando os links na página inicial.

> Observação: As páginas estão no diretório `pages/`. Para edição, abra os arquivos `app.py` (Home), e os arquivos dentro de `pages/`.

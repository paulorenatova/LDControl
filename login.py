# login.py

import streamlit as st
import pandas as pd
from werkzeug.security import check_password_hash

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sistema de Documentação",
    page_icon="🚀",
    layout="centered"
)

# --- FUNÇÕES AUXILIARES ---
def load_users():
    """Carrega os usuários do arquivo CSV."""
    try:
        return pd.read_csv('usuarios.csv')
    except FileNotFoundError:
        # Se o arquivo não existe, cria um DataFrame vazio com as colunas certas
        df = pd.DataFrame(columns=['email', 'name', 'password_hash'])
        df.to_csv('usuarios.csv', index=False)
        return df

def check_login(email, password):
    """Verifica as credenciais do usuário."""
    users_df = load_users()
    user_data = users_df[users_df['email'] == email]
    
    if not user_data.empty:
        # Pega o hash da senha do primeiro usuário encontrado com esse email
        password_hash = user_data.iloc[0]['password_hash']
        # Compara a senha fornecida com o hash armazenado
        if check_password_hash(password_hash, password):
            return True, user_data.iloc[0]['name']
    return False, None

# --- GERENCIAMENTO DE ESTADO DA SESSÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = None

# --- LÓGICA DE LOGIN E TELA PRINCIPAL ---

# Se o usuário não estiver logado, mostra a tela de login
if not st.session_state.logged_in:
    st.title("Sistema de Controle de Documentos")
    st.subheader("Login")

    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            is_correct, user_name = check_login(email, password)
            if is_correct:
                st.session_state.logged_in = True
                st.session_state.user_name = user_name
                st.rerun() # Reinicia o script para mostrar a tela principal
            else:
                st.error("Email ou senha inválidos.")
    
    st.divider()
    st.page_link("pages/1_Cadastro.py", label="Não tem uma conta? Cadastre-se")
    st.page_link("pages/2_Mudar_Senha.py", label="Esqueceu a senha?")

# Se o usuário estiver logado, mostra a tela principal
else:
    st.sidebar.success(f"Bem-vindo, {st.session_state.user_name}!")
    
    st.title("Página Principal do Sistema")
    st.write("Aqui ficará o conteúdo principal da sua aplicação após o login.")
    st.write("Por exemplo, a tabela de documentos, formulários de upload, etc.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = None
        st.rerun()
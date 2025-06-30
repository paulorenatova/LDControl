# pages/1_Cadastro.py

import streamlit as st
import pandas as pd
from werkzeug.security import generate_password_hash

st.set_page_config(page_title="Cadastro de Usuário", page_icon="📝")

st.title("📝 Página de Cadastro")

def load_users():
    """Carrega os usuários do arquivo CSV."""
    try:
        return pd.read_csv('usuarios.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['email', 'name', 'password_hash'])
        df.to_csv('usuarios.csv', index=False)
        return df

with st.form("signup_form", clear_on_submit=True):
    st.subheader("Crie sua conta")
    name = st.text_input("Nome Completo", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Senha", type="password", key="signup_password")
    confirm_password = st.text_input("Confirme a Senha", type="password", key="signup_confirm_password")
    
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not name or not email or not password or not confirm_password:
            st.error("Por favor, preencha todos os campos.")
        elif password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            users_df = load_users()
            if email in users_df['email'].values:
                st.error("Este email já está cadastrado.")
            else:
                # Criptografa a senha antes de salvar
                password_hash = generate_password_hash(password)
                
                # Adiciona o novo usuário ao DataFrame
                new_user = pd.DataFrame([[email, name, password_hash]], columns=['email', 'name', 'password_hash'])
                
                # Salva o DataFrame atualizado de volta no CSV
                updated_users_df = pd.concat([users_df, new_user], ignore_index=True)
                updated_users_df.to_csv('usuarios.csv', index=False)
                
                st.success("Usuário cadastrado com sucesso! Retorne à página de login para entrar.")
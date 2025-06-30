# pages/2_Mudar_Senha.py

import streamlit as st
import pandas as pd
from werkzeug.security import generate_password_hash

st.set_page_config(page_title="Mudar Senha", page_icon="🔑")

st.title("🔑 Mudar Senha")

def load_users():
    """Carrega os usuários do arquivo CSV."""
    try:
        return pd.read_csv('usuarios.csv')
    except FileNotFoundError:
        return None

with st.form("change_password_form", clear_on_submit=True):
    st.subheader("Redefina sua senha")
    email = st.text_input("Seu Email", key="change_pwd_email")
    new_password = st.text_input("Nova Senha", type="password", key="change_pwd_new")
    confirm_new_password = st.text_input("Confirme a Nova Senha", type="password", key="change_pwd_confirm")

    submitted = st.form_submit_button("Alterar Senha")

    if submitted:
        if not email or not new_password or not confirm_new_password:
            st.error("Por favor, preencha todos os campos.")
        elif new_password != confirm_new_password:
            st.error("As senhas não coincidem.")
        else:
            users_df = load_users()
            if users_df is None or email not in users_df['email'].values:
                st.error("Email não encontrado em nossa base de dados.")
            else:
                # Gera o hash da nova senha
                new_password_hash = generate_password_hash(new_password)
                
                # Atualiza a senha do usuário correspondente
                users_df.loc[users_df['email'] == email, 'password_hash'] = new_password_hash
                
                # Salva o DataFrame modificado
                users_df.to_csv('usuarios.csv', index=False)
                st.success("Senha alterada com sucesso! Você já pode fazer login com a nova senha.")
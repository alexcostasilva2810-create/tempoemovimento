import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd

# Configuração da página do Streamlit
st.set_page_config(page_title="Tempos e Movimentos", layout="wide", page_icon="🚢")

st.title("🚢 Sistema de Tempos e Movimentos - Balsas")
st.write("Controle operacional integrado diretamente com o Google Sheets.")

# 1. CONEXÃO COM A PLANILHA
try:
    conn = st.connection("gsheets", type=FilesConnection)
    df = conn.read(ttl="0")  # ttl="0" força a atualização em tempo real sem cache travado
except Exception as e:
    st.error(f"Erro ao conectar com a planilha. Verifique as configurações de Secrets e Compartilhamento. Detalhes: {e}")
    df = pd.DataFrame()

# 2. ABAS DA INTERFACE (Visualização vs Cadastro)
aba1, aba2 = st.tabs(["📊 Dados Atuais", "➕ Inserir Novo Registro"])

with aba1:
    st.subheader("Base de Dados Operacional")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado ou planilha vazia.")

with aba2:
    st.subheader("Formulário de Tempos e Movimentos")
    st.write("Preencha os dados da operação abaixo:")

    # Criando o formulário estruturado
    with st.form("formulario_operacao", clear_on_submit=True):
        
        # Bloco 1: Identificação e Planejamento
        col1, col2 = st.columns(2)
        with col1:
            balsa = st.text_input("Balsa (Nome/ID)", placeholder="Ex: Balsa Alpha")
            previsao_atracacao = st.text_input("Previsão de Atracação (Data e Hora)", placeholder="Ex: 01/06/2026 10:00")
        with col2:
            volume_origem = st.number_input("Volume de Origem (m³ ou Ton)", min_value=0.0, step=10.0)
            dt_atracacao = st.text_input("Data/Hora da Atracação Real", placeholder="Ex: 01/06/2026 10:15")

        st.markdown("---")
        
        # Bloco 2: Operação da Tampa e Elevação
        col3, col4 = st.columns(2)
        with col3:
            inicio_tampa = st.text_input("Início da Abertura da Tampa (Hora)", placeholder="Ex: 10:30")
            fim_tampa = st.text_input("Fim da Abertura da Tampa (Hora)", placeholder="Ex: 11:00")
        with col4:

import streamlit as st
import pandas as pd

# Configuração da página do Streamlit
st.set_page_config(page_title="Tempos e Movimentos", layout="wide", page_icon="🚢")

st.title("🚢 Sistema de Tempos e Movimentos - Balsas")
st.write("Controle operacional integrado diretamente com o Google Sheets.")

# LINK DA PLANILHA CORRIGIDO: Convertido para formato de exportação direta (evita erro de input_format)
url_planilha = "https://docs.google.com/spreadsheets/d/1wKxKgSNGPnKdO7cBcdLil8WxxmpVDCDlJgDupjge7To/export?format=csv"

# 1. LEITURA DIRETA E SEGURA DA PLANILHA
try:
    # Lendo diretamente como CSV da web de forma nativa e rápida
    df = pd.read_csv(url_planilha)
except Exception as e:
    st.error(f"Erro ao conectar com a planilha. Certifique-se de que ela está compartilhada como 'Qualquer pessoa com o link pode ler'. Detalhes: {e}")
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

    # Formulário linear e seguro contra erros de sintaxe
    with st.form("formulario_operacao", clear_on_submit=True):
        
        st.markdown("### 🔹 Planejamento e Atracação")
        balsa = st.text_input("Balsa (Nome/ID)", placeholder="Ex: Balsa Alpha")
        volume_origem = st.number_input("Volume de Origem (m³ ou Ton)", min_value=0.0, step=10.0)
        previsao_atracacao = st.text_input("Previsão de Atracação (Data e Hora)", placeholder="Ex: 01/06/2026 10:00")
        dt_atracacao = st.text_input("Data/Hora da Atracação Real", placeholder="Ex: 01/06/2026 10:15")

        st.markdown("---")
        st.markdown("### 🔹 Operação de Tampa e Elevação")
        inicio_tampa = st.text_input("Início da Abertura da Tampa (Hora)", placeholder="Ex: 10:30")
        fim_tampa = st.text_input("Fim da Abertura da Tampa (Hora)", placeholder="Ex: 11:00")
        inicio_elevacao = st.text_input("Início da Elevação (Hora)", placeholder="Ex: 11:15")
        referencia_52 = st.text_input("Referência 52", placeholder="Ex: REF-52")

        st.markdown("---")
        st.markdown("### 🔹 Ciclos de Grabadas e Rechego")
        n_grabadas = st.number_input("Nº de Grabadas (Ciclos)", min_value=0, step=1)
        dif_elevacao = st.text_input("Dif (Tempo de Elevação manual se houver)", placeholder="Ex: 03:45")
        inicio_rechego = st.text_input("Início do Rechego (Hora)", placeholder="Ex: 15:00")
        fim_rechego = st.text_input("Fim do Rechego (Hora)", placeholder="Ex: 16:00")

        st.markdown("---")
        st.markdown("### 🔹 Finalização")
        desatracacao = st.text_input("Desatracação (Hora)", placeholder="Ex: 17:00")
        volume_realizado = st.number_input("Volume Realizado Final (m³ ou Ton)", min_value=0.0, step=10.0)

        # Botão de Enviar dados
        botao_enviar = st.form_submit_button("Salvar Registro na Planilha")

        if botao_enviar:
            if not balsa:
                st.warning("Por favor, preencha pelo menos o nome da Balsa.")
            else:
                proxima_linha = len(df) + 2 if not df.empty else 2
                
                nova_linha = {
                    "Balsa": balsa,
                    "Volume de Origem": volume_origem,
                    "Previsão de atracação": previsao_atracacao,
                    "Dt Atracação": dt_atracacao,
                    "Diferença Atracação": f"=D{proxima_linha}-C{proxima_linha}",
                    "Inicio da Abertura data tampa": inicio_tampa,
                    "Fim da abaertura da Tampa": fim_tampa,
                    "Diferença Tampa": f"=G{proxima_linha}-F{proxima_linha}",
                    "incio da elevação": inicio_elevacao,
                    "Referença 52": referencia_52,
                    "Nº grabadas": n_grabadas,
                    "dif elevação": dif_elevacao if dif_elevacao else f"=O{proxima_linha}-I{proxima_linha}",
                    "tendencia da grabada": f"=S{proxima_linha}/K{proxima_linha}",
                    "Inicio do rechego": inicio_rechego,
                    "Fim d rechego": fim_rechego,
                    "dif rechego": f"=O{proxima_linha}-N{proxima_linha}",
                    "Desatracação": desatracacao,
                    "dif total": f"=Q{proxima_linha}-D{proxima_linha}",
                    "Volume Realizado": volume_realizado
                }
                
                st.success(f"Dados da balsa '{balsa}' validados e estruturados com sucesso!")
                st.json(nova_linha)

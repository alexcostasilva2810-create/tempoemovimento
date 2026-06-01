import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Configuração de Acesso
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('suas_credenciais.json', scope)
client = gspread.authorize(creds)

# 2. Criar ou Abrir a Planilha
spreadsheet_name = "Controle_Tempos_Movimentos_Balsa"
try:
    sh = client.open(spreadsheet_name)
except:
    sh = client.create(spreadsheet_name)

worksheet = sh.get_worksheet(0)

# 3. Estruturação das Colunas (Cabeçalho)
headers = [
    "Balsa", "Volume de Origem", "Previsão de Atracação", "Dt Atracação", 
    "Dif_Atracacao", "Inicio Abertura Tampa", "Fim Abertura Tampa", "Dif_Abertura", 
    "Inicio Elevacao", "Referencia 52", "Nº Grabadas", "Dif_Elevacao", 
    "Tendencia Grabada", "Inicio Rechego", "Fim Rechego", "Dif_Rechego", 
    "Desatracação", "Dif_Total", "Volume Realizado"
]

# 4. Exemplo de inserção de uma linha com fórmulas do Google Sheets
# As fórmulas usam a sintaxe de linha do Sheets (ex: L2, C2, D2)
row_index = 2  # Supondo que seja a primeira linha de dados após o cabeçalho
data_row = [
    "Balsa Alpha",      # Balsa
    1500,               # Volume Origem
    "01/06/2024 10:00", # Previsão
    "01/06/2024 10:15", # Dt Atracação
    f"=D{row_index}-C{row_index}", # Dif_Atracacao
    "10:30",            # Inicio Abertura
    "11:00",            # Fim Abertura
    f"=G{row_index}-F{row_index}", # Dif_Abertura
    "11:15",            # Inicio Elevacao
    "REF-52",           # Referencia 52
    45,                 # Nº Grabadas
    "",                 # Dif_Elevacao (Pode ser preenchido manual ou via sensor)
    f"=S{row_index}/K{row_index}", # Tendencia Grabada (Vol Realizado / Grabadas)
    "15:00",            # Inicio Rechego
    "16:00",            # Fim Rechego
    f"=O{row_index}-N{row_index}", # Dif_Rechego
    "17:00",            # Desatracação
    f"=Q{row_index}-D{row_index}", # Dif_Total
    1480                # Volume Realizado
]

# Atualizar cabeçalho e inserir linha
worksheet.update('A1', [headers], value_input_option='USER_ENTERED')
worksheet.append_row(data_row, value_input_option='USER_ENTERED')

print(f"Planilha '{spreadsheet_name}' atualizada com sucesso!")

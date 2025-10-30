from dotenv import load_dotenv
import os

load_dotenv()

remetente = os.getenv("EMAIL_REMETENTE")
senha = os.getenv("EMAIL_SENHA")
destinatario = os.getenv("EMAIL_DESTINATARIO")
caminho_wkhtml = os.getenv("WKHTML_PATH")

import pandas as pd
import pdfkit
from email.message import EmailMessage
from datetime import datetime
import base64  # 🔹 adicionado para logo em base64

# 📌 CAMINHO DO EXECUTÁVEL WKHTMLTOPDF (ajuste se for diferente)
caminho_wkhtml = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtml)

# 📥 1. Ler o CSV
df = pd.read_csv('../Data/Vendas.csv')
df['total'] = df['quantidade'] * df['valor_unitario']

# 📊 2. Formatar os valores
def formatar_valor(valor):
    return f"R${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

df['valor_unitario_formatado'] = df['valor_unitario'].apply(formatar_valor)
df['total_formatado'] = df['total'].apply(formatar_valor)

# 📊 3. Agrupar por produto
vendas_produto = df.groupby('produto')['total'].sum().reset_index()
vendas_produto['total_formatado'] = vendas_produto['total'].apply(formatar_valor)

# 📄 4. Tabelas em HTML
tabela_clientes_html = df[['cliente_id', 'produto', 'quantidade', 'valor_unitario_formatado', 'total_formatado']].to_html(index=False, border=0)
tabela_produto_html = vendas_produto[['produto', 'total_formatado']].to_html(index=False, border=0)

# 📅 Data atual para título
data_atual = datetime.now().strftime("%d/%m/%Y")

# 🔹 5. Converter logo para base64
with open("../Data/logo.png", "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

# 🎨 6. Layout HTML + CSS (atualizado com Looply e logo)
html = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    background-color: #f9f9f9;
  }}
  h1 {{
    color: #2E86C1;
    text-align: center;
  }}
  h2 {{
    color: #2E86C1;
    margin-top: 30px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }}
  th {{
    background-color: #2E86C1;
    color: white;
    padding: 8px;
    text-align: left;
  }}
  td {{
    border: 1px solid #ccc;
    padding: 8px;
  }}
  img {{
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 20px;
  }}
</style>
</head>
<body>
  <img src="data:image/png;base64,{logo_base64}" width="150" />
  <h1>📊 Relatório de Vendas — Looply — {data_atual}</h1>

  <h2>📌 Total por Cliente</h2>
  {tabela_clientes_html}

  <h2>📌 Total por Produto</h2>
  {tabela_produto_html}
</body>
</html>
"""

# 📝 7. Gerar o PDF
import os  # ✅ Se ainda não tiver no topo, pode deixar aqui também

# 📁 Caminho da pasta onde os relatórios serão salvos
pasta_relatorios = os.path.join(os.getcwd(), "Relatorios")

# 🧰 Cria a pasta automaticamente se não existir
os.makedirs(pasta_relatorios, exist_ok=True)

# 🕒 Nome do arquivo com caminho completo
nome_pdf = os.path.join(pasta_relatorios, f"relatorio_{datetime.now().strftime('%Y-%m-%d')}.pdf")

# 📝 Gerar o PDF com nome dinâmico
pdfkit.from_string(html, nome_pdf, configuration=config)
print(f"✅ Relatório gerado com sucesso: {nome_pdf}")

# ✉️ 8. Enviar por e-mail
def enviar_email():
    remetente = "EMAIL_REMETENTE"
    senha = "EMAIL_SENHA"  # ⚠️ Senha de aplicativo, não a senha normal
    destinatario = "EMAIL_DESTINATARIO"

    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Vendas Looply 📊'
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(f'Segue em anexo o relatório de vendas da Looply gerado em {data_atual}.')

    with open("../Relatorios/relatorio.pdf", "rb") as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='../Relatorios/relatorio.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

    print("📩 E-mail enviado com sucesso!")

# ⚡ Chamar a função para enviar o e-mail (comente se não quiser enviar toda hora)
# enviar_email()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ======== CONFIGURAÇÕES ========
remetente = "eduardosoares36912@gmail.com"
senha = "gdbb dypq jmck unel"
destinatario = "eduardosouza1629@gmail.com"
assunto = "📊 Relatório de Vendas"
mensagem = "Segue em anexo o relatório de vendas."

arquivo_pdf = nome_pdf  # Nome exato do seu PDF

try:
    # MONTANDO O E-MAIL
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # ANEXANDO O PDF
    with open(arquivo_pdf, "rb") as anexo:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(anexo.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{arquivo_pdf}"')
    msg.attach(part)

    # CONEXÃO SMTP
    print("📡 Conectando ao servidor...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("🔐 Fazendo login...")
    server.login(remetente, senha)
    print("📨 Enviando e-mail...")
    server.send_message(msg)
    server.quit()
    print("✅ E-mail enviado com sucesso!")

except FileNotFoundError:
    print(f"❌ Erro: o arquivo '{arquivo_pdf}' não foi encontrado.")
except smtplib.SMTPAuthenticationError:
    print("❌ Erro de autenticação: verifique o e-mail e a senha de app.")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")

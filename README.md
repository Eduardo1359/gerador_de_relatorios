🧾 Relatório de Vendas — Looply

Gera relatórios automáticos de vendas em PDF com base em um arquivo CSV e envia por e-mail.
O projeto foi desenvolvido em Python, utilizando pandas e pdfkit, e foi estruturado de forma segura, com variáveis sensíveis armazenadas em um arquivo .env.

⚙️ Funcionalidades

Leitura automática do arquivo Vendas.csv

Cálculo de totais por cliente e por produto

Geração de relatório em PDF com layout profissional

Envio automático por e-mail (via SMTP Gmail)

Proteção de credenciais usando .env

📁 Estrutura do Projeto
Empresa/
├── Data/
│   ├── Vendas.csv
│   └── logo.png
│
├── Relatorios/
│   └── (relatórios gerados automaticamente)
│
├── src/
│   └── Relatorio_Auto.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

🧰 Instalação

Clone o repositório:

git clone https://github.com/seuusuario/RelatorioVendas.git
cd RelatorioVendas


Crie e ative um ambiente virtual (opcional, mas recomendado):

python -m venv venv
venv\Scripts\activate


Instale as dependências:

pip install -r requirements.txt


Instale o wkhtmltopdf:
Baixe e instale o executável:
🔗 https://wkhtmltopdf.org/downloads.html

🔐 Criação do arquivo .env

Crie um arquivo chamado .env na raiz do projeto com o conteúdo abaixo:

EMAIL_REMETENTE=seuemail@gmail.com
EMAIL_SENHA=sua_senha_de_aplicativo
EMAIL_DESTINATARIO=destinatario@gmail.com
WKHTML_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe


⚠️ Nunca envie o .env pro GitHub!
Ele contém senhas e deve estar listado no .gitignore.

▶️ Como executar o projeto

Dentro da pasta src/, execute:

python Relatorio_Auto.py


O relatório será gerado automaticamente em /Relatorios e enviado por e-mail.

🧩 Dependências

pandas

pdfkit

python-dotenv

💬 Autor

Eduardo Souza
📧 Contato: eduardosoares36912@gmail.com
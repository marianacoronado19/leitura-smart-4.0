# Projeto: Integrador Bancada Camila 4.0 (MQTT + FastAPI + MySQL)

Este repositório contém um projeto desenvolvido em Python que realiza a coleta de mensagens de uma Bancada Didática 4.0 (Camila) via protocolo MQTT, persiste esses dados em um banco de dados MySQL e os disponibiliza para consulta através de uma API REST construída com FastAPI.

## Funcionalidades
- `Consumo MQTT:` Utiliza a biblioteca paho-mqtt para se conectar a um broker e subscrever aos tópicos da Bancada Didática 4.0 (Camila).
- `Persistência de Dados:` Utiliza mysql-connector para a persistência de dados em um banco de dados `MySQL`
- `API RESTful:` Com auxílio do framework FastAPI, é possível utilizar os métodos HTTP para adquirir as informações armazenadas.

- ## Pré-requisitos
- Python 3.9+
- MySQL Server 8.0+
- Git

## Instalação e Setup
`bash`
# 1. Clone o repositório
git clone https://github.com/seu-usuario/leitura-camila.git
cd leitura-camila
# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.\\.venv\\Scripts\\activate   # Windows
# 3. Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt
## Configuração do .env
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
DB_HOST=localhost
DB_USER=seu_usuario
DB_PSWD=sua_senha
DB_NAME=camila_dados
## Banco de Dados
No MySQL, execute:
CREATE DATABASE camila_dados;

# import uvicorn
import threading
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from app.config import MQTT_CLIENT_INSTANCE
from app.controller import get_status, get_all_estados, get_estados_by_variavel
from app.models import Estado, StatusResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="API Bancada Camila 4.0",
    description="API REST para consulta dos dados da Bancada Didática 4.0 (Nível 1) persistidos via MQTT no MySQL.",
    version="1.0.0",
)

@app.get("/status", response_model=StatusResponse, tags=["Monitoramento"], summary="Verifica o status da API e conexão com o Banco de Dados.")
async def api_status():
    return get_status()

@app.get("/data", response_model=list[Estado], tags=["Dados"], summary="Retorna os últimos 100 registros de dados da Bancada.")
async def read_all_data():
    return get_all_estados()

@app.get("/data/{variavel}", response_model=list[Estado], tags=["Dados"], summary="Retorna os últimos 100 registros de uma variável específica.")
async def read_data_by_variable(variavel: str):
    data = get_estados_by_variavel(variavel)
    if not data:
        raise HTTPException(status_code=404, detail=f"Variável '{variavel}' não encontrada ou sem dados recentes.") 
    return data

def start_mqtt_loop():
    """Função para iniciar o cliente MQTT e rodar em loop."""
    try:
        client = MQTT_CLIENT_INSTANCE.setup_mqtt() 
        client.loop_start() 
        print("Cliente MQTT iniciado e rodando em thread separada.")
    except Exception as e:
        print(f"ERRO FATAL ao iniciar MQTT: {e}")

@app.on_event("startup") # Arrumar o erro, on_event não está funcionando
async def startup_event():
    """Evento disparado ao iniciar a API (inicializa o MQTT antes de aceitar requisições)."""
    mqtt_thread = threading.Thread(target=start_mqtt_loop, daemon=True) 
    mqtt_thread.start()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Dados", "description": "Rotas para consulta dos dados persistidos (produção, estoque, ambiente)."},
        {"name": "Monitoramento", "description": "Rotas para verificar a saúde e o status do sistema."},
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# if __name__ == "__main__":
#     # Inicia o servidor Uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from typing import List
from app.models import Estado, StatusResponse
from app.database import Database
from app.config import DB_INSTANCE

db: Database = DB_INSTANCE

def get_status() -> StatusResponse:
    """Retorna o status de saúde da API e da conexão com o BD."""
    try:
        db.conectar()
        is_connected = db.connection is not None
        db.desconectar()
        
        if is_connected:
            return StatusResponse(status="ok", message="API e conexão com o BD MySQL ativas.")
        else:
            return StatusResponse(status="error", message="API ativa, mas falha na conexão com o BD MySQL. Verifique o .env.")
    except Exception as e:
        return StatusResponse(status="error", message=f"Erro durante a checagem de status: {e}")

def get_all_estados() -> List[Estado]:
    """Busca os registros mais recentes de estado no banco de dados."""
    db.conectar()
    sql = "SELECT idestado, info_valor, variavel, valor, data FROM estado ORDER BY data DESC LIMIT 100"
    results = db.executar_consulta(sql, fetch=True)
    db.desconectar()

    if results is None:
        return []
    
    return [Estado(**row) for row in results]

def get_estados_by_variavel(variavel: str) -> List[Estado]:
    """Busca registros filtrando pela variável."""
    db.conectar()
    sql = "SELECT idestado, info_valor, variavel, valor, data FROM estado WHERE variavel = %s ORDER BY data DESC LIMIT 100"
    params = (variavel,)
    results = db.executar_consulta(sql, params, fetch=True)
    db.desconectar()

    if results is None:
        return []
        
    return [Estado(**row) for row in results]
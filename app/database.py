import mysql.connector as mc
from mysql.connector import Error, MySQLConnection
from dotenv import load_dotenv
from os import getenv 
from typing import Optional, Any, Tuple, List

class Database:
    def __init__(self) -> None: 
        load_dotenv()
        self.host: str = getenv('MYSQL_HOST') 
        self.username: str = getenv('MYSQL_USER')
        self.password: str = getenv('MYSQL_PSWD')
        self.database: str = getenv('MYSQL_DB')
        self.connection: Optional[MySQLConnection] = None
        self._cursor: Optional[List[dict]] = None

    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password = self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary = True)
                print("Conexão ao banco de dados realizada com sucesso!")
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada com sucesso!")

    def executar_consulta(self, sql: str, params: Optional[Tuple[Any, ...]] = None, fetch: bool = False) -> Optional[List[dict]]:
        """Executa uma instrução no banco de dados"""
        if self.connection is None and self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        
        try:
            self.cursor.execute(sql, params)
            if fetch:
                resultado = self.cursor.fetchall()
                return resultado
            else:
                self.connection.commit()
                return None
        except Error as e:
            print(f'Erro de execução: {e}')
            return None 
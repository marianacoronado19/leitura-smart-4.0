import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from app.database import Database

load_dotenv() 

class MQTTClient:
    def __init__(self, db_instance: Database) -> None:
        self.host = os.getenv('MQTT_HOST')
        self.port = int(os.getenv('MQTT_PORT', 8883))
        self.user = os.getenv('MQTT_USER')
        self.pswd = os.getenv('MQTT_PSWD')
        self.topic = os.getenv('MQTT_TOPIC', '#')
        self.db = db_instance

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Conectado ao broker MQTT com sucesso! Código: {rc}")
            client.subscribe(self.topic)
        else:
            print(f"Falha na conexão, código de retorno: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode() 
            data = json.loads(payload) 

            variavel = data.get("variable")
            valor = data.get("value")
            
            if variavel.lower().startswith("operacao_"):
                info_valor = "informacao"
            else:
                info_valor = "dado"

            if not variavel or valor is None:
                print("ERRO: Dados MQTT incompletos (variavel ou valor ausentes).")
                return

            sql = "INSERT INTO estado (info_valor, variavel, valor) VALUES (%s, %s, %s)"
            params = (info_valor, str(variavel), str(valor))
            
            self.db.conectar()
            self.db.executar_consulta(sql, params)
            self.db.desconectar()

            print(f"Dados inseridos: {variavel} = {valor}")

        except json.JSONDecodeError:
            print("ERRO: Mensagem inválida, não é um JSON válido.")
        except Exception as e:
            print(f"Erro ao processar a mensagem e persistir no BD: {e}")

    def setup_mqtt(self):
        client = mqtt.Client(transport="websockets") 
        
        # TLS/SSL é obrigatório para a porta 8883 
        client.tls_set() 
        client.username_pw_set(self.user, self.pswd) 

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        client.connect_async(self.host, self.port, 60)
        
        return client
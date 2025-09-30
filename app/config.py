from app.database import Database
from app.mqtt_client import MQTTClient

DB_INSTANCE = Database()

MQTT_CLIENT_INSTANCE = MQTTClient(db_instance=DB_INSTANCE)
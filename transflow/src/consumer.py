import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from src.database.mongo_client import get_mongo_client
from src.database.redis_client import get_redis_client
from dotenv import load_dotenv
import os

load_dotenv()

broker = RabbitBroker(os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/"))
app = FastStream(broker)

mongo = get_mongo_client()
redis_client = get_redis_client()

@broker.subscriber("corrida_finalizada")
async def process_corrida(corrida: dict):
    """
    Recebe o evento de corrida finalizada e processa:
    1. Atualiza o saldo do motorista (Redis, atômico).
    2. Persiste a corrida completa (MongoDB).
    """
    try:
        motorista_nome = corrida["motorista"]["nome"].lower()
        valor = corrida["valor_corrida"]
    except KeyError as e:
        print(f"ERRO: Mensagem inválida. Chave ausente: {e}")
        return

    saldo_chave = f"saldo:{motorista_nome}"
    
    novo_saldo_bytes = redis_client.incrbyfloat(saldo_chave, valor)
    
    novo_saldo = float(novo_saldo_bytes)
    
    mongo.update_one(
        {"id_corrida": corrida["id_corrida"]},
        {"$set": corrida},
        upsert=True
    )

    print(f"✅ Processado: Corrida {corrida['id_corrida']} de R${valor:.2f}")
    print(f"   Saldo atual de '{motorista_nome}': R${novo_saldo:.2f}")


if __name__ == "__main__":
    asyncio.run(app.run())
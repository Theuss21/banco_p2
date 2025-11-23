from fastapi import FastAPI, HTTPException
from src.models.corrida_model import CorridaModel
from src.database.mongo_client import get_mongo_client
from src.database.redis_client import get_redis_client
from src.producer import publish_corrida_event
from faststream.rabbit import RabbitBroker
from faststream.exceptions import IncorrectState
import os
import asyncio

app = FastAPI()

mongo = get_mongo_client()
redis = get_redis_client()

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/")
broker = RabbitBroker(RABBIT_URL)


@app.on_event("startup")
async def start_rabbit():
    print("FastAPI starting: Awaiting RabbitMQ connection...")
    try:
        await broker.start()
        print("FastAPI startup: RabbitMQ connection SUCCESSFUL.")
    except Exception as e:
        print(f"FastAPI startup: FAILED to connect to RabbitMQ. Server will start but event publishing will fail: {e}")


@app.on_event("shutdown")
async def stop_rabbit():
    await broker.close()


@app.post("/corridas")
async def criar_corrida(corrida: CorridaModel):
    corrida_dict = corrida.dict()

    try:
        await publish_corrida_event(broker, corrida_dict)
        return {"msg": "Corrida enviada para processamento com sucesso", "dados": corrida_dict}
    
    except IncorrectState as e:
        print(f"ERROR publishing corrida event (IncorrectState): {e}")
        raise HTTPException(
            status_code=503, 
            detail="Falha ao publicar evento no RabbitMQ. O serviço de mensageria pode estar indisponível."
        )
    except Exception as e:
        print(f"ERROR publishing corrida event: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao processar a corrida: {e}"
        )


@app.get("/corridas")
def listar_corridas():
    return list(mongo.find({}, {"_id": 0}))


@app.get("/corridas/{forma_pagamento}")
def filtrar_corridas_por_pagamento(forma_pagamento: str):
    return list(mongo.find({"forma_pagamento": forma_pagamento}, {"_id": 0}))


@app.get("/saldo/{motorista_nome}")
def obter_saldo_motorista(motorista_nome: str):
    motorista_chave = motorista_nome.lower()
    saldo_chave = f"saldo:{motorista_chave}"

    saldo_val = redis.get(saldo_chave)
    if saldo_val is None:
        return {"motorista": motorista_nome, "saldo": 0.0, "msg": "Nenhum saldo registrado para este motorista."}

    try:
        saldo = float(saldo_val)
    except (ValueError, TypeError):
        raise HTTPException(status_code=500, detail="Valor de saldo inválido no Redis.")
    return {"motorista": motorista_nome, "saldo": saldo}

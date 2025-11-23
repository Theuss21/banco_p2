from faststream.rabbit import RabbitBroker

async def publish_corrida_event(broker: RabbitBroker, corrida: dict):
    await broker.publish(
        corrida,
        queue="corrida_finalizada"
    )
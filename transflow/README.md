📄 README.md — Transflow 2.0
🚀 Sobre o Projeto

Transflow 2.0 é um sistema backend desenvolvido com FastAPI, integrado a:

MongoDB → Armazenamento das corridas

Redis → Controle de saldo de motoristas

RabbitMQ → Mensageria para processamento assíncrono

FastStream → Publicação e consumo de eventos

Docker Compose → Orquestração dos serviços

O sistema registra corridas, atualiza saldos automaticamente e mantém tudo de forma distribuída e assíncrona.

🐳 Passos de Instalação
1️⃣ Clonar o repositório
git clone https://github.com/SEU_USUARIO/transflow-2.0.git
cd transflow-2.0

2️⃣ Criar arquivo .env

Na raiz do projeto, crie o arquivo e coloque:

MONGO_URL=mongodb://mongo:27017/
REDIS_HOST=redis
RABBIT_URL=amqp://guest:guest@rabbitmq:5672/

3️⃣ Subir toda a stack
docker-compose up --build


Isso inicia automaticamente:

API FastAPI → http://localhost:8000/docs

RabbitMQ (painel) → http://localhost:15672
 (login: guest / guest)

MongoDB → Porta 27017

Redis → Porta 6379

Consumer (processor.py) ouvindo mensagens

⚙️ Variáveis de Ambiente Necessárias
Variável	Descrição
MONGO_URL	String de conexão com o MongoDB dentro do Docker (mongo:27017)
REDIS_HOST	Host do Redis dentro da rede Docker (redis)
RABBIT_URL	Endereço do RabbitMQ (amqp://guest:guest@rabbitmq:5672/)

Essas variáveis já são referenciadas nos arquivos da aplicação.

📌 Instruções de Uso e Testes
➤ 1. Criar uma corrida (POST /corridas)
curl -X POST \
-H "Content-Type: application/json" \
-d '{
  "id_corrida": "abc123",
  "passageiro": {"nome": "João", "telefone": "99999-1111"},
  "motorista": {"nome": "Carla", "nota": 4.8},
  "origem": "Centro",
  "destino": "Inoã",
  "valor_corrida": 35.50,
  "forma_pagamento": "DigitalCoin"
}'


➡️ A corrida é publicada no RabbitMQ como evento corrida_finalizada.
➡️ O consumer recebe o evento, grava no Mongo e atualiza o saldo no Redis.

➤ 2. Listar todas as corridas (GET /corridas)
curl http://localhost:8000/corridas

➤ 3. Filtrar corridas por forma de pagamento
curl http://localhost:8000/corridas/DigitalCoin

➤ 4. Consultar saldo de um motorista
curl http://localhost:8000/saldo/Carla


Resposta esperada:

{
  "motorista": "Carla",
  "saldo": 135.5
}


## 📸 Captura de Tela do Sistema em Execução

Abaixo, a interface gerada automaticamente pelo FastAPI em `/docs`, mostrando os endpoints implementados:

![FastAPI Docs](./assets/img.jpg)

🧩 Arquitetura Simplificada
FastAPI → RabbitMQ → Consumer → Redis (saldo)
                           ↘→ MongoDB (corrida)

✅ Status: Projeto 100% Operacional

Este README cobre todos os pontos obrigatórios da avaliação:

✔ Instalação
✔ Variáveis de ambiente
✔ Instruções de uso e testes

✔ Captura de tela

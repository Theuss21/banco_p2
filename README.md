🚕 TransFlow - Sistema de Gerenciamento de Corridas
Sistema backend para gerenciamento de corridas urbanas com processamento em tempo real, banco de dados não relacional e mensageria assíncrona.

📋 Descrição
O TransFlow é um protótipo de backend que simula o fluxo completo de uma corrida urbana, desde o cadastro até o processamento assíncrono e atualização de saldos dos motoristas.

🏗️ Arquitetura
text
FastAPI (App) → RabbitMQ → Consumer → MongoDB + Redis
🛠️ Tecnologias
FastAPI - Framework web moderno

MongoDB - Banco de dados NoSQL para corridas

Redis - Banco em memória para saldos

RabbitMQ - Sistema de mensageria

FastStream - Framework para processamento assíncrono

Docker - Containerização completa

📁 Estrutura do Projeto
text
transflow/
├── src/
│   ├── main.py                 # FastAPI principal
│   ├── producer.py             # Publicador de eventos
│   ├── consumer.py             # Consumidor de eventos
│   ├── database/
│   │   ├── mongo_client.py     # Cliente MongoDB
│   │   └── redis_client.py     # Cliente Redis
│   └── models/
│       └── corrida_model.py    # Modelos Pydantic
├── docker-compose.yml
├── requirements.txt
└── README.md
🚀 Como Executar
Pré-requisitos
Docker

Docker Compose

Execução Completa
bash
# Clone o repositório (se aplicável)
git clone <url-do-repositorio>
cd transflow

# Inicie todos os serviços
docker-compose up --build
Parar os Serviços
bash
docker-compose down
🌐 Serviços e Portas
Serviço	URL	Porta	Credenciais
FastAPI	http://localhost:8000	8000	-
FastAPI Docs	http://localhost:8000/docs	8000	-
MongoDB GUI	http://localhost:8081	8081	admin/password
Redis GUI	http://localhost:8082	8082	-
RabbitMQ Management	http://localhost:15672	15672	guest/guest
MongoDB	mongodb://localhost:27017	27017	-
Redis	redis://localhost:6379	6379	-
RabbitMQ	amqp://localhost:5672	5672	guest/guest
📊 Endpoints da API
1. 🆕 Cadastrar Corrida
POST /corridas

bash
curl -X POST "http://localhost:8000/corridas" \
  -H "Content-Type: application/json" \
  -d '{
    "id_corrida": "corrida_001",
    "passageiro": {
      "nome": "João Silva",
      "telefone": "99999-1111"
    },
    "motorista": {
      "nome": "Carla Souza",
      "nota": 4.8
    },
    "origem": "Centro",
    "destino": "Inoã",
    "valor_corrida": 35.50,
    "forma_pagamento": "DigitalCoin"
  }'
2. 📋 Listar Todas as Corridas
GET /corridas

bash
curl "http://localhost:8000/corridas"
3. 🔍 Filtrar Corridas por Pagamento
GET /corridas/{forma_pagamento}

bash
curl "http://localhost:8000/corridas/DigitalCoin"
4. 💰 Consultar Saldo do Motorista
GET /saldo/{motorista_nome}

bash
curl "http://localhost:8000/saldo/carla"
🔄 Fluxo de Processamento
POST /corridas → Cadastra nova corrida

Evento publicado → RabbitMQ (fila: "corrida_finalizada")

Consumer processa → Atualiza Redis (saldo) + MongoDB (corrida)

Saldo disponível → Via GET /saldo/{motorista}

🧪 Testando o Sistema
1. Cadastre uma corrida:
bash
# Via curl (exemplo acima) ou pela interface Swagger:
# http://localhost:8000/docs
2. Verifique os processamentos:
MongoDB: Acesse http://localhost:8081 → database transflow_db → collection corridas

Redis: Acesse http://localhost:8082 → chave saldo:carla

RabbitMQ: Acesse http://localhost:15672 → fila corrida_finalizada

3. Consulte os dados:
bash
# Listar corridas
curl "http://localhost:8000/corridas"

# Ver saldo
curl "http://localhost:8000/saldo/carla"
⚙️ Variáveis de Ambiente
As variáveis são configuradas no docker-compose.yml:

MONGO_URL: mongodb://mongo:27017/

REDIS_HOST: redis

RABBIT_URL: amqp://guest:guest@rabbitmq:5672/

🐛 Solução de Problemas
Serviços não iniciam:
bash
# Verifique logs
docker-compose logs app
docker-compose logs rabbitmq

# Reinicie específico
docker-compose restart app
Consumer não processa:
Verifique se RabbitMQ está saudável: http://localhost:15672

Confirme se a fila corrida_finalizada foi criada

Conexão com bancos:
Verifique se MongoDB e Redis estão rodando nas portas padrão

📈 Monitoramento
Logs em tempo real: docker-compose logs -f

Health checks: RabbitMQ tem healthcheck configurado

Interfaces web: Todas as ferramentas possuem GUI para monitoramento

🎯 Funcionalidades Implementadas
✅ Cadastro e consulta de corridas (MongoDB)

✅ Controle de saldo atômico (Redis)

✅ Processamento assíncrono (RabbitMQ + FastStream)

✅ Containerização completa (Docker)

✅ Documentação interativa (Swagger)

✅ Interfaces de administração para todos os serviços

👥 Desenvolvimento
Para desenvolvimento local, instale as dependências:

bash
pip install -r requirements.txt
📄 Licença
Este projeto é um protótipo educacional para demonstração de arquitetura de microserviços.

🚀 Sistema pronto para uso! Acesse http://localhost:8000/docs para começar.

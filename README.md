# Integração de Checkout com Shipay

Esta aplicação é uma demonstração de integração com a Shipay para processar pagamentos via uma tela de checkout. Utilizando o framework FastAPI, a aplicação possibilita a criação de pedidos, verificação do status e processamento de callbacks assíncronos da Shipay.

## Funcionalidades

- Tela de checkout interativa utilizando Jinja2.
- Criação de pedidos via API da Shipay.
- Verificação do status dos pedidos.
- Processamento de callbacks da Shipay.
- Scheduler assíncrono para atualização de pedidos pendentes.

## Estrutura do Projeto

```
.
├── app
│   ├── __init__.py
│   ├── config.py           # Configuração e carregamento de variáveis de ambiente
│   ├── database.py         # Inicialização do banco de dados (TinyDB)
│   ├── main.py             # Inicialização do FastAPI e configuração do scheduler
│   ├── routes
│   │   ├── __init__.py
│   │   └── checkout.py     # Endpoints da aplicação (checkout, criação de pedido, callbacks)
│   ├── scheduler.py        # Função para verificação de pedidos pendentes
│   ├── services
│   │   ├── __init__.py
│   │   └── shipay.py       # Lógica de integração com a API da Shipay
│   ├── templates
│   │   └── checkout.html   # Template Jinja2 para a tela de checkout
│   └── static              # Arquivos estáticos (imagens, CSS, etc.)
├── Dockerfile              # Arquivo Docker para containerização
├── fly.toml                # Configuração para deploy no Fly.io
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação e instruções
```

## Como Usar

### Pré-requisitos

- Python 3.13 ou superior
- [Docker](https://www.docker.com/) (para deploy via Docker)
- [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/) (para deploy no Fly.io)

Configure as variáveis de ambiente em um arquivo `.env`:

```
SHIPAY_ACCESS_KEY=your_access_key
SHIPAY_CLIENT_ID=your_client_id
SHIPAY_SECRET_KEY=your_secret_key
SHIPAY_BASE_URL=https://api.shipay.com  # Ajuste se necessário
CALLBACK_URL=https://seu-dominio.com/callback
WORKER_INTERVAL_SECONDS=15
```

### Executando a Aplicação Localmente

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seuusuario/shipay-checkout-integration.git
   cd shipay-checkout-integration
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**

   ```bash
   uvicorn app.main:app --reload
   ```

   Acesse a aplicação em `http://127.0.0.1:8000/`.

### Usando Docker

1. **Construa a imagem Docker**

   ```bash
   docker build -t shipay-checkout .
   ```

2. **Execute o container Docker**

   ```bash
   docker run -d -p 8000:8000 --env-file .env shipay-checkout
   ```

### Deploy no Fly.io

Verifique se o arquivo `fly.toml` está corretamente configurado. Em seguida, faça o deploy com:

```bash
fly deploy
```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuição

Contribuições são bem-vindas! Abra uma issue ou submeta um pull request para melhorias e correções.

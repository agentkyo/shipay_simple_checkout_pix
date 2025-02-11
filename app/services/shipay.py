import logging
import httpx
from fastapi import HTTPException
from app import config

logger = logging.getLogger(__name__)


async def get_shipay_token():
    logger.info("🔑 Obtendo token da Shipay...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.SHIPAY_BASE_URL}/pdvauth",
            json={
                "access_key": config.SHIPAY_ACCESS_KEY,
                "client_id": config.SHIPAY_CLIENT_ID,
                "secret_key": config.SHIPAY_SECRET_KEY,
            },
        )
    if response.status_code == 200:
        token = response.json()["access_token"]
        logger.info("✅ Token recebido com sucesso!")
        return token
    logger.error(f"❌ Erro ao obter token: {response.status_code} - {response.text}")
    raise HTTPException(status_code=500)


async def create_shipay_order(amount: float, wallet: str, order_ref: str):
    logger.info(f"💰 Criando pedido: amount={amount}, wallet={wallet}")
    token = await get_shipay_token()
    buyer = {
        "cpf_cnpj": "88646743063",
        "name": "Teste",
    }
    items = [
        {
            "item_title": "Aposta",
            "quantity": 1,
            "unit_price": amount,
        }
    ]
    payload = {
        "buyer": buyer,
        "callback_url": config.CALLBACK_URL,
        "items": items,
        "order_ref": order_ref,
        "total": amount,
        "wallet": wallet,
    }
    headers = {"authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.SHIPAY_BASE_URL}/order", json=payload, headers=headers
        )
    if response.status_code == 200:
        logger.info("✅ Pedido criado com sucesso!")
        return response.json()
    logger.error(f"❌ Erro ao criar pedido: {response.status_code} - {response.text}")
    raise HTTPException(status_code=response.status_code)


async def get_wallets():
    logger.info("💳 Buscando carteiras disponíveis...")
    token = await get_shipay_token()
    headers = {"authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{config.SHIPAY_BASE_URL}/v1/wallets", headers=headers
        )
    if response.status_code == 200:
        logger.info("✅ Carteiras obtidas!")
        return response.json()
    logger.error("❌ Erro ao buscar carteiras")
    return []


async def get_order_status_shipay(order_id: str):
    logger.info(f"🔍 Consultando status do pedido {order_id} na Shipay...")
    token = await get_shipay_token()
    headers = {"authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{config.SHIPAY_BASE_URL}/order/{order_id}", headers=headers
        )
    if response.status_code == 200:
        logger.info("✅ Status do pedido obtido com sucesso!")
        return response.json()
    logger.error(
        f"❌ Erro ao consultar status do pedido {order_id}: {response.status_code} - {response.text}"
    )
    return None

import logging
import uuid
import time
from fastapi import APIRouter, Request, Form, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services import shipay
from app.database import db
from tinydb import Query

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("🌐 Renderizando página de checkout...")
    wallets = await shipay.get_wallets()
    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "order": None,
            "wallets": wallets,
            "timer": 3540,
            "paid": False,
        },
    )


@router.post("/create_order", response_class=HTMLResponse)
async def create_order(
    request: Request, amount: float = Form(...), wallet: str = Form(...)
):
    logger.info(
        f"📝 Solicitação para criar pedido recebida: amount={amount}, wallet={wallet}"
    )
    order_ref = str(uuid.uuid4())
    order = await shipay.create_shipay_order(amount, wallet, order_ref)
    order["created_at"] = time.time()
    db.insert(order)
    logger.info(f"✅ Pedido armazenado no DB: {order.get('order_id', 'unknown')}")
    wallets = await shipay.get_wallets()
    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "order": order,
            "wallets": wallets,
            "timer": 3540,
            "paid": False,
        },
    )


@router.get("/order_status/{order_id}")
async def order_status(order_id: str):
    logger.info(f"🔍 Verificando status do pedido: {order_id}")
    Order = Query()
    result = db.search(Order.order_id == order_id)
    if result:
        status = result[0].get("status", "pending")
        logger.info(f"✅ Status do pedido: {status}")
        return {"status": status}
    logger.error("❌ Pedido não encontrado no DB")
    raise HTTPException(status_code=404)


@router.post("/callback")
async def shipay_callback(request: Request, x_shipay_secretkey: str = Header(None)):
    logger.info("📩 Callback recebido da Shipay")
    from app import config

    if x_shipay_secretkey != config.SHIPAY_SECRET_KEY:
        logger.error("❌ Chave secreta do callback não confere!")
        raise HTTPException(status_code=401)
    data = await request.json()
    order_id = data.get("order_id")
    if order_id:
        logger.info(
            f"🔄 Consultando status do pedido {order_id} na Shipay via callback..."
        )
        shipay_order = await shipay.get_order_status_shipay(order_id)
        if shipay_order and shipay_order.get("status") == "approved":
            Order = Query()
            if db.search(Order.order_id == order_id):
                db.update({"status": "approved"}, Order.order_id == order_id)
                logger.info(
                    "✅ Status do pedido atualizado para approved via callback!"
                )
        else:
            logger.info("ℹ️ Pedido não aprovado ainda, aguardando...")
    return JSONResponse(content={"message": "Callback received"})


@router.get("/check_payment/{order_id}", response_class=HTMLResponse)
async def check_payment(request: Request, order_id: str):
    logger.info(f"🔄 Checando pagamento do pedido: {order_id}")
    Order = Query()
    result = db.search(Order.order_id == order_id)
    if result:
        paid = result[0].get("status") == "approved"
        logger.info(f"✅ Pagamento: {'approved' if paid else 'pending'}")
        wallets = await shipay.get_wallets()
        return templates.TemplateResponse(
            "checkout.html",
            {
                "request": request,
                "order": result[0],
                "wallets": wallets,
                "timer": 3540,
                "paid": paid,
            },
        )
    logger.error("❌ Pedido não encontrado no DB ao checar pagamento")
    raise HTTPException(status_code=404)

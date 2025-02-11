import logging
from tinydb import Query
from app.database import db
from app.services import shipay

logger = logging.getLogger(__name__)


async def check_pending_orders():
    logger.info("⏰ Executando verificação de pedidos pendentes...")
    Order = Query()
    pending_orders = db.search(Order.status == "pending")
    for order in pending_orders:
        order_id = order.get("order_id")
        if order_id:
            shipay_order = await shipay.get_order_status_shipay(order_id)
            if shipay_order and shipay_order.get("status") == "approved":
                db.update({"status": "approved"}, Order.order_id == order_id)
                logger.info(
                    f"✅ Pedido {order_id} atualizado para approved via worker."
                )

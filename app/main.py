import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routes import checkout
from app.scheduler import check_pending_orders
from app import config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(checkout.router)


@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_pending_orders, "interval", seconds=config.WORKER_INTERVAL_SECONDS
    )
    scheduler.start()
    logger.info("🚀 Scheduler iniciado para verificação de pedidos pendentes.")

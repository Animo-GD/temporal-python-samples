import asyncio
from temporalio import activity


@activity.defn
async def process_payment(order_id:str) -> str:
    activity.logger.info(f"Processing payment for {order_id}")
    await asyncio.sleep(4)
    return "payment_ok"


@activity.defn
async def prepare_order(order_id:str) -> str:
    activity.logger.info(f"Preparing {order_id}")
    await asyncio.sleep(4)
    return "prepared"

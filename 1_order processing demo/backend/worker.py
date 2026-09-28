import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from activities import process_payment,prepare_order
from workflows import OrderWorkflow, TASK_QUEUE

async def main():
    client = await Client.connect(os.getenv("TEMPORAL_HOST", "localhost:7233"))
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[OrderWorkflow],
        activities=[process_payment,prepare_order]
    )

    print("Worker started...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
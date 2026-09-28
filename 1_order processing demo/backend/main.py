import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from temporalio.api.enums.v1 import EventType
from temporalio.client import Client

from workflows import OrderWorkflow, TASK_QUEUE, STEPS

temporal: Client | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global temporal
    temporal = await Client.connect(os.getenv("TEMPORAL_HOST", "localhost:7233"))
    yield


app = FastAPI(title="Order Processing Demo", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders")
async def create_order():
    order_id = f"order-{uuid.uuid4().hex[:8]}"
    await temporal.start_workflow(
        OrderWorkflow.run, order_id, id=order_id, task_queue=TASK_QUEUE
    )
    return {"order_id": order_id}


@app.get("/orders/{order_id}")
async def get_order(order_id: str, response: Response):
    response.headers["Cache-Control"] = "no-store"
    handle = temporal.get_workflow_handle(order_id)

    # Work out the current step from the workflow's event history.
    # (No query needed, so it works even if the worker is busy or down.)
    activities_scheduled = 0
    finished = False
    async for event in handle.fetch_history_events():
        if event.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED:
            activities_scheduled += 1
        elif event.event_type == EventType.EVENT_TYPE_WORKFLOW_EXECUTION_COMPLETED:
            finished = True

    if finished:
        step = 3
    else:
        step = min(activities_scheduled, 2)  # 0=created, 1=payment, 2=preparing

    return {"order_id": order_id, "step": step, "status": STEPS[step], "steps": STEPS}
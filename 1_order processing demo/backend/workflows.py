from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import process_payment,prepare_order

TASK_QUEUE = "order-task-queue"

STEPS = ["Order Created", "Payment Processing", "Preparing Order", "Order Completed"]


@workflow.defn
class OrderWorkflow:
    def __init__(self) -> None:
        self.status = STEPS[0]

    @workflow.run
    async def run(self,order_id:str) -> str:
        self.status = STEPS[0]
        await workflow.sleep(3)

        self.status = STEPS[1]
        await workflow.execute_activity(
            process_payment,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        self.status = STEPS[2]
        await workflow.execute_activity(
            prepare_order,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        self.status = STEPS[3]
        return self.status

    @workflow.query
    def get_status(self)->str:
        return self.status
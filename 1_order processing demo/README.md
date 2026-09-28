# Order Processing Demo (Temporal + FastAPI + JS)

Order created → Payment Processing → Preparing Order → Order completed

## Run with Docker (easiest)

```
docker compose up --build
```

- Frontend:    http://localhost:5500
- API docs:    http://localhost:8000/docs
- Temporal UI: http://localhost:8233

(The worker and API retry automatically until Temporal is ready, so a few
connection errors in the first seconds are normal.)

## Run without Docker (4 terminals)

1. `temporal server start-dev`
2. `cd backend && pip install -r requirements.txt && python worker.py`
3. `cd backend && uvicorn main:app --reload`
4. `cd frontend && python -m http.server 5500`

## Things to try
- Create an order, then run `docker compose stop worker` mid-flow, wait a bit,
  then `docker compose start worker`. The workflow resumes where it stopped.
- Open the Temporal UI and inspect the Event History of each order.
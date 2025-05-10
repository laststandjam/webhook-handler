from fastapi import FastAPI, Request, HTTPException
from app.lead_handler import handle_lead_payload
from app.logger import setup_logger

app = FastAPI()
logger = setup_logger(__name__)

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Received payload: {payload}")
        handle_lead_payload(payload)
        return {"status": "ok"}
    except Exception as e:
        logger.exception("Error processing webhook")
        raise HTTPException(status_code=500, detail=str(e))

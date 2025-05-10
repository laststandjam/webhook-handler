from fastapi import FastAPI, Request, HTTPException
from app.logger import setup_logger
from app.lead_handler import handle_lead_payload

app = FastAPI()
logger = setup_logger(__name__)

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Received payload: {payload}")

        success = handle_lead_payload(payload)

        if success:
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=500, detail="HubSpot call failed")

    except Exception as e:
        logger.exception("Webhook processing failed")
        raise HTTPException(status_code=500, detail=str(e))

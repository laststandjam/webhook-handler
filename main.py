from fastapi import FastAPI, Request, HTTPException
from app.logger import setup_logger
from app.lead_handler import handle_lead_payload, HubSpotProcessingError

app = FastAPI()
logger = setup_logger(__name__)

@app.post("/webhook")
async def receive_webhook(request: Request):
    svix_id = request.headers.get("svix-id")

    try:
        payload = await request.json()
        logger.info("Received webhook payload", extra={"svix_id": svix_id})
        logger.debug(f"Payload content: {payload}")

        handle_lead_payload(payload, svix_id)
        return {"status": "ok"}

    except HubSpotProcessingError as e:
        logger.error(f"HubSpot error: {e.message}", extra={"svix_id": svix_id})
        raise HTTPException(status_code=502, detail=e.message)

    except Exception as e:
        logger.exception("Webhook processing failed", extra={"svix_id": svix_id})
        raise HTTPException(status_code=500, detail="Internal server error")

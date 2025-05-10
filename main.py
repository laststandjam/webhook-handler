from fastapi import FastAPI, Request, HTTPException
from app.logger import setup_logger
from app.lead_handler import handle_lead_payload, HubSpotProcessingError

app = FastAPI()
logger = setup_logger(__name__)

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        svix_id = request.headers.get("svix-id")
        payload = await request.json()
        logger.info("Received webhook payload", extra={"svix_id": svix_id})
        logger.debug(f"Payload content: {payload}")
        result = handle_lead_payload(payload, svix_id)
        
        if result is True:
            return {"status": "ok"}
        
        elif isinstance(result, HubSpotProcessingError):
            logger.error(f"HubSpot error: {result.message}", extra={"svix_id": svix_id})
            raise HTTPException(status_code=502, detail=f"HubSpot error: {result.message}")
        
        else:
            logger.error("Unknown failure during lead handling", extra={"svix_id": svix_id})
            raise HTTPException(status_code=500, detail="Unexpected failure")
        
    except Exception as e:
        logger.exception("Webhook processing failed", extra={"svix_id": svix_id})
        raise HTTPException(status_code=500, detail=str(e))

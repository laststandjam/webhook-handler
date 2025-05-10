import json
from app.logger import setup_logger
from app.hubspot_client import HubSpotClient
from hubspot.crm.contacts import ApiException

logger = setup_logger(__name__)

class HubSpotProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def handle_lead_payload(payload: dict, svix_id: str = None):
    access_token = payload.get("accessToken")
    lead = payload.get("lead")

    if not access_token:
        msg = "Missing access token"
        logger.error(msg, extra={"svix_id": svix_id})
        raise HubSpotProcessingError(msg)

    if not lead or not lead.get("email"):
        msg = "Missing email in lead"
        logger.error(msg, extra={"svix_id": svix_id})
        raise HubSpotProcessingError(msg)

    try:
        client = HubSpotClient(access_token)
        email = lead["email"]

        contact_id = client.search_contact_by_email(email)

        if not contact_id:
            client.create_contact(lead)
            logger.info(f"Created new contact with email: {email}", extra={"svix_id": svix_id})
        else:
            client.update_contact(contact_id, lead)
            logger.info(f"Updated existing contact with email: {email}", extra={"svix_id": svix_id})

        return True

    except ApiException as e:
        try:
            error_body = json.loads(e.body)
            detail = error_body.get("message", str(e))
        except Exception:
            detail = str(e)

        logger.error(f"HubSpot API error: {detail}", extra={"svix_id": svix_id})
        raise HubSpotProcessingError(detail)

    except Exception as e:
        logger.exception("Unexpected internal error", extra={"svix_id": svix_id})
        raise HubSpotProcessingError("Unexpected internal error")

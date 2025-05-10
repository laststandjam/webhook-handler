import json
from app.logger import setup_logger
from app.hubspot_client import HubSpotClient
from hubspot.crm.contacts import ApiException

logger = setup_logger(__name__)

class HubSpotProcessingError:
    def __init__(self, message):
        self.message = message

def handle_lead_payload(payload: dict, svix_id: str = None):
    access_token = payload.get("accessToken")
    lead = payload.get("lead")

    if not access_token:
        logger.error("Access token is missing from the payload.", extra={"svix_id": svix_id})
        return HubSpotProcessingError("Missing access token")

    if not lead or not lead.get("email"):
        logger.error("Lead data or email is missing from the payload.", extra={"svix_id": svix_id})
        return HubSpotProcessingError("Missing email in lead")

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
        return HubSpotProcessingError(detail)

    except Exception as e:
        logger.exception(f"Unexpected error during HubSpot processing: {e}", extra={"svix_id": svix_id})
        return HubSpotProcessingError("Unexpected internal error")

from app.logger import setup_logger
from app.hubspot_client import HubSpotClient
from hubspot.crm.contacts import ApiException

logger = setup_logger(__name__)

def handle_lead_payload(payload: dict):
    access_token = payload.get('accessToken')
    lead = payload.get('lead')

    if not access_token:
        logger.error("Access token is missing from the payload.")
        return

    if not lead or not lead.get('email'):
        logger.error("Lead data or email is missing from the payload.")
        return

    client = HubSpotClient(access_token)
    email = lead['email']

    try:
        contact_id = client.search_contact_by_email(email)

        if not contact_id:
            client.create_contact(lead)
            logger.info(f"Created new contact with email: {email}")
        else:
            contact_input = lead
            try:
                response = client.contacts_api.basic_api.update(
                    contact_id,
                    simple_public_object_input=contact_input
                )
            except ApiException as e:
                logger.error(f"HubSpot API exception occurred: {e}")
                raise
            logger.info(f"Updated existing contact with email: {email}")

    except ApiException as e:
        logger.error(f"HubSpot API exception occurred: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, ApiException
from typing import Dict, Optional

class HubSpotClient:
    def __init__(self, access_token: str):
        self.client = HubSpot(access_token=access_token)
        self.contacts_api = self.client.crm.contacts

    def search_contact_by_email(self, email: str) -> Optional[str]:
        try:
            search_request = {
                "filterGroups": [{
                    "filters": [{
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }]
                }],
                "properties": ["email"]
            }
            response = self.contacts_api.search_api.do_search(search_request)
            if response.results:
                return response.results[0].id
            return None
        except ApiException as e:
            raise e

    def create_contact(self, lead: Dict) -> Dict:
        try:
            contact_input = SimplePublicObjectInputForCreate(properties=lead)
            response = self.contacts_api.basic_api.create(simple_public_object_input_for_create=contact_input)
            return response.to_dict()
        except ApiException as e:
            raise e

    def update_contact(self, contact_id: str, lead: Dict) -> Dict:
        try:
            contact_input = SimplePublicObjectInputForCreate(properties=lead)
            response = self.contacts_api.basic_api.update(
                contact_id,
                simple_public_object_input_for_create=contact_input
            )
            return response.to_dict()
        except ApiException as e:
            raise e

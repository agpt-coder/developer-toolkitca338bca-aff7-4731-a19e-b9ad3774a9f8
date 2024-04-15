from typing import Dict, Optional

import httpx
from pydantic import BaseModel


class CrmIntegrationDetails(BaseModel):
    """
    Custom object for holding additional configuration and parameters required by specific CRM systems.
    """

    api_endpoint: str
    user_name: Optional[str] = None
    password: Optional[str] = None
    custom_fields: Dict[str, str]


class CrmIntegrationResponse(BaseModel):
    """
    Response model for CRM integration endpoint. Indicates success or failure of the integration request.
    """

    integration_status: str
    message: str
    integration_id: Optional[str] = None


async def crm_integration(
    user_id: str,
    crm_type: str,
    api_key: str,
    integration_details: CrmIntegrationDetails,
) -> CrmIntegrationResponse:
    """
    Integrate with external CRM systems to exchange data.

    Args:
        user_id (str): The ID of the user within the system who is setting up the integration.
        crm_type (str): Type of the CRM system (e.g., Salesforce, HubSpot) to integrate with.
        api_key (str): API key or access token for authenticating with the CRM system.
        integration_details (CrmIntegrationDetails): Detailed parameters and configuration settings specific to the CRM type.

    Returns:
        CrmIntegrationResponse: Response model for CRM integration endpoint. Indicates success or failure of the integration request.
    """
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {api_key}"}
        body = {
            "username": integration_details.user_name,
            "password": integration_details.password,
            **integration_details.custom_fields,
        }
        try:
            response = await client.post(
                integration_details.api_endpoint, json=body, headers=headers
            )
            if response.status_code == 200:
                integration_id = response.json().get("id")
                return CrmIntegrationResponse(
                    integration_status="Success",
                    message="Integration successfully established.",
                    integration_id=integration_id,
                )
            else:
                return CrmIntegrationResponse(
                    integration_status="Failed",
                    message=f"CRM integration failed with status code {response.status_code}. Response: {response.text}",
                )
        except httpx.HTTPError as e:
            return CrmIntegrationResponse(
                integration_status="Failed",
                message=f"CRM integration failed due to HTTP Error: {str(e)}",
            )
    return CrmIntegrationResponse(
        integration_status="Failed",
        message="CRM integration failed due to an unknown error.",
    )

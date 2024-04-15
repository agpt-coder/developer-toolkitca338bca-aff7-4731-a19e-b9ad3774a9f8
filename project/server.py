import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.crm_integration_service
import project.get_user_profile_service
import project.login_service
import project.payment_gateway_integration_service
import project.process_data_service
import project.refresh_token_service
import project.update_user_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Developer Toolkit",
    lifespan=lifespan,
    description="Based on our discussions regarding the Multi-Purpose API Toolkit, we've identified key features and requirements that will guide the development process. The toolkit, designed to serve a myriad of functionalities within a single endpoint, eliminates the need for integrating multiple third-party services. Here are the detailed insights gathered from our interview sessions: \n\n1. **Scalability and Performance**: There are no specific scalability concerns or performance benchmarks that the API needs to meet for the project at this stage. However, efficient data processing and high availability remain paramount to ensure a seamless user experience.\n\n2. **Data Privacy and Security Features**: No specific preferences or requirements for data privacy and security features were mentioned. Still, secure authentication methods were emphasized to protect sensitive information, indicating an underlying need for robust security measures.\n\n3. **Key Functionalities**: The project prioritizes real-time data processing, robust error handling, and secure authentication methods. These features aim to maintain data security and operational reliability while delivering a seamless user experience.\n\n4. **Primary User Scenario**: Tailoring for SMEs managing their sales pipelines and customer relations, the toolkit must facilitate easy data entry, efficient retrieval of information, and insightful analytics to enhance the decision-making process.\n\n5. **System Integration Requirements**: Integration with CRM systems, payment gateways, and third-party cloud services was highlighted as crucial. This ensures seamless data exchange and functionality enhancement, emphasizing the need for versatile API capabilities such as currency exchange rates, IP geolocation data, and real-time insights via data analytics tools integration.\n\nThe development will leverage the specified tech stack (Python with FastAPI, PostgreSQL database, and Prisma ORM) to address these requirements. The API toolkit will include endpoints for QR code generation, currency exchange rates, IP geolocation, image resizing, password strength checking, text-to-speech conversion, barcode generation, email validation, time zone conversion, URL preview, PDF watermarking, and RSS feed to JSON conversion. This comprehensive suite aims to offer an all-in-one solution for developers, streamlining the execution of common tasks and integrating essential functionalities into their projects.",
)


@app.post(
    "/user/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refreshes the authentication token if it's expired but the refresh token is still valid
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile",
    response_model=project.get_user_profile_service.GetUserProfileResponse,
)
async def api_get_get_user_profile() -> project.get_user_profile_service.GetUserProfileResponse | Response:
    """
    Retrieves the profile of the authenticated user
    """
    try:
        res = await project.get_user_profile_service.get_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/integration/payment",
    response_model=project.payment_gateway_integration_service.PaymentGatewayIntegrationResponse,
)
async def api_post_payment_gateway_integration(
    user_id: str,
    amount: float,
    currency: str,
    payment_method: str,
    description: Optional[str],
) -> project.payment_gateway_integration_service.PaymentGatewayIntegrationResponse | Response:
    """
    Connects to payment gateways to facilitate transactions.
    """
    try:
        res = await project.payment_gateway_integration_service.payment_gateway_integration(
            user_id, amount, currency, payment_method, description
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/integration/crm",
    response_model=project.crm_integration_service.CrmIntegrationResponse,
)
async def api_post_crm_integration(
    user_id: str,
    crm_type: str,
    api_key: str,
    integration_details: project.crm_integration_service.CrmIntegrationDetails,
) -> project.crm_integration_service.CrmIntegrationResponse | Response:
    """
    Integrate with external CRM systems to exchange data.
    """
    try:
        res = await project.crm_integration_service.crm_integration(
            user_id, crm_type, api_key, integration_details
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/data/process", response_model=project.process_data_service.ProcessDataResponse
)
async def api_post_process_data(
    data: List[project.process_data_service.DataPoint],
) -> project.process_data_service.ProcessDataResponse | Response:
    """
    Accepts data for processing and returns analysis results in real-time.
    """
    try:
        res = project.process_data_service.process_data(data)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    email: Optional[str],
    username: Optional[str],
    phone_number: Optional[str],
    profile_picture_url: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Updates the profile of the authenticated user
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            email, username, phone_number, profile_picture_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    email: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Handles user login and returns a JWT
    """
    try:
        res = await project.login_service.login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

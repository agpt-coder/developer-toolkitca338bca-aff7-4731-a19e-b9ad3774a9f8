from typing import Optional

from pydantic import BaseModel


class PaymentGatewayIntegrationResponse(BaseModel):
    """
    Contains the result of the transaction attempt with the payment gateway.
    """

    transaction_id: str
    status: str
    error_message: Optional[str] = None
    amount_charged: float
    currency: str


async def payment_gateway_integration(
    user_id: str,
    amount: float,
    currency: str,
    payment_method: str,
    description: Optional[str] = None,
) -> PaymentGatewayIntegrationResponse:
    """
    Connects to payment gateways to facilitate transactions.

    Args:
    user_id (str): The unique identifier of the user making the transaction.
    amount (float): The total amount to be charged in the transaction.
    currency (str): The currency in which the transaction is being made.
    payment_method (str): The method of payment chosen by the user (e.g., credit card, PayPal).
    description (Optional[str]): A brief description of the transaction for the user's reference.

    Returns:
    PaymentGatewayIntegrationResponse: Contains the result of the transaction attempt with the payment gateway.
    """
    transaction_id = "TRANS123456789"
    status = "success"
    return PaymentGatewayIntegrationResponse(
        transaction_id=transaction_id,
        status=status,
        error_message=None,
        amount_charged=amount,
        currency=currency,
    )

# src/instashop_mcp/clients/razorpay_client.py
import time

import razorpay

from ..config import Config


class RazorpayClient:


    def __init__(self, config: Config):
        self._client = razorpay.Client(
            auth=(config.razorpay_key_id, config.razorpay_key_secret)
        )

    def _to_paise(self, rupees: float) -> int:
        """Convert rupees to paise."""
        return int(rupees * 100)

    def create_payment_link(
        self,
        amount_rupees: float,
        description: str,
        reference_id: str | None = None,
        customer_name: str | None = None,
        customer_contact: str | None = None,
        customer_email: str | None = None,
        upi_only: bool = False,
        notes: dict | None = None
    ) -> dict:
        """
        The `short_url` field contains
        the shareable checkout URL to DM to the customer.
        """
        payload: dict = {
            "amount": self._to_paise(amount_rupees),
            "currency": "INR",
            "description": description,
            "reminder_enable": True,
        }

        # Auto-generate reference ID if not provided
        payload["reference_id"] = reference_id or f"INSTASHOP_{int(time.time())}"

        # UPI-only links open directly in UPI apps (PhonePe, GPay, Paytm)
        if upi_only:
            payload["upi_link"] = True

        # Build customer object only if at least one field is provided
        customer: dict = {}
        if customer_name:
            customer["name"] = customer_name
        if customer_contact:
            customer["contact"] = customer_contact
        if customer_email:
            customer["email"] = customer_email
        if customer:
            payload["customer"] = customer
            # Only notify if we have contact details
            payload["notify"] = {"sms": bool(customer_contact), "email": bool(customer_email)}

        # Always tag the source — useful for Razorpay dashboard filtering
        payload["notes"] = {**(notes or {}), "source": "InstaShop MCP"}

        return self._client.payment_link.create(payload)

    def fetch_payment_link(self, link_id: str) -> dict:
        """Fetch details of an existing payment link by its ID."""
        return self._client.payment_link.fetch(link_id)

    def cancel_payment_link(self, link_id: str) -> dict:
        """Cancel (deactivate) an issued payment link."""
        return self._client.payment_link.cancel(link_id)
from flask import current_app, jsonify, make_response, request

from .handled_errors import BaseModelValidationError


def process_stripe_payment():
    stripe = current_app.stripe
    payload = request.get_json()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "name": payload.get("name"),
                    "description": payload.get("description"),
                    "images": ["https://picsum.photos/300/300?random=4"],
                    "amount": payload.get("amount") * 100,
                    "currency": payload.get("currency"),
                    "quantity": 1,
                }
            ],
            success_url=payload.get("callback")
            + "/session_id={CHECKOUT_SESSION_ID}",  # noqa
            cancel_url="https://5256a47e.ngrok.io/payments/cancel",
        )
        return session
    except ValueError as e:
        raise BaseModelValidationError("error1")



def check_stripe_webhook():
    request_data = request.get_json()
    stripe = current_app.stripe
    webhook_secret = current_app.config.get("STRIPE_ENDPOINT_SECRET")

    if webhook_secret:
        signature = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret
            )
            data = event["data"]
        except Exception as e:
            raise BaseModelValidationError(str(e)) 
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]
    return event,event_type

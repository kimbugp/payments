# -*- coding: utf-8 -*-
"""Rating views."""
import os

import stripe
from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from ..utils.validate_payment import check_stripe_webhook, process_stripe_payment
from ..utils.view_utils import delete_by_id
from .models import Payments
from .schema import PaymentsSchema

blueprint = Blueprint("payments", __name__, url_prefix="/payments")


class PaymentsView(MethodView):
    def post(self):
        event, event_type = check_stripe_webhook()
        if event_type == "checkout.session.completed":
            print("Completed")
        else:
            pass
        return make_response(jsonify({"status": "success"}))

    def get(self):
        payments = Payments.query.all()
        schema = PaymentsSchema(many=True)
        return {"payments": schema.dump(payments)}, 200


class PaymentRequestView(MethodView):
    def post(self):
        session = process_stripe_payment()
        return make_response(jsonify({"sessionId": session["id"]}))


blueprint.add_url_rule("/", view_func=PaymentsView.as_view("payments"))
blueprint.add_url_rule("/request", view_func=PaymentRequestView.as_view("requests"))

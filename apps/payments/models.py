# -*- coding: utf-8 -*-
"""Location models."""
from ..database import Model, SurrogatePK, db


class Payments(SurrogatePK, Model):
    __tablename__ = "payments"
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    timezone = db.Column(db.String(80), nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Location({self.name})>"

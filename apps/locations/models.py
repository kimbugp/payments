# coding: utf-8
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..database import db, Model, SurrogatePK

Base = declarative_base()
metadata = Base.metadata


class Location(SurrogatePK, Model):
    """A Location location.

    e.g Lagos, Kampala, Accra, New York
    """

    __tablename__ = "location"
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    timezone = db.Column(db.String(80), nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Location({self.name})>"


class Cinemahall(Base):
    __tablename__ = 'cinemahall'

    id = Column(Integer, primary_key=True, server_default=text("nextval('cinemahall_id_seq'::regclass)"))
    date_created = Column(DateTime, server_default=text("now()"))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(100), nullable=False)


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, server_default=text("nextval('movie_id_seq'::regclass)"))
    date_created = Column(DateTime, server_default=text("now()"))
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    date_of_release = Column(DateTime, nullable=False)
    rating = Column(Integer, nullable=False)
    length = Column(Time, nullable=False)
    summary = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    date_created = Column(DateTime, server_default=text("now()"))
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100))
    is_staff = Column(Boolean, nullable=False, server_default=text("false"))


class Seat(Base):
    __tablename__ = 'seat'
    __table_args__ = (
        UniqueConstraint('name', 'cinema_hall', 'number'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('seat_id_seq'::regclass)"))
    name = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    date_created = Column(DateTime, server_default=text("now()"))
    cinema_hall = Column(ForeignKey('cinemahall.id', ondelete='CASCADE'))

    cinemahall = relationship('Cinemahall')


class Showtime(Base):
    __tablename__ = 'showtime'
    __table_args__ = (
        UniqueConstraint('show_datetime', 'movie_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('showtime_id_seq'::regclass)"))
    date_created = Column(DateTime, server_default=text("now()"))
    show_datetime = Column(DateTime, nullable=False)
    movie_id = Column(ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    price = Column(Numeric, nullable=False)
    cinema_hall = Column(ForeignKey('cinemahall.id', ondelete='CASCADE'))

    cinemahall = relationship('Cinemahall')
    movie = relationship('Movie')


class Ticket(Base):
    __tablename__ = 'ticket'
    __table_args__ = (
        UniqueConstraint('showtime_id', 'seat_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('ticket_id_seq'::regclass)"))
    date_created = Column(DateTime, server_default=text("now()"))
    payment_method = Column(String(10), nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    showtime_id = Column(ForeignKey('showtime.id', ondelete='CASCADE'), nullable=False)
    seat_id = Column(ForeignKey('seat.id', ondelete='CASCADE'))

    seat = relationship('Seat')
    showtime = relationship('Showtime')
    user = relationship('User')

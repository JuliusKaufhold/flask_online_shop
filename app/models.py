from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional, List

db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index = True, unique = True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    cart: so.Mapped[List["Cart"]] = so.relationship("Cart",back_populates="user")

    def __repr__(self):
        return "<User {}>".format(self.username)

class Item(db.Model):
    __tablename__ = "item"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    price: so.Mapped[float] = so.mapped_column(sa.Float(precision=2))
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    image: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    cart: so.Mapped[List["Cart"]] = so.relationship("Cart",back_populates="item")

class Cart(db.Model):
    __tablename__ = "cart"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index = True)
    item_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Item.id), index = True)

    user: so.Mapped['User'] = so.relationship("User", back_populates="cart")
    item: so.Mapped['Item'] = so.relationship("Item", back_populates="cart")


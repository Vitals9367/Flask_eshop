from datetime import datetime
from flask import current_app
from . import db, login_manager,whooshee
from flask_login import UserMixin
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	info = db.relationship("User_Info", cascade="all, delete-orphan", uselist=False, backref="user")
	cart = db.relationship("Cart",cascade="all, delete-orphan", uselist=False, backref="user")
	orders = db.relationship("Orders", backref="user")
	reviews = db.relationship("Reviews", backref="user")
	is_admin = db.Column(db.Boolean,nullable=False,default=False)

	def __repr__(self):
		return f"User('{self.username}')"


class User_Info(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=True)
	first_name = db.Column(db.String(30), nullable=True)
	last_name = db.Column(db.String(30), nullable=True)
	phone_number = db.Column(db.String(30), nullable=True)
	address = db.Column(db.String(30), nullable=True)


class Orders(db.Model):
	__tablename__ = 'orders'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	order_items = db.relationship("Order_Items", backref="order",cascade="all,delete")
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	price = db.Column(db.Float)
	paid = db.Column(db.Boolean,nullable=False)


class Order_Items(db.Model):
	__tablename__ = 'order_items'
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),nullable=False)
	date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	defined_item_id = db.Column(db.Integer, db.ForeignKey('defined_items.id'),nullable=False)

class Cart(db.Model):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=True)
	cart_items = db.relationship("Cart_Items", backref="cart")


class Cart_Items(db.Model):
	__tablename__ = 'cart_items'
	id = db.Column(db.Integer, primary_key=True)
	cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'),nullable=False)
	defined_item_id = db.Column(db.Integer, db.ForeignKey('defined_items.id'))
	date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Defined_Items(db.Model):
	__tablename__ = 'defined_items'

	id = db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'),nullable=False)
	size = db.Column(db.String(10), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	order_item = db.relationship("Order_Items",backref=backref('defined_item', remote_side=[id]), lazy=True)
	cart_item_id = db.relationship("Cart_Items",backref=backref('defined_item', remote_side=[id]), lazy=True)

@whooshee.register_model('name')
class Item(db.Model):
	__tablename__ = 'item'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	price = db.Column(db.Float, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='shirt.jpg')
	item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'))
	defined_item = db.relationship("Defined_Items",backref=backref('item', remote_side=[id]), lazy=True)
	reviews = db.relationship("Reviews", backref="item")

class Item_Type(db.Model):
	__tablename__ = 'item_type'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	item = db.relationship("Item",backref=backref('item_type', remote_side=[id]), lazy=True)
	
	def __repr__(self):
		return f"('{self.name}')"


class Sizes(db.Model):
	__tablename__ = 'sizes'
	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.String(10), nullable=False)
	value = db.Column(db.String(10), nullable=False)


class Reviews(db.Model):
	__tablename__ = 'reviews'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
	comment = db.Column(db.Text, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
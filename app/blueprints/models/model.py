from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (or_)
from sqlalchemy import func

from werkzeug.security import generate_password_hash, check_password_hash

from dataclasses import dataclass

db = SQLAlchemy()


class UserAlreadyExistsException(Exception):
    pass


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    products = db.relationship('Product', secondary='product_orders', back_populates='orders')
    user1 = db.relationship("User", primaryjoin='Order.user == User.id', backref="user_orders_0")

    @staticmethod
    def create_order(_user_id):
        ord = Order(user_id=_user_id)
        Order.save_to_db(ord)

    @classmethod
    def find_order_by_user_id(cls, _id):
        return cls.query.filter_by(user=_id).all()

    @classmethod
    def find_order_by_user_id_order_id(cls, _id, order_id):
        return cls.query.filter(cls.user==_id, cls.id== order_id).all()

    def __init__(self, user_id):
        self.user = user_id

    def __repr__(self):
        return u"<Order(id=%r, user=%r,  created_date=%r)>" \
               % (self.id, self.user, self.created_date)

    # Method to save to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return dict(id=self.id,
                    user=self.user,
                    )


class ProductOrder(db.Model):
    __tablename__ = 'product_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id
        self.created_date = dt.now()

    @classmethod
    def get_products_by_order_id(cls, order_id):
        return cls.query.filter(cls.order_id == order_id).all()

    @classmethod
    def find_id_by_order_and_product(cls, order_id, product_id):
        return cls.query.filter(cls.order_id == order_id, cls.product_id == product_id).all()

    # Method to save role_policy to DB
    def save_to_db(self):
        self.modified_date = dt.now()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return dict(id=self.id,
                    order_id=self.order_id,
                    product_id=self.product_id)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    orders = db.relationship('Order', secondary='product_orders', back_populates='products')

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return u"<Product(id=%r, name=%r,  price=%r," \
               u" quantity=%r)>" \
               % (self.id, self.name, self.price,
                  self.quantity)

    @classmethod
    def get_products(cls):
        return cls.query.all()

    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.query.get(product_id)

    # Method to save to DB
    def save_to_db(self):
        self.modified_date = dt.now()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return dict(id=self.id, name=self.name, price=self.price, quantity=self.quantity)



@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(75), nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(20), nullable=False, index=True)
    created_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs and kwargs.get('password'):
            kwargs['password'] = self.set_password(kwargs.get('password'))
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"<User(id=%r, first_name=%r,  last_name=%r," \
               u" email=%r)>" \
               % (self.id, self.first_name, self.last_name,
                  self.email)

    @property
    def user_id(self):
        return self.id

    @staticmethod
    def get_user(email=None, mobile=None, username=None):
        filter_obj = ""
        if mobile:
            mobile = mobile.strip()
            filter_obj = or_(User.mobile == mobile)
        if email:
            email = email.lower().strip()
            filter_obj = or_(func.lower(User.email) == email)
        if username:
            username = username.strip().lower()
            filter_obj = or_(User.mobile == username, func.lower(User.email) == username)
        user = User.query.filter(filter_obj).all()
        if user:
            return user
        return None

    @staticmethod
    def create_user(mobile, password, first_name=None, last_name=None, email=None):
        if User.get_user(mobile=mobile, email=email):
            raise UserAlreadyExistsException()
        # create the user on Database
        if email:
            email = email.strip()
        if first_name:
            first_name = first_name.strip()
        if last_name:
            last_name = last_name.strip()
        u = User(first_name=first_name,
                 last_name=last_name,
                 email=email,
                 mobile=mobile,
                 password=password,)

        User.save_to_db(u)
        return u

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        return self.password

    # Method to verify a password for a user
    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)

    # Method to save user to DB
    def save_to_db(self):
        self.modified_date = dt.now()
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return dict(id=self.id,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    age=self.age)

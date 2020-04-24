from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import json


subs = db.Table('subs',
                db.Column('subs_id', db.Integer, primary_key=True),
                db.Column('id', db.Integer, db.ForeignKey('user.id')),
                db.Column('prod_id', db.Integer, db.ForeignKey('cart.prod_id')),
                db.Column('cart_count', db.Integer, default=1)
                )

# class Subs(db.Model):
#     #__table__ = "subs_table"
#     subs_id = db.Column(db.Integer, primary_key=True)
#     u_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
#     p_id = db.Column(db.Integer, db.ForeignKey('cart.prod_id'), primary_key = True)
#     cart_count = db.Column(db.Integer)
#     # user = db.relationship('User', backref=db.backref('user_assoc'))
#     # cart = db.relationship('Cart', backref=db.backref('cart_assoc'))


class User(UserMixin, db.Model):
    #__table__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    cart_item = db.relationship('Cart', backref='crt_item', lazy='dynamic')
    item_order = db.relationship('Order', backref='itm_order', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    item_count = db.Column(db.Integer, default=0)
    user_cart_item = db.relationship('Cart', secondary=subs, backref=db.backref('cart_items', lazy='dynamic'))
    token = db.Column(db.String(140))
    #carts = db.relationship('Cart', secondary='Subs', backref=db.backref('user_table'))
    followers = db.Table('followers',
                         db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                         )
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_item_count(self, item_count):
        self.item_count = item_count + 1
        return item_count

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Cart(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(64), index=True, unique=True)
    part_cost = db.Column(db.Integer)
    part_desc = db.Column(db.String(140))
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    u_cart_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buy_item = db.Column(db.Integer, default=0)
    item_page = db.Column(db.Integer)
    #users_cart = db.relationship('User', secondary='Subs')


class Brand(db.Model):
    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(64), index=True, unique=True)
    brand_desc = db.Column(db.String(140))
    brand_filename = db.Column(db.String, default=None, nullable=True)
    brand_url = db.Column(db.String, default=None, nullable=True)
    brand_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_user_address = db.Column(db.String(84), index=True, unique=True)
    order_item_detail = db.Column(db.JSON)
    order_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



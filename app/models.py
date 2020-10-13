from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model):
    __table_name__ = 'user'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(40), unique=True, nullable=False)
    profileImg = db.Column(db.String(100), default="default.png")
    privilege = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    comments = db.relationship('Comment', backref='author', lazy=True)
    products = db.relationship('Product', backref='seller', lazy=True)
    transactions = db.relationship('Transaction', backref='mine', lazy=True)

    def __init__(self, username, nickname, password, privilege, email, address):
        self.username = username
        self.email = email
        self.nickname = nickname
        self.privilege = privilege
        self.password = self.setPassword(password)
        self.address = address

    def setPassword(self, password):
        return generate_password_hash(password)

    def tryLogin(self, password):
        return check_password_hash(self.password, password)

class Product(db.Model):
    __table_name__ = 'product'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    clothtype = db.Column(db.String(50), default="cloth")
    img = db.Column(db.String(255), default='default.png')
    description = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, name, img, price, description, userId, clothtype):
        self.name = name
        self.img = img
        self.price = price
        self.clothtype = clothtype
        self.description = description
        self.userId = userId

class Comment(db.Model):
    __table_name__ = 'comment'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    at = db.Column(db.Date, default=datetime.datetime.now())


    def __init__(userId, productId, content):
        self.userId = userId
        self.productId = productId
        self.content = content
    
class Transaction(db.Model):
    __table_name__ = 'transaction'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    approval = db.Column(db.Boolean, nullable=False, default=False)
    at = db.Column(db.Date, default=datetime.datetime.now())

    def __init__(userId, productId, quantity, approval):
        self.userId = userId
        self.productId = productId
        self.quantity = quantity
        self.approval = approval

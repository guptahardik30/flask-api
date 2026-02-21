# stores = {}
# items = {}

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()            # to create a database file named data.db in the current directory

#ORM code starting here
class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(82), nullable=False , unique=False)
    items = db.relationship('ItemModel', backref='store', lazy='dynamic')  # one to many relationship
    
    items = db.relationship(
        "ItemModel",                     
        backref="store", 
        cascade="all, delete")

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(82), nullable=False , unique=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.String(32), db.ForeignKey('stores.id'),nullable=False)
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, ValidationError
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    discription = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.discription} {self.price} {self.inventory_quantity} {self.img_url}'

# Schemas
class ProductSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    name = fields.String(required=True)
    discription = fields.String()
    price = fields.Float(required=True)
    inventory_quantity = fields.Integer(required=True)
    img_url = fields.String()

    class Meta:
        fields('id', 'name', 'discription', 'price', 'inventory_quantity', 'img_url')

    @post_load
    def create_product(self, data, **kwargs):
        return Product(**data)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Resources
class PruductListResource(Resource):
    def get(self):
        return products_schema.dump(Product.query.all()), 200

    def post(self):
        try:
            add_product = product_schema.load(request.get_json())
            db.session.add(add_product)
            db.session.commit()
            return product_schema.dump(add_product), 201
        except ValidationError as error:
            return error.messages, 400

class ProductResource(Resource):
    pass


# Routes
api.add_resource(PruductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:pk>')
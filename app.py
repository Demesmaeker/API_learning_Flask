from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os
from random import randint

# Init app
app = Flask(__name__)
api = Api(app, version='1.0', title='Learning API',
    description='API done when learning the Art of API Crafting',
)
basedir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
db = SQLAlchemy(app)


# Seller Class/model
class SellerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    VAT = db.Column(db.String)

    def __init__(self, name, VAT):
        self.name = name
        self.VAT = VAT

    def __repr__(self):
        return f"Seller(name = {name}, VAT = {VAT})"
# db.create_all()


# Serialize seller's response into a good looking JSON
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'VAT': fields.String
}


@api.route('/home', methods=['GET'])
@api.doc(description='This API says "Hello"')
class home(Resource):
    def get(self):
        result = {
            'status' : True,
            'message' : 'Hello World'
        }
        return jsonify(result)


@api.route('/status', methods=['GET'])
@api.doc(description='This API is alive !')
class status(Resource):
    def get(self):
        result = {
            'status' : True,
            'message' : 'The server is alive! Please, don\'t kill it...'
        }
        return jsonify(result)


@api.route('/login', methods=['POST'])
@api.doc(params={
    'username': 'A username',
    'password': 'A password'
}, description='There really is a session here, so just login! (too much sarcasm?)')
class login(Resource):
    def post(self):
        log_info = request.get_json()
        username = log_info["username"]
        password_length = len(log_info["password"])
        return f"Login success for user {username} with password from length: {password_length}!"


@api.route('/predict/<int:seller_avaible>/<string:month>/<int:customer_visiting_website>', methods=['GET'])
@api.doc(description='Get a super acurate prediction here')
class predict(Resource):
    def get(self, month, customer_visiting_website, seller_avaible):
        number = randint(2000, 5000)
        return f"{number}"


@api.route('/sellers', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@api.doc(description='Gestion of the sellers part of the API, with a CRUD.')
class seller(Resource):
    @marshal_with(resource_fields)
    @api.doc(description='Getting all sellers')
    def get(self):
        result = SellerModel.query.all()
        return result

    @marshal_with(resource_fields)
    @api.doc(params={
        'name': 'Name of the seller'
    }, description='Getting the information of one seller')
    def post(self):
        name = request.get_json()['name']
        result = SellerModel.query.filter_by(name=name).first()
        return result

    @marshal_with(resource_fields)
    @api.doc(params={
        'name': 'Name of the seller',
        'VAT' : "Exemple : BE 0 123 456 789"
    }, description='Adding a seller')
    def put(self):
        args = request.get_json()
        seller = SellerModel(id=seller_id, name=args['name'], VAT=args['VAT'])
        db.session.add(seller)
        db.session.commir()
        return seller
    
    @marshal_with(resource_fields)
    @api.doc(params={
        'id' : 'number',
        'name': 'Name of the seller',
        'VAT' : "Exemple : BE 0 123 456 789"
    }, description='Adding a seller')
    def patch(self):
        args = request.get_json()
        seller = SellerModel(id=args['id'], name=args['name'], VAT=args['VAT'])
        db.session.commit()
        return seller, 201
    
    def delete(self):
    @api.doc(params={
        'name': 'Name of the seller'
    }, description='Deleting a seller')
        sellers = "test delete"
        return sellers


# Run server
if __name__ == '__main__':
   app.run(port=5000)


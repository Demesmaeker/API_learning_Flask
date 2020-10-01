import os
from random import randint
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


# Init app
app = Flask(__name__)
api = Api(app, version='1.0', title='Learning API', description='API done when learning the Art of API Crafting', default='V1', default_label='first test')
basedir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Seller Class/model
class SellerModel(db.Model):
    '''
    Model for the Seller table of the database
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    VAT = db.Column(db.String)

    def __init__(self, name, VAT):
        self.name = name
        self.VAT = VAT

    def __repr__(self):
        return f"Seller(name = {self.name}, VAT = {self.VAT})"
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
        if not result:
            abort(404, message="Couldn't a seller with this name...")
        
        return result



    @marshal_with(resource_fields)
    @api.doc(params={
        'name': 'Name of the seller',
        'VAT' : "Exemple : BE 0 123 456 789"
    }, description='Adding a seller')
    def put(self):

        args = request.get_json()
        name = args['name']
        VAT =  args['VAT']

        result = SellerModel.query.filter_by(name=name).first()
        if result:
            abort(409, message="This seller already exists...")

        new_seller = SellerModel(name, VAT)
        db.session.add(new_seller)
        db.session.commit()
        return new_seller
    


    @marshal_with(resource_fields)
    @api.doc(params={
        'id' : 'number',
        'name': 'Name of the seller',
        'VAT' : "Exemple : BE 0 123 456 789"
    }, description='Editing a seller, you can chande the name and VAT but id have to be an axisting one')
    def patch(self):

        args = request.get_json()
        seller_id = args['id']
        result = SellerModel.query.filter_by(id=seller_id).first()

        if not result:
            abort(404, message="Couldn't find a seller with this id...")
        if args['name']:
            result.name = args['name']
        if args['VAT']:
            result.VAT = args['VAT']

        db.session.commit()

        return result
    


    @marshal_with(resource_fields)
    @api.doc(params={
        'name': 'Name of the seller'
    }, description='Deleting a seller')
    def delete(self):

        args = request.get_json()
        name = args['name']

        result = SellerModel.query.filter_by(name=name).first()
        if not result:
            abort(404, message="Couldn't find a seller with this id...")

        db.session.delete(result)
        db.session.commit()

        return '', 204





# Run server
if __name__ == '__main__':
    app.run(port=5000)


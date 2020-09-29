from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
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
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    VAT = db.Column(db.Integer)

    def __init__(self, name, VAT):
        self.name = name
        self.VAT = VAT



@api.route('/')
class home(Resource):
    def get(self):
        return jsonify({'message' : 'Hello World'})


@api.route('/status', methods=['GET'])
class status(Resource):
    def get(self):
        result = {
            "status" : True,
            "message" : "The server is alive! Please, don't kill it..."
        }
        return jsonify(result)

@api.route('/login', methods=['POST'])
class login(Resource):
    def post(self):
        log_info = request.get_json()
        username = log_info["username"]
        password_length = len(log_info["password"])
        return f"Login success for user {username} with password from length: {password_length}!"


@api.route('/predict/<int:seller_avaible>/<string:month>/<int:customer_visiting_website>', methods=['GET'])
class predict(Resource):
    def get(self, month, customer_visiting_website, seller_avaible):
        number = randint(2000, 5000)
        return f"{number}"


@api.route('/sellers', methods=['GET', 'POST', 'PATCH', 'DELETE'])
class seller(Resource):
    def get(self):
        sellers = "test get"
        return sellers

    def post(self):
        sellers = "test post"
        return sellers
    
    def patch(self):
        sellers = "test patch"
        return sellers
    
    def delete(self):
        sellers = "test delete"
        return sellers


# Run server
if __name__ == '__main__':
   app.run(port=5000)


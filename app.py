from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from random import randint

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Seller Class/model
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    VAT = db.Column(db.Integer)

    def __init__(self, name, VAT):
        self.name = name
        self.VAT = VAT


# Seller Schema
class SellerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'VAT')

seller_schema = SellerSchema(strict=True)
sellers_schema = SellerSchema(many=True, strict=True)



@app.route('/')
def home():
   return jsonify({'message' : 'Hello World'})

@app.route('/status', methods=['GET'])
def status():
    result = {
        "status" : True,
        "message" : "The server is alive! Please, don't kill it..."
    }
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    log_info = request.get_json()
    username = log_info["username"]
    password_length = len(log_info["password"])
    return f"Login success for user {username} with password from length: {password_length}!"


@app.route('/predict/<int:seller_avaible>/<string:month>/<int:customer_visiting_website>', methods=['GET'])
def predict(month, customer_visiting_website, seller_avaible):
    number = randint(2000, 5000)
    return f"{number}"


@app.route('/sellers', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def seller():
    if request.method == 'GET' :
        sellers = "test get"
        return sellers
    elif request.method == 'POST' :
        sellers = "test post"
        return sellers
    elif request.method == 'PATCH' :
        sellers = "test patch"
        return sellers
    else:
        sellers = "test delete"
        return sellers


# Run server
if __name__ == '__main__':
   app.run(port=5000)


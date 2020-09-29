from flask import Flask, request, jsonify
from random import randint
app = Flask(__name__)

@app.route('/')
def home():
   return 'Hello World'

@app.route('/status', methods=['GET'])
def status():
    result = {
        "status" : True,
        "message" : "The server is alive! Please, don't kill it..."
    }
    return result

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

if __name__ == '__main__':
   app.run(port=5000)


from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse, fields, marshal_with
import configparser
import json
import yaml
import db.db as db
import os


app = Flask(__name__)
api = Api(app)

# Flask configurations
flask_config = "flask.yml"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, flask_config)) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
API_KEY = data['API_KEY']
print(API_KEY)


# Helper functions
def money2float(money):
    return float(money[1:])

# Homepage
@app.route('/')
def home():
    return render_template('base.html')

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'firstname', dest='firstname',
    location='form', required=True,
    help='The user\'s firstname',
)

# User RESTFUL API
class User(Resource):
    def get(self, username):
        if not db.check_user_exists(username):
            return {"status": 405, "response": f"User {username} does not exist"}
        return {"status": 200, "response": db.show_user(username)}
        
    def post(self, username):
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        phonenumber = data['phonenumber']

        if 'API-KEY' not in request.headers or request.headers['API_KEY'] != API_KEY:
            return {"status": 404, "response": "Forbidden: API Key required for this function"}
        
        if not all([username, firstname, lastname, phonenumber]):
            return {"status": 403, "response": "Invalid: One or more fields missing."}
        
        if db.check_user_exists(username):
            return {"status": 405, "response": f"User {username} already exists!"}

        if db.check_number_exists(phonenumber):
            return {"status": 406, "response": f"{phonenumber} is registered under an existing user!"}
        
        user_details = db.create_new_user(username, firstname, lastname, phonenumber)
        return {"status": 200, "response": user_details}


# Admin/View all users in database
class Users(Resource):
    def get(self):
        if 'API-KEY' not in request.headers or request.headers['API_KEY'] != API_KEY:
            return {"status": 404, "response": "Forbidden: API Key required for this function"}
        return {"status": 200, "response": db.show_all_users()}


# User/View Account balance
@app.route('/viewBalance')
def viewBalance():
    username = request.args.get('username', default='', type=str)
    if not username:
        return {"status": 403, "response": "username field is missing"}
    if not db.check_user_exists(username):
        return {"status": 405, "response": f"User {username} does not exist"}
    
    return {"status": 200, "response": db.show_balance(username)}


# User/Top-up wallet
class Topup(Resource):
    def post(self, username):
        data = request.get_json()
        try:
            amount = float(data['amount'])
        except:
            return {"status": 410, "response": "Amount must be a number"}

        if not all([username, amount]):
            return {"status": 403, "response": "One or more fields is missing!"}
        if amount < 0:
            return {"status": 408, "response": "Trying to top-up negative amount."}
        if not db.check_user_exists(username):
            return {"status": 405, "response": f"User {username} does not exist"}
        
        balance = money2float(db.show_balance(username))
        new_balance = balance + amount
        db.update_balance(username, new_balance)

        return {"status": 200, "response": {
            "username": username,
            "prev_balance": balance,
            "topup_amount": amount,
            "new_balance": new_balance
        }}


# User/Transfer to another user
@app.route('/transfer')
def transfer():
    sender = request.args.get('sender', default='', type=str)
    recipient = request.args.get('recipient', default='', type=str)
    amount = request.args.get('amount', default=0.0, type=float)
    
    if not all([sender, recipient, amount]):
        return {"status": 403, "response": "One or more fields is missing!"}
    if amount < 0:
        return {"status": 408, "response": "Trying to send negative amount."}
    if not db.check_user_exists(sender):
        return {"status": 405, "response": f"Sender {sender} does not exist"}
    if not db.check_user_exists(recipient):
        return {"status": 405, "response": f"Recipient {recipient} does not exist"}
    if sender == recipient:
        return {"status": 409, "response": f"Trying to transfer money to ownself"}

    sender_balance = money2float(db.show_balance(sender))
    recipient_balance = money2float(db.show_balance(recipient))
    if sender_balance < amount:
        return {"status": 400, "response": f"Invalid operation: Sender {sender} has insufficient funds."}
    
    sender_balance_new = sender_balance - amount
    recipient_balance_new = recipient_balance + amount
    
    db.update_balance(sender, sender_balance_new)
    db.update_balance(recipient, recipient_balance_new)

    return {"status": 200, "response": {
        "sender": sender,
        "recipient": recipient,
        "sender_balance": sender_balance_new,
        "recipient_balance": recipient_balance_new
    }}


api.add_resource(User, '/user/<username>')
api.add_resource(Users, '/users')
api.add_resource(Topup, '/topup/<username>')

if __name__ == "__main__":
    app.run(debug=True)
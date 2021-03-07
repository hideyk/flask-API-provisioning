from flask import Flask, request, render_template
import configparser
import json
import yaml
import db.db as db
import os


app = Flask(__name__)

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


# Admin/Create a new user
@app.route('/createUser')
def createUser():
    if 'API-KEY' not in request.headers or request.headers['API_KEY'] != API_KEY:
        return {"status_code": 404, "response": "Forbidden: API Key required for this function"}
    
    username = request.args.get('username', default='', type=str)
    firstname = request.args.get('firstname', default='', type=str)
    lastname = request.args.get('lastname', default='', type=str)
    phonenumber = request.args.get('phonenumber', default='', type=int)

    if not all([username, firstname, lastname, phonenumber]):
        return {
            "status_code": 403, 
            "response": "Invalid: One or more fields missing."
        }
    
    if db.check_user_exists(username):
        return {"status_code": 405, "response": f"User {username} already exists!"}

    if db.check_number_exists(phonenumber):
        return {"status_code": 406, "response": f"{phonenumber} is registered under an existing user!"}
    
    user_details = db.create_new_user(username, firstname, lastname, phonenumber)
    return {"status_code": 200, "response": user_details}
    

# Admin/View all users in database
@app.route('/showUsers')
def showUsers():
    if 'API-KEY' not in request.headers or request.headers['API_KEY'] != API_KEY:
        return {"status_code": 404, "response": "Forbidden: API Key required for this function"}
    return {"status_code": 200, "response": db.show_all_users()}


# User/View Account details
@app.route('/viewAccount')
def viewAccount():
    username = request.args.get('username', default='', type=str)
    if not username:
        return {"status_code": 403, "response": "username field is missing"}
    if not db.check_user_exists(username):
        return {"status_code": 405, "response": f"User {username} does not exist"}
    
    return {"status_code": 200, "response": db.show_user(username)}


# User/View Account balance
@app.route('/viewBalance')
def viewBalance():
    username = request.args.get('username', default='', type=str)
    if not username:
        return {"status_code": 403, "response": "username field is missing"}
    if not db.check_user_exists(username):
        return {"status_code": 405, "response": f"User {username} does not exist"}
    
    return {"status_code": 200, "response": db.show_balance(username)}


# User/Top-up wallet
@app.route('/topup')
def topup():
    username = request.args.get('username', default='', type=str)
    amount = request.args.get('amount', default=0.0, type=float)
    
    if not all([username, amount]):
        return {"status_code": 403, "response": "One or more fields is missing!"}
    if amount < 0:
        return {"status_code": 408, "response": "Trying to top-up negative amount."}
    if not db.check_user_exists(username):
        return {"status_code": 405, "response": f"User {username} does not exist"}
    
    balance = money2float(db.show_balance(username))
    new_balance = balance + amount
    db.update_balance(username, new_balance)

    return {"status_code": 200, "response": {
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
        return {"status_code": 403, "response": "One or more fields is missing!"}
    if amount < 0:
        return {"status_code": 408, "response": "Trying to send negative amount."}
    if not db.check_user_exists(sender):
        return {"status_code": 405, "response": f"Sender {sender} does not exist"}
    if not db.check_user_exists(recipient):
        return {"status_code": 405, "response": f"Recipient {recipient} does not exist"}
    if sender == recipient:
        return {"status_code": 409, "response": f"Trying to transfer money to ownself"}

    sender_balance = money2float(db.show_balance(sender))
    recipient_balance = money2float(db.show_balance(recipient))
    if sender_balance < amount:
        return {"status_code": 400, "response": f"Invalid operation: Sender {sender} has insufficient funds."}
    
    sender_balance_new = sender_balance - amount
    recipient_balance_new = recipient_balance + amount
    
    db.update_balance(sender, sender_balance_new)
    db.update_balance(recipient, recipient_balance_new)

    return {"status_code": 200, "response": {
        "sender": sender,
        "recipient": recipient,
        "sender_balance": sender_balance_new,
        "recipient_balance": recipient_balance_new
    }}
    

if __name__ == "__main__":
    app.run(debug=True)
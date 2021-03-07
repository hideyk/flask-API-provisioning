from flask import Flask, request, render_template
import configparser
import json
import yaml



app = Flask(__name__)

# Flask configurations
config_file = r"app.yml"
with open(config_file) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


# Homepage
@app.route('/')
def home():
    return render_template('base.html')


# Admin/Create a new user
@app.route('/newUser')
def login():
    xApiKey = get_config()
    base_url = r"https://849rs099m3.execute-api.ap-southeast-1.amazonaws.com/techtrek/login"
    username = request.args.get('username', default='', type=str)
    password = request.args.get('password', default='', type=str)

    headers = {
        "x-api-key": xApiKey
    }
    params = {
        "username": f'{username}',
        "password": f'{password}' 
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(params))
    if response.status_code != 200:
        return {
            "status_code": response.status_code,
            "response": response.text
        }
    else:
        return {
            "status_code": response.status_code,
            "response": response.text
        }


# Admin/View all users in database


if __name__ == "__main__":
    app.run(debug=True)
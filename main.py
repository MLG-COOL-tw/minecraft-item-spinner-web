from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

auth_url = os.getenv("auth_url")
api_url = os.getenv("api_url")
client_id = os.getenv("client_id")
public_key = os.getenv("public_key")
secret_key = os.getenv("secret_key")

redir = "http://127.0.0.1:8080/main"
API_ENDPOINT = 'https://discord.com/api/v10'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        return redirect(auth_url)
    else:
        return render_template("login.html")


@app.route("/main", methods=['GET'])
def main():
    if request.args:
        code = request.args.get('code')
        user = exchange_code(code)

        username = user['username']
        userid = user['id']
        useravatar = user['avatar']

        return render_template("index.html", username = username, userid = userid, useravatar = useravatar)
    else:
        return redirect(url_for("login"))

def exchange_code(code):
    # gets the access_token

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redir
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(client_id, secret_key))
    r.raise_for_status()
    return get_user_data(r.json()['access_token'])

def get_user_data(accessToken):
    # gets the user id from the access_token

    headers = {
        "Authorization": f"Bearer {accessToken}"
    }

    r = requests.get(url=api_url, headers=headers)
    r.raise_for_status()
    return r.json()


@app.errorhandler(500)
def internal_server_error(error):
    #重新登入
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
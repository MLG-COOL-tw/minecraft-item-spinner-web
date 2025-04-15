from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

login_site = os.getenv("login_site")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        return redirect(login_site)
    else:
        return render_template("login.html")

@app.route("/main", methods=['GET'])
def main():
    if request.args:
        code = request.args.get('code')
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True, port=8080)

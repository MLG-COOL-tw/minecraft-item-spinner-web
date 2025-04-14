from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route("/main")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8080)

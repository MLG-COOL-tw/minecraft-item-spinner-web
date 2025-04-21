#TODO: change roll's api stuff

from flask import Flask, render_template, request, session, redirect, url_for
import requests
import random
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("secret_key")

client_secret = os.getenv("client_secret")
client_id = "1361369448279183532"
API_ENDPOINT = "https://discord.com/api/v10"
redir = "http://127.0.0.1:8080/"
auth_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redir}&scope=identify"
api_url = "https://discordapp.com/api/users/@me"


@app.route("/", methods=['GET', 'POST'])
def main():
    if not session.get("login"):
        #if haven't logged in
        if session.get("username"):
            session["username"] = ""
            session["userid"] = ""
            session["useravatar"] = ""

        #post request for the button
        if request.method == 'POST':
            #logged in
            session["login"] = True
            
            return redirect(auth_url)
        else:
            return render_template("login.html")
    elif session.get("login"):
        #if logged in
        if request.method == 'POST':
            #logout btn
            if request.form["btn"] == "logout":
                session["login"] = False;
                return redirect(redir)
            #roll btn
            elif request.form["btn"] == "roll":
                return redirect(url_for("roll")) 

        if request.args and not session.get("username"):
            #gets the code from the auth link
            #gets the username, id, avatar from discord api
            code = request.args.get('code')
            user = exchange_code(code)

            session["username"] = user['username']
            session["userid"] = user['id']
            session["useravatar"] = user['avatar']
        
        #renders index.html with the session
        return render_template("index.html", username=session["username"], userid=session["userid"], useravatar=session["useravatar"])

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

    r = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers, auth=(client_id, client_secret))
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


@app.route("/roll", methods=['GET', 'POST'])
def roll():
    if request.method == 'POST' or not session.get("login"):
        #if is post request: go back to main page
        #if login=false: go back to login page
        #both are on the same url
        return redirect(redir)
    else:
        #all the items
        items = [["iron_sword", "diamond_sword", "netherite_sword"],
                 ["iron_axe", "diamond_axe", "netherite_axe"],
                 ["iron_pickaxe", "diamond_pickaxe", "netherite_pickaxe"],
                 ["iron_helmet", "diamond_helmet", "netherite_helmet"],
                 ["iron_chestplate", "diamond_chestplate", "netherite_chestplate"],
                 ["iron_leggings", "diamond_leggings", "netherite_leggings"],
                 ["iron_boots", "diamond_boots", "netherite_boots"],
                 ["bow"], ["mace"]]
        
        #randomly picks one item
        pick_item = random.randint(0, len(items)-1)
        pick_item_type = random.randint(0, len(items[pick_item])-1)
        enchantments = {}
        enchant = []

        #randomly chooses the level of the enchantment
        enchantments["mending"] = random.randint(0, 1)
        enchantments["unbreaking"] = random.randint(0, 3)
        if pick_item == 0:
            enchantments["sharpness"] = random.randint(0, 5)
            enchantments["fire_aspect"] = random.randint(0, 2)
            enchantments["looting"] = random.randint(0, 3)
            enchantments["sweeping_edge"] = random.randint(0, 3)
        elif pick_item == 1:
            enchantments["sharpness"] = random.randint(0, 5)
            enchantments["efficiency"] = random.randint(0, 5)
            enchantments["fortune"] = random.randint(0, 3)
        elif pick_item == 2:
            enchantments["efficiency"] = random.randint(0, 5)
            enchantments["fortune"] = random.randint(0, 3)
        elif pick_item == 3:
            enchantments["protection"] = random.randint(0, 4)
            enchantments["thorns"] = random.randint(0, 3)
            enchantments["aqua_affnity"] = random.randint(0, 1)
            enchantments["respiration"] = random.randint(0, 3)
        elif pick_item == 4:
            enchantments["protection"] = random.randint(0, 4)
            enchantments["thorns"] = random.randint(0, 3)
        elif pick_item == 5:
            enchantments["protection"] = random.randint(0, 4)
            enchantments["thorns"] = random.randint(0, 3)
            enchantments["swift_sneak"] = random.randint(0, 3)
        elif pick_item == 6:
            enchantments["protection"] = random.randint(0, 4)
            enchantments["thorns"] = random.randint(0, 3)
            enchantments["feather_falling"] = random.randint(0, 4)
            enchantments["depth_strider"] = random.randint(0, 3)
            enchantments["soul_speed"] = random.randint(0, 3)
        elif pick_item == 7:
            enchantments["power"] = random.randint(0, 5)
            enchantments["flame"] = random.randint(0, 3)
            enchantments["punch"] = random.randint(0, 4)
        elif pick_item == 8:
            enchantments["smite"] = random.randint(0, 5)
            enchantments["density"] = random.randint(0, 5)
            enchantments["wind_burst"] = random.randint(0, 3)

        for key, value in enchantments.items():
            if value != 0:
                enchant.append(key)
        
        return render_template("roll.html", pick_item=pick_item, pick_item_type=pick_item_type, enchant=enchant, enchantments=enchantments)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
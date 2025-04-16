from flask import Flask, render_template, request, redirect, url_for
import requests
import random
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
    #login page
    #post request for the button
    if (request.method == 'POST'):
        return redirect(auth_url)
    else:
        return render_template("login.html")


@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        #selects random item and random enchantment for the item
        #sends it back to html with jinja

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
        enchantments = {"item":items[pick_item][pick_item_type]}

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

        return enchantments

    elif request.args:
        #gets the code from the auth link
        #gets the username, id, avatar from discord api
        code = request.args.get('code')
        user = exchange_code(code)

        username = user['username']
        userid = user['id']
        useravatar = user['avatar']

        return render_template("index.html", username = username, userid = userid, useravatar = useravatar)
    else:
        #if there is no code then make them relogin
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
    #relogin (cus the discord access token has a timer for some reason)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
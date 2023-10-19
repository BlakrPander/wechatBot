# riot-auth Copyright (c) 2022 Huba Tuba (floxay)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


import asyncio
import sys

import riotAuth.RiotLogin

# region asyncio.run() bug workaround for Windows, remove below 3.8 and above 3.10.6
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# endregion

def fetch_store(username,password):
    # username = "blakr624"
    # password = "Pander@1234"
    # CREDS = username, password

    user = riotAuth.RiotLogin.Auth(username,password)
    user.auth()

    # print(f"Access Token Type: {user.token_type}\n")
    # print(f"Access Token: {user.access_token}\n")
    # print(f"Entitlements Token: {user.entitlement}\n")
    # print(f"User ID: {user.Sub}")

    # Reauth using cookies. Returns a bool indicating whether the reauth attempt was successful.
    # asyncio.run(auth.reauthorize())

    import requests

    url = "https://pd.ap.a.pvp.net/"+"store/v2/storefront/"+user.Sub
    access_token = user.access_token
    entitlements_token = user.entitlement
    client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
    client_version = "release-07.05-shipping-4-974204"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Riot-Entitlements-JWT": entitlements_token,
        "X-Riot-ClientPlatform": client_platform,
        "X-Riot-ClientVersion": client_version,
        "Content-Type": "application/response.json"
    }

    response = requests.get(url, headers=headers)

    # print(response.status_code)
    # print(response.json())

    import json

    json_dict=response.json()
    json_str = json.dumps(json_dict)
    json_obj= json.loads(json_str)

    formatted_json_str = json.dumps(json_obj, indent=4)

    store_offers=json_obj["SkinsPanelLayout"]["SingleItemOffers"]
    # print(formatted_json_str)
    # print(store_offers)

    weaponJson_file_path = os.path.abspath(os.path.join(curPath, "weapon.json"))

    with open(weaponJson_file_path,"r",encoding="gbk") as file:
        local_json_data = json.load(file)
    data=local_json_data["data"]
    res=[]
    for weaponuuid in store_offers:
        item_name = None
        for item in data:
            for level in item["levels"]:
                if level.get("uuid") == weaponuuid:
                    item_name = level.get("displayName")
                    break

        if item_name:
            print(item_name)
            res.append(item_name)
        else:
            print("404!")
    return res

if __name__ == "__main__":
    username="blakr624"
    password="Pander@1234"
    print(fetch_store(username,password))
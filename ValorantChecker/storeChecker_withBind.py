# riot-auth Copyright (c) 2022 Huba Tuba (floxay)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

import sys
import os
import asyncio
import sys
import riotAuth.RiotLogin
import requests
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pickle





# region asyncio.run() bug workaround for Windows, remove below 3.8 and above 3.10.6
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# endregion


# username = sys.argv[1]
# password = sys.argv[2]
# username = "blakr624"
# password = "Pander@1234"
username = "bl4kr"
password = "Pander1234"

def checkIfBind(wxid):
    loginData_file_path = os.path.abspath(os.path.join(curPath, "data.pickle"))
    with open(loginData_file_path,"rb") as file:
        logindata=pickle.load(file)
    check=logindata.get(wxid)
    if(check):
        return True
    else:
        return False

def bindLoginInfo(wxid,username,password,rebind=False):
    loginData_file_path = os.path.abspath(os.path.join(curPath, "data.pickle"))
    with open(loginData_file_path,"rb") as file:
        logindata=pickle.load(file)
    check=logindata.get(wxid)
    if check is None or rebind is True:
        user = riotAuth.RiotLogin.Auth(username,password)
        try:
            user.auth()
        except Exception as e:
            return -1
        # print(f"Access Token Type: {user.token_type}\n")
        # print(f"Access Token: {user.access_token}\n")
        # print(f"Entitlements Token: {user.entitlement}\n")
        # print(f"User ID: {user.Sub}")
        logindata[wxid]={"user_id":user.Sub,"username":username,"password":password,"access_token":user.access_token,"entitlements_token":user.entitlement}
        # print(logindata)
        with open(loginData_file_path,"wb") as file:
            pickle.dump(logindata,file)
        return 1
    else:
        print(logindata)
        print("bind already!")
        return 0
    # Reauth using cookies. Returns a bool indicating whether the reauth attempt was successful.
    # asyncio.run(auth.reauthorize())

def fetchStore(wxid,target="skinsPanelLayout"):
    while True:
        loginData_file_path = os.path.abspath(os.path.join(curPath, "data.pickle"))
        with open(loginData_file_path,"rb") as file:
            logindata=pickle.load(file)
        check=logindata.get(wxid)
        if(check is None):
            print("user not binded!")
            return -1
        user=logindata[wxid]
        # print(type(user["access_token"]))
        if(target=="skinsPanelLayout"):
            print("正在为"+wxid+"获取每日商店！")
        elif(target=="bonusStore"):
            print("正在为"+wxid+"获取夜市！")
        url = "https://pd.ap.a.pvp.net/"+"store/v2/storefront/"+user["user_id"]
        client_platform = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        client_version = "release-07.05-shipping-4-974204"

        headers = {
            "Authorization": f"Bearer "+user['access_token'],
            "X-Riot-Entitlements-JWT": user['entitlements_token'],
            "X-Riot-ClientPlatform": client_platform,
            "X-Riot-ClientVersion": client_version,
            "Content-Type": "application/response.json"
        }

        response = requests.get(url, headers=headers)

        if(response.status_code!=200): #login failed trying to renew auth
            res=bindLoginInfo(wxid,user['username'],user['password'],True)
            if(res==-1):
                return -1
        else:
            res=analyzeResult(response,target)
            return res




def analyzeResult(response,target="skinsPanelLayout"):
    import json

    json_dict=response.json()
    json_str = json.dumps(json_dict)
    json_obj= json.loads(json_str)

    storeOffers=[]
    bonusOffers=[]
    bonusOffersDetail=[]
    # formatted_json_str = json.dumps(json_obj, indent=4)
    if target=="skinsPanelLayout":
        storeOffers=json_obj["SkinsPanelLayout"]["SingleItemOffers"]
        # print(formatted_json_str)
        # print(store_offers)
    elif target=="bonusStore":
        if "BonusStore" in json_obj:
            bonusStoreOffers=json_obj["BonusStore"]["BonusStoreOffers"]
            # print(bonusStoreOffers)
            for item in bonusStoreOffers:
                detail={}
                offer=item["Offer"]
                detail["DiscountPercent"]=item["DiscountPercent"]
                detail["DiscountCosts"]=list(item["DiscountCosts"].values())[0]
                # print(detail["DiscountCosts"],item["DiscountCosts"])
                bonusOffers.append(offer["OfferID"])
                bonusOffersDetail.append(detail)
                storeOffers=bonusOffers
        else:
            return -1

    weaponJson_file_path = os.path.abspath(os.path.join(curPath, "weapon1.json"))

    with open(weaponJson_file_path,"r",encoding='utf-8') as file:
        local_json_data = json.load(file)
    data=local_json_data["data"]
    res=[]
    for weaponuuid in storeOffers:
        item_name = None
        for item in data:
            for level in item["levels"]:
                if level.get("uuid") == weaponuuid:
                    item_name = level.get("displayName")
                    break

        if item_name:
            # print(item_name)
            res.append(item_name)
        else:
            print("404!")
    if(target=="bonusStore"):
        for detail,item in zip(bonusOffersDetail,res):
            detail["Offer"]=item
        res=bonusOffersDetail
    return res


if __name__ == "__main__":
    bindLoginInfo("1","blakr624","Pander@1234")
    fetchStore("1")
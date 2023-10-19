#coding=gbk
import pickle

# # Òª´æ´¢µÄ×ÖµäÊý¾Ý
# data = {"wxid1":{"user_id":"","access_token":"","entitlements_token":""}}

# # ½«×ÖµäÊý¾Ý´æÈëÎÄ¼þ
# filename = "data.pickle"
# with open(filename, "wb") as file:
#     pickle.dump(data, file)

# import pickle

filename = "data.pickle"
with open(filename, "rb") as file:
    data=pickle.load(file)
print(data)

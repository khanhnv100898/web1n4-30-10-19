from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

# creat data
ttw_db = client.ttw_app

# creat collection
Login = ttw_db["logins"]


# a = ['1','2','3','4','5']

# creat document
# new_login = {
#     "fullname":"NgoVanKhanh",
#     "username":"shipper",
#     "password":"shipper",
#     # 1 admin. 2 user, 3 shipper
#     "level":3,
#     "email":"khanhnv100898@gmail.com",
#     "phone":"0353918686",
#     "id_person":"013540512",
#     "balance":"100",
#     "address":"Yen Vien, Ha Noi",
# }
# Login.insert_one(new_login)

# id = Login.find_one({"_id":ObjectId("5da54441aa22fd9e496a7462")})

# new_login = {"$set":{
#     "fullname":"NgoVanKhanh",
#     "username":"user",
#     "password":"user",
#     "level":2,
#     "email":"khanhnv100898@gmail.com",
#     "phone":"0353918686",
#     "id_person":"013540512",
#     "balance":"100",
#     "address":"Yen Vien, Ha Noi",
#     "test":a},
# }}

# new_login = {"$addToSet":{
#     "test":"6",
# }}

# Login.update_one(id,new_login)


# found_login = Login.find()
# print(found_login)
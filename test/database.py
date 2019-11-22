from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

# creat data
ttw_db = client.ttw_app


# 
# creat collection
# Login = ttw_db["logins"]

# creat document
# new_login = {
    # "fullname":"NgoVanKhanh",
    # "username":"user3",
    # "password":"user3",
    # "level":2,
    # "email":"khanhnv100898@gmail.com",
    # "phone":"0353918686",
    # "id_person":"013540512",
    # "balance":"100",
    # "address":"Yen Vien, Ha Noi"
# }
# Login.insert_one(new_login)

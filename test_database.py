from pymongo import MongoClient
from bson import ObjectId


uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

ttw_db = client.ttw_app

Order = ttw_db["orders"]
Product = ttw_db["products"]
Test = ttw_db["tests"]


# order = Order.find_one({"_id":ObjectId("5db5acfdfc0faed706867f83")})

# a = int(order['order_fee'])
# a = a-40
# print(a)

# product = Product.find({'product_kids': True})
# for i in product:
#     print(i['name'])

# product = Product.find_one({"_id":ObjectId("5da09d00e033bb38fa636551")})


# id_product = ObjectId("5da09d00e033bb38fa636551")
# a = order['product_id']
# for i in a:
#     if i['_id']== id_product:
#         a.remove(i)
#     else:
#         update = {
#             "product":a,
#         }
#         Order.update_one(order,update)


a = {
    "_id":"1",
    "name":"Khanh"
}
b = {
    "_id":"2",
    "name":"Khanh"
}
c = {
    "_id":"3",
    "name":"Khanh"
}
d = {
    "_id":"4",
    "name":"Khanh"
}

# ar=[a,b,c,d]

# Test.insert_one({"test":ar})

# test = Test.find_one({"_id":ObjectId('5db90e46cab1e85cccc3d8db')})

# ar = test['test']
# for i in ar:
#     if i['_id']=="1":
#         ar.remove(i)
#         for i in ar:
#             update = {"$set":{"test":{
#                 "_id":i['_id'],
#                 "name":i['name'],
#             }}}
#             Test.update_one(test,update)

# Test.update_many(
#     {'_id': ObjectId("5db90e46cab1e85cccc3d8db")}, 
#     { '$pull': { "test" : { '_id': '1' } } },
# )



# for i in ar:
#     update = {"$addToSet":{"test":{
#         "_id":i['_id'],
#         "name":i['name'],
#     }}}
#     Test.update(test,update)







        # update_order = {"$addToSet":{"product_id":{
        #     "_id":i['_id'],
        #     "image":i['image'],
        #     "name":i['name'],
        #     "description":i['description'],
        #     "price":int(i['price']),
        #     "status":i['status'],
        #     "brand":i['brand'],
        #     "product_type":i['product_type'],
        #     "product_gender":i['product_gender'],
        #     "product_kids":i['product_kids'],
        # }}}

        # Order.update_one(order,update_order)






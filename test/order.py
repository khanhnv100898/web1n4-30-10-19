from pymongo import MongoClient
from bson import ObjectId


uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

# creat data
ttw_db = client.ttw_app

# creat collection
Order = ttw_db["orders"]

# Mongoengine
# class Orders(Document):
#     user_id = ListField(ReferenceField(Login))
#     product_id = ListField(ReferenceField(Product))
#     address = StringField()
#     request_time = DateTimeField()
#     order_time = DateTimeField()
#     order_fee = IntField()
#     ship_fee = IntField()
#     is_ordered = BooleanField()
#     status = StringField()

# new_order = {
#     "user_id":,
#     "product_id":,
#     "shipper_id":,
#     "address":,
#     "request_time":,
#     "order_time":,
#     "order_fee":,
#     "ship_fee":,
#     "is_ordered":,
#     "status":,
# }

# Order.insert_one(new_order)
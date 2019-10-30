from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

ttw_db = client.ttw_app

Product = ttw_db["products"]

# new_Product = {
#     "image": "https://assets.adidas.com/images/h_600,f_auto,q_auto,fl_lossy/e65d468b91a64c45b753a84e0101decd_9366/Galaxy_Away_Jersey_Blue_BS4993_01_laydown.jpg",
#     "name": "Galaxy Away Jersey KNV456",
#     "description": "Galaxy rule the game with a one-two punch of lightning-quick pace and strong attacking power. Honor the star-stacked squad from LA in this junior boys' soccer jersey. Styled after the team's away uniform, the jersey features an LA Galaxy badge on the chest plus ventilated climacool®.",
#     "price": 75,
#     "status": "Còn hàng",
#     "brand": "Adidas",
#     "product_type": "Áo",
#     "product_gender": "Girl",
#     "product_kids": True,
# }
# Product.insert_one(new_Product)

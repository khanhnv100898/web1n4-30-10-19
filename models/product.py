from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://admin:admin@ttw-xlquo.mongodb.net/admin?retryWrites=true&w=majority"

client = MongoClient(uri)

ttw_db = client.ttw_app

Product = ttw_db["products"]

# new_Product = {
#     "image": "https://assets.adidas.com/images/h_600,f_auto,q_auto,fl_lossy/c53668fe225a4e11a98da82500cb60a0_9366/Ultraboost_Shoes_White_BB6308_01_standard.jpg",
#     "name": "NMD_R1 Shoes Grey ",
#     "description": "Stride out in a minimalist technical style. These NMD shoes bring a modern attitude to 80s racing heritage. These knit sneakers are built for a sock-like fit. Boost cushioning provides a responsive, energized feel.",
#     "price": 75,
#     "status": "Hết hàng",
#     "brand": "Adidas",
#     "product_type": "Giầy",
#     "product_gender": "Women",
#     "product_kids": False,
#     "view":34,
#     "sold_count":45,
# }
# Product.insert_one(new_Product)

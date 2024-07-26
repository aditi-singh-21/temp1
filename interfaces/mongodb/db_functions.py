from flask import current_app

class VendorsRepository:
    def __init__(self):
        self.mongo = current_app.config["mongo_db"]

    def find_by_slug(self, slug):
        return self.mongo.vendors.find_one({"slug": slug},{'_id':0})

    def find_vendors(self,category,city,state,services):
        return list(self.mongo.vendors.find({
    "$or": [
        {
            "category":category, 
        },
        {
            "address": {"$regex": f"^\\b{city}\\b,", "$options": "i"}, 
           
        },
        {
           "address": {"$regex": f",\\s*\\b{state}\\b$", "$options": "i"}
        },
        {
           "services": {"$regex": f".({services}).", "$options": "i"}
        }
    ]
}))
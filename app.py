# from flask import Flask ,request

# app = Flask(__name__)

# # # @app.route('/')
# # # def hello_world():
# # #     return 'Hello,world!'

# # # @app.route('/store')
# # # def hello_world():
# # #     return 'Hello,world!'


# store = [
#     {
#         "name": "spencer",
#         "items" : [
#             {
#                 "name": "snacks",
#                 "price":"20"
#             }
#         ]
#     }
# ]

# # print(store)

# # @app.route('/')
# # def home():
# #     return "Flask server running ✅"

# # @app.route('/store')
# # def get_store():
# #     return str(store)  

# # if __name__ == "__main__":
# #     app.run(debug=True)


# @app.get('/store')
# def get_store():
#     return str(store) 
# @app.post("/store")
# def add_store():
#     request_data=request.get_json()
#     new_data={"name": request_data["name"],"items":[]}
#     store.append(new_data)
#     return store,200

# @app.post("/store/<string:name>/item")
# def add_items(name):
#     request_data =request.get_json()
#     for stor in store:
#         if stor['name']==name:
#             new_data= {"name"  : request_data["name"], "price":request_data["price"]}
#             stor["items"].append(new_data)
#             return stor["name"], 200
#     return {"message" : "Store Not Found"}

# @app.get("/store/<string:name>")
# def get_store_by_name(name):
#     for s in store:
#         if s['name'] == name:
#             return s
#     return {"message": "store not found"}, 404



from flask import Flask, request
from db import db, StoreModel, ItemModel 
import uuid
from flask import abort
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def home():
    return{"message":"Api is running"}

@app.post("/store")
def addStoreDetail():

    store_data=request.get_json()

    if"name" not in store_data:
        abort(400,message="Bad request. Payload does not contain the name")

    if StoreModel.query.filter_by(name=store_data["name"]).first() :
        return {"message":"StoreName already exists"}
    

    store=StoreModel(
        id=uuid.uuid4().hex,
        name=store_data["name"]
    )

    db.session.add(store)
    db.session.commit()

    return{'id':store.id, "name":store.name},201

@app.get("/store")
def get_stores():
    stores = StoreModel.query.all()
    return {
        "stores": [{"id": store.id, "name": store.name} for store in stores]
    }


@app.get("/store/<string:store_id>")
def get_store(store_id):
    store = StoreModel.query.get(store_id)

    if not store:
        return {"message": "Store not exists"}
    
    return {"id": store.id, "name": store.name, "items": [{"id": item.id, "name": item.name, "price": item.price} for item in store.items]}


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    store = StoreModel.query.get(store_id)

    if not store:
        return {"message": "Store not exists"}
    
    db.session.delete(store)
    db.session.commit()

    return {"message": "Store deleted successfully."}



@app.post("/item")
def create_item():
    data = request.get_json()
    requirement_fields = {"name", "price", "store_id"}

    if not requirement_fields.issubset(data):
        abort(400, message="Bad request. Payload does not contain the name, price or store_id.")

    store = StoreModel.query.get(data["store_id"])

    if not store:
        return {"message": "Store not found"}
    
    item = ItemModel(id=uuid.uuid4().hex, name=data["name"], price=data["price"], store_id=data["store_id"])

    db.session.add(item)
    db.session.commit()

    return {"id": item.id, "name": item.name, "price": item.price, "store_id": item.store_id}, 201

@app.get("/item")
def get_items():
    items = ItemModel.query.all()
    return {
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "store_id": item.store_id
            } 
            for item in items
        ]
    }

# if __name__ == '__main__':
#     app.run(debug=True)



#######################################################
# from flask import Flask,request     # Here flask is a package and Flask is a class
# from db import stores, items
# import uuid                 # alpha numeric number of 16 digits
# from flask_smorest import abort

# app = Flask(__name__)

# @app.post("/store")
# def addStoreDetail():

#     store_data = request.get_json()

#     if "name" not in store_data:
#         abort(400, message="Bad request. Payload does not contain the name.")
    

#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             return {"message": "Store name already exists."}
        
#     store_id = uuid.uuid4().hex
#     store = {**store_data, "id":store_id}
#     stores[store_id] = store

#     return {"message": "values stored"}

# @app.get("/store")
# def getStoreList():
#     return {"stores": list(stores.values())}


# @app.get("/store/<store_id>")
# def getStoreId(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         return {"message" : "Mentioned Store Id does not exists."}


# @app.delete("/store/<store_id>")
# def deleteStoreId(store_id):
#     try:
#         del stores[store_id]
#         return {"message" : "Store deleted successfully."}
#     except KeyError:
#         return {"message" : "Mentioned Store Id does not exists."}


# @app.post("/item")
# def createItems():
#     item_data = request.get_json()

#     if "name" not in item_data or "price" not in item_data or "store_id" not in item_data:
#         abort(400, message="Bad request. Payload does not contain the name, price or store_id.")
    
#     for item in items.values():
#         if item_data["name"] == item["name"]:
#             return {"message": "Item name already exists."}
        
#     if item_data["store_id"] not in stores:
#         return {"message": "Store Id does not exist."}

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id":item_id}
#     items[item_id] = item

#     return {"message": "values stored"}

# @app.get("/item")
# def getitemlist():
#     return {"items": list(items.values())}


# @app.get("/item/<item_id>")
# def getspecificitem(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         return {"message" : "Mentioned Item Id does not exists."}
    

# @app.delete("/item/<item_id>")
# def deletespecificitem(item_id):
#     try:
#         del items[item_id]
#         return {"message" : "Item deleted successfully."}
#     except KeyError:
#         return {"message" : "Mentioned Item Id does not exists."}


# @app.put("/item/<item_id>")
# def updatespecificitem(item_id):
#     item_data = request.get_json()

#     if "name" not in item_data or "price" not in item_data or "store_id" not in item_data:
#         abort(400, message="Bad request. Payload does not contain the name, price or store_id.")

#     if item_id not in items:
#         return {"message" : "Item Id does not exists."}
    
#     item = items[item_id]
#     item |= item_data

#     return {"message" : "Item value is updated."}





###############################################################

# @app.route("/")          # By default API......Here app is object of Flask instance
# def hello_world():
#     return "Hello World"

# store = [
#     {
#         "name" : "spencer",
#         "items" : [
#             {
#                 "name" : "snacks",
#                 "price" : "20"
#             }
#         ]
#     }
# ]

# @app.get("/store")
# def store_list():
#     return store


# @app.post("/store")
# def add_store():
#     request_data = request.get_json()
#     new_data = {"name": request_data["name"], "items": []}
#     store.append(new_data)
#     return store, 200

# @app.post("/store/<string:name>/item")
# def add_items(name):
#     request_data = request.get_json()
#     for stor in store:
#         if stor["name"] == name:
#             new_data = {"name": request_data["name"], "price": request_data["price"]}
#             stor["items"].append(new_data)
#             return stor["name"], 200
#     return {"message" : "store not found"}

# @app.get("/store/<string:name>")
# def get_store_details(name):
#     for stor in store:
#         if stor["name"] == name:
#             return stor
#     return {"message" : "Store not found"}, 404

# @app.get("/store/<string:name>/item")
# def get_items_in_store(name):
#     for stor in store:
#         if stor["name"] == name:
#             return {"items": stor["items"]}
#     return {"message" : "Store not found"}, 404
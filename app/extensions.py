from flask_pymongo import PyMongo

def init_mongo(app):
    # Set MongoDB URI
    app.config["MONGO_URI"] = "mongodb+srv://vidhigaydhane27:74ILH280ndDda7Ry@cluster0.jdm4b.mongodb.net/github_webhook_DB"
    mongo = PyMongo(app)
    return mongo

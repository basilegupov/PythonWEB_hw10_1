# from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
#
#
# def get_mongodb():
#     connect(
#         db="hw9",
#         host="mongodb+srv://user71:19710822@cluster0.wvawurb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
#
#     )
#     db = connect.hw9


from pymongo import MongoClient


def get_mongodb():
    client = MongoClient(
        "mongodb+srv://user71:19710822@cluster0.wvawurb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.hw9
    return db

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageClassification
users = db["Users"]

#check if user exist
def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        #get data from user
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        #check if user exist
        if UserExist(username):
            retJson = {
                "status": 301,
                "error": "username already taken"
            }
            return jsonify(retJson)
            #if user doesnt exist, hash password
        hashedpw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        #insert user in db
        users.insert({
            "Username": username,
            "Password": hashedpw,
            "Tokens": 6
        })
        retJson = {
            "status": 200,
            "message": "account succesfully created"
        }
        return jsonify(retJson)

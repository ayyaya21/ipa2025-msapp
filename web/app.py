import os
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

sample = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")
print(db_name)
client = MongoClient(mongo_uri)
mydb = client[db_name]
collection = mydb["routers"]

@sample.route("/")
def main():
    data = collection.find({}, {'password':0})
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        collection.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        myquery = {'_id': ObjectId(idx)}
        collection.delete_one(myquery)
        # if 0 <= idx < len(data):
        #     data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080, debug=True)
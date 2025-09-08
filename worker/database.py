from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from bson import json_util
from router_client import get_interfaces

load_dotenv()


def save_interface_status(router_ip, interfaces):
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["interface_status"]
    data = {"interfaces": interfaces, "timestamp": datetime.now(timezone.utc)}
    collection.update_one({
        "router_ip": router_ip},
        {"$set": data},
        upsert=True)
    client.close()


def callback(ch, method, props, body):
    job = json_util.loads(body.decode())
    router_ip = job["ip"]
    router_username = job["username"]
    router_password = job["password"]
    output = get_interfaces(router_ip, router_username, router_password)
    save_interface_status(router_ip, output)

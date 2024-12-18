import json
import os
from app import app

def read_json(path):
    with open(path,"r") as f:
        return json.load(f)

def load_revenue():
    return read_json(os.path.join(app.root_path, "data/revenue.json"))

def get_appointment_history(user_id):
    return

def get_appointment_history_detail(user_id, order_id):
    return
import json
import os
from app import app

def read_json(path):
    with open(path,"r") as f:
        return json.load(f)

def load_revenue():
    return read_json(os.path.join(app.root_path, "data/revenue.json"))

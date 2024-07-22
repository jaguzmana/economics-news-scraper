import json
import os

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def append_data_json(path, data):
    with open(path, 'a') as f:
        json.dump(data, f)
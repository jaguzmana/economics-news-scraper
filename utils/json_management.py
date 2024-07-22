import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

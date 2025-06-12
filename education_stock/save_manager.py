import os
import json

SAVE_DIR = "saves"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_game(data, filename):
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_game(filename):
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    with open(filepath, "r") as f:
        return json.load(f)

def delete_game(filename):
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

def list_saved_files():
    return [f.replace(".json", "") for f in os.listdir(SAVE_DIR) if f.endswith(".json")]

def load_game(filename):
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    if not os.path.exists(filepath):
        print(f"❌ 파일 '{filename}.json'이 존재하지 않습니다.")
        return None
    with open(filepath, "r") as f:
        return json.load(f)

def save_game(data, filename):
    filepath = os.path.join(SAVE_DIR, f"{filename}.json")
    with open(filepath, "w") as f:
        json.dump(data, f)

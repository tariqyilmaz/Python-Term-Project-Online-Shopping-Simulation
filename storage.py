import json
import os
from datetime import datetime
from shutil import copy2

def load_json(path: str) -> dict | list:
    try:
        with open(path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Warning: Folder is not found")
        return []

def write_json(path: str, data: dict | list) -> None:
    try:
        with open(path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning {e}")

def ensure_storage_structure(base_dir: str = ".") -> None:
    required_dirs = ["data", "receipts", "backups", "reports"]
    
    print("\n---Storage Structure Control---")
    for dir_name in required_dirs:
        path = os.path.join(base_dir, dir_name)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Directory ready: {path}")
        except OSError as e:
            print(f"Warning, Directory could not be created {path}. Warning: {e}")

def backup_file(source_path: str, backup_dir: str) -> str:   
    if not os.path.exists(source_path):
        print(f"Warning, source file is not found: {source_path}")
        return ""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(source_path) 
    
    name, ext = os.path.splitext(base_name)
    backup_filename = f"{name}_{timestamp}{ext}"
    destination_path = os.path.join(backup_dir, backup_filename)
    
    try:
        copy2(source_path, destination_path) 
        return destination_path
    except Exception as e:
        print(f"Warning, file is not loaded. {source_path} -> {destination_path}. Hata: {e}")
        return ""
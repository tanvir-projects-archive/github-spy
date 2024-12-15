import os
import json
import requests

def create_data_folder(username):
    """
    Creates a folder named after the GitHub username in the 'data' directory.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    user_folder = os.path.join('data', username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def save_to_json(file_path, data):
    """
    Saves data to a JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

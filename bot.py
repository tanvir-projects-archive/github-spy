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

def fetch_user_info(username, token):
    """
    Fetches user information from the GitHub API.
    """
    url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user info for {username}. Status code: {response.status_code}")
        return None

def fetch_user_repos(username, token):
    """
    Fetches repositories for the GitHub user.
    """
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repositories for {username}. Status code: {response.status_code}")
        return None

def fetch_user_followers(username, token):
    """
    Fetches followers for the GitHub user.
    """
    url = f'https://api.github.com/users/{username}/followers'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching followers for {username}. Status code: {response.status_code}")
        return None

def fetch_user_following(username, token):
    """
    Fetches following list for the GitHub user.
    """
    url = f'https://api.github.com/users/{username}/following'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching following list for {username}. Status code: {response.status_code}")
        return None

def process_user_info(user_info):
    """
    Process the user info to match the required format.
    """
    return {
        "username": user_info.get('login', ''),
        "id": user_info.get('id', ''),
        "profile_url": user_info.get('html_url', ''),
        "followers_url": user_info.get('followers_url', ''),
        "following_url": user_info.get('following_url', ''),
        "type": user_info.get('type', ''),
    }

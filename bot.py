import os
import json
import requests
import shutil

GITHUB_TOKEN = "ghp_xxxx"

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
    Fetches all repositories for the GitHub user, handling pagination.
    """
    repos_data = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/repos?page={page}&per_page=100'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos_info = response.json()
            if not repos_info:
                break
            repos_data.extend(repos_info)
            page += 1
        else:
            print(f"Error fetching repositories for {username}. Status code: {response.status_code}")
            break
    return repos_data

def fetch_user_followers(username, token):
    """
    Fetches all followers for the GitHub user, handling pagination.
    """
    followers_data = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/followers?page={page}&per_page=100'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            followers_info = response.json()
            if not followers_info:
                break
            followers_data.extend(followers_info)
            page += 1
        else:
            print(f"Error fetching followers for {username}. Status code: {response.status_code}")
            break
    return followers_data

def fetch_user_following(username, token):
    """
    Fetches all following list for the GitHub user, handling pagination.
    """
    following_data = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/following?page={page}&per_page=100'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            following_info = response.json()
            if not following_info:
                break
            following_data.extend(following_info)
            page += 1
        else:
            print(f"Error fetching following list for {username}. Status code: {response.status_code}")
            break
    return following_data

def process_user_info(user_info):
    """
    Process the user info to match the required format.
    """
    return {
        "username": user_info.get('login', ''),
        "user_id": user_info.get('id', ''),
        "profile_url": user_info.get('html_url', ''),
        "followers_url": user_info.get('followers_url', ''),
        "following_url": user_info.get('following_url', ''),
        "type": user_info.get('type', ''),
    }

def process_repo_info(repos_info):
    """
    Process the repository info to match the required format.
    """
    repos_data = []
    for repo in repos_info:
        repos_data.append({
            "name": repo.get('name', ''),
            "repo_url": repo.get('html_url', ''),
            "description": repo.get('description', ''),
            "language": repo.get('language', ''),
            "created_at": repo.get('created_at', ''),
            "updated_at": repo.get('updated_at', ''),
        })
    return repos_data

def process_followers_following(followers_info, is_following=False):
    """
    Process the followers or following info to match the required format.
    """
    followers_data = []
    for follower in followers_info:
        follower_data = {
            "username": follower.get('login', ''),
            "user_id": follower.get('id', ''),
            "profile_url": follower.get('html_url', ''),
            "followers_url": follower.get('followers_url', ''),
            "following_url": follower.get('following_url', ''),
            "type": follower.get('type', ''),
        }
        if not is_following:
            del follower_data["type"]
        followers_data.append(follower_data)
    return followers_data

def zip_and_move_folder(username):
    """
    Zips the user folder and moves it to the archive directory.
    """
    user_folder = os.path.join('data', username)
    archive_folder = os.path.join('data', 'archive')

    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    zip_file = os.path.join(archive_folder, f"{username}.zip")
    shutil.make_archive(zip_file.replace('.zip', ''), 'zip', user_folder)

    print(f"Your raw folder: {user_folder}")
    print(f"Your compressed zip file: {zip_file}")

def main():
    username = input("Enter the GitHub username to fetch: ")

    print(f"Fetching data for {username}...")

    token = GITHUB_TOKEN if GITHUB_TOKEN else input("Enter your GitHub Personal Access Token: ")

    user_folder = create_data_folder(username)

    user_info = fetch_user_info(username, token)
    if user_info:
        processed_user_info = process_user_info(user_info)
        save_to_json(os.path.join(user_folder, 'user_info.json'), processed_user_info)

    repos_info = fetch_user_repos(username, token)
    if repos_info:
        processed_repos_info = process_repo_info(repos_info)
        save_to_json(os.path.join(user_folder, 'repos.json'), processed_repos_info)

    followers_info = fetch_user_followers(username, token)
    if followers_info:
        processed_followers_info = process_followers_following(followers_info)
        save_to_json(os.path.join(user_folder, 'followers.json'), processed_followers_info)

    following_info = fetch_user_following(username, token)
    if following_info:
        processed_following_info = process_followers_following(following_info, is_following=True)
        save_to_json(os.path.join(user_folder, 'following.json'), processed_following_info)

    summary = {
        "total_repos": len(repos_info) if repos_info else 0,
        "total_followers": len(followers_info) if followers_info else 0,
        "total_following": len(following_info) if following_info else 0,
        "profile_url": processed_user_info['profile_url'] if user_info else '',
    }
    save_to_json(os.path.join(user_folder, 'summary.json'), summary)

    zip_and_move_folder(username)

if __name__ == "__main__":
    main()

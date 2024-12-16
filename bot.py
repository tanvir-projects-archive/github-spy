import os
import json
import requests
import shutil
import telegram
import asyncio
from telegram.constants import ParseMode

GITHUB_TOKEN = "ghp_xxxx"
TELEGRAM_TOKEN = "xxxx"
CHAT_ID = "-100xxxx"

def create_data_folder(username):
    """Creates a folder for the user to store data."""
    if not os.path.exists('data'):
        os.makedirs('data')

    user_folder = os.path.join('data', username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def save_to_json(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def fetch_user_info(username, token):
    """Fetches GitHub user information."""
    url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user info for {username}. Status code: {response.status_code}")
        return None

def fetch_user_repos(username, token):
    """Fetches all repositories for the GitHub user, handling pagination."""
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
    """Fetches all followers for the GitHub user, handling pagination."""
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
    """Fetches all following list for the GitHub user, handling pagination."""
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

def zip_and_move_folder(username):
    """Zips the user folder."""
    user_folder = os.path.join('data', username)
    archive_folder = os.path.join('data', 'archive')

    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    zip_file = os.path.join(archive_folder, f"{username}.zip")
    shutil.make_archive(zip_file.replace('.zip', ''), 'zip', user_folder)

    return zip_file

async def send_telegram_message(zip_file, username, profile_url):
    """Send the formatted message and the zip file as an attachment with caption."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    message = (
        f"*Name:* `{username}`\n"
        f"*URL:* [GitHub Profile]({profile_url})"
    )

    with open(zip_file, 'rb') as file:
        await bot.send_document(chat_id=CHAT_ID, document=file, caption=message, parse_mode=ParseMode.MARKDOWN)

def main():
    username = input("Enter the GitHub username to fetch: ")

    print(f"Fetching data for {username}...")

    user_info = fetch_user_info(username, GITHUB_TOKEN)
    if user_info:
        processed_user_info = {
            "username": user_info.get('login', ''),
            "profile_url": user_info.get('html_url', '')
        }

        user_folder = create_data_folder(username)

        save_to_json(os.path.join(user_folder, 'user_info.json'), processed_user_info)

        repos_info = fetch_user_repos(username, GITHUB_TOKEN)
        if repos_info:
            processed_repos_info = [{"name": repo['name'], "url": repo['html_url']} for repo in repos_info]
            save_to_json(os.path.join(user_folder, 'repos.json'), processed_repos_info)

        followers_info = fetch_user_followers(username, GITHUB_TOKEN)
        if followers_info:
            processed_followers_info = [{"username": follower['login'], "url": follower['html_url']} for follower in followers_info]
            save_to_json(os.path.join(user_folder, 'followers.json'), processed_followers_info)

        following_info = fetch_user_following(username, GITHUB_TOKEN)
        if following_info:
            processed_following_info = [{"username": following['login'], "url": following['html_url']} for following in following_info]
            save_to_json(os.path.join(user_folder, 'following.json'), processed_following_info)

        zip_file = zip_and_move_folder(username)

        asyncio.run(send_telegram_message(zip_file, processed_user_info["username"], processed_user_info["profile_url"]))

        print(f"Your raw folder: {user_folder}")
        print(f"Your compressed zip file: {zip_file}")
        print(f"Message sent successfully for {username}")
        print(f"File sent successfully for {username}")

if __name__ == "__main__":
    main()

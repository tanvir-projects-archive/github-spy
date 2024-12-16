# GitHub Profile Data Scraper with Telegram Integration
- This Python script fetches data from a GitHub user's profile and sends it directly to a Telegram chat, along with saving it locally

## Features
- Fetches data from a GitHub user's profile:
  - **User Info**
  - **Repositories**
  - **Followers**
  - **Following**
- Saves the data as JSON files in a user-specific folder
- Sends a Telegram message with:
  - **Name and profile link**
  - **A ZIP file containing all JSON files**

## Prerequisites
1. **GitHub Personal Access Token (PAT):**
- Create one by following [GitHub's guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

2. **Telegram Bot Token:**
- Get a bot token by creating a bot using [BotFather](https://t.me/botfather)

3. **Chat ID:**
- Find your Telegram chat ID

## Installation
1. Clone this repository:
```bash
git clone https://github.com/tanvir-projects-archive/github-spy && cd github-spy
```

2. Install required libraries:
```bash
pip install -r requirements.txt
```

## Setup
1. Edit the script bot.py and replace these placeholders:
- GITHUB_TOKEN = "ghp_xxxx"
  - Your github personal access token
- TELEGRAM_TOKEN = "xxxx"
  - Your telegram bot api token
- CHAT_ID = "-100xxxx"
  - Your chat ID

## Usage
1. Run the script:
```bash
python bot.py
```

2. Enter the GitHub username when prompted

## Output
1. **Locally Saved Data:**
- The script creates a folder for the username:
- data/username/
- Inside the username folder, the following files will be saved:
 - user_info.json
 - repos.json
 - followers.json
 - following.json
 - summary.json
- data/archive/
- The archive folder will store ZIP files of each username's data for easier transfer

2. **Telegram Message:**
- The bot sends like:
```bash
Name: tanvirr007
URL: github.com/tanvirr007
```
- The ZIP file containing all JSON files

## Notes
- Ensure your tokens are correct to avoid errors
- The script works for users with many followers and repositories by handling pagination
- Enjoy scraping GitHub profiles with Telegram notifications!

## Author
- This script is created by [тαиνir](https://github.com/tanvirr007)
- If you find any issues or want to improve the script, feel free to open a pull request and contact me on [Telegram](https://t.me/tanvirr007)

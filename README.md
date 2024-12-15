# GitHub Profile Data Scrapper
This Python script fetches data from a GitHub user's profile and stores it locally in a structured format, following:
- User info
- List of repositories
- List of followers
- List of users the person is following

## Features
- Saves data in JSON format in a user-specific folder.
- Organizes data into multiple JSON files:
  - user_info.json
  - repos.json
  - followers.json
  - following.json
  - summary.json

## Prerequisites
Before running this script, ensure you have:
- A **GitHub Personal Access Token** (PAT) for accessing the GitHub API.
- To create a GitHub Personal Access Token (PAT), follow [GitHub's official guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

## Installation
1. Clone or download the repository:
    ```bash
    git clone https://github.com/tanvir-projects-archive/github-spy
    cd github-spy
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Replace "ghp_xxxx" in the GITHUB_TOKEN variable in the script with your GitHub token like:
    ```bash
    GITHUB_TOKEN = "ghp_asdfqwertypoiuytlkjhg"
    ```
   Alternatively, you can enter your token when prompted

2. Run the script:
    ```bash
    python bot.py
    ```

3. Enter the GitHub username you wish to fetch data for when prompted

## Output
The script will create a folder path:

- data/username/
- Inside the username folder, the following files will be saved:
 - user_info.json
 - repos.json
 - followers.json
 - following.json
 - summary.json

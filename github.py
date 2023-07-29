import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Make sure to replace 'your-token' with your actual token
headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}


# Replace 'username' with your username and 'repo' with your repository name
response = requests.get('https://api.github.com/repos/baileyg2016/', headers=headers)

print(response.json())

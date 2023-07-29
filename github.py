import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

# Make sure to replace 'your-token' with your actual token
files_url = 'https://api.github.com/repos/baileyg2016/finTracker/contents'
headers = {
    'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}',
    'Accept': 'application/vnd.github.v3+json'
  }

def decode_file(file):
    file_content_base64 = file['content']
    return base64.b64decode(file_content_base64).decode('utf-8')

def get_all_files(url=files_url):
    response = requests.get(url, headers=headers)
    files = response.json()
    file_paths = []

    for file in files:
        if file['type'] == 'file':
          file_paths.append(file['path'])
        elif file['type'] == 'dir':
          file_paths.extend(get_all_files(file['url']))

    return file_paths

# response = requests.get('https://api.github.com/repos/baileyg2016/finTracker/contents', headers=headers)
# print(response.json())

# response = requests.get('https://api.github.com/repos/baileyg2016/finTracker/contents/README.md', headers=headers)
# file_content = decode_file(response.json())

file_paths = get_all_files()
print(file_paths)
import os
import requests
from dotenv import load_dotenv
import base64
import numpy as np

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

def get_all_files(url):
    response = requests.get(url, headers=headers)
    files = response.json()
    file_contents = {}

    for file in files:
        if file['type'] == 'file' and [file['name'].endswith(ext) for ext in ['.py', '.js', '.ts', '.css']].count(True) > 0:
            file_response = requests.get(file['url'], headers=headers)
            file_content = decode_file(file_response.json())
            file_contents[file['path']] = file_content
        elif file['type'] == 'dir':
            file_contents.update(get_all_files(file['url']))

    return file_contents

def load_files(url):
    response = requests.get(url, headers=headers)
    files = np.array(response.json())
    file_contents = {}

    for file in files:
        if file['type'] == 'file' and [file['name'].endswith(ext) for ext in ['.py', '.js', '.ts', '.css']].count(True) > 0:
            file_response = requests.get(file['url'], headers=headers)
            file_content = decode_file(file_response.json())
            file_contents[file['path']] = file_content
        elif file['type'] == 'dir':
            print(file)
            print(file['url'])
            file_contents.update(get_all_files(file['url']))

    return file_contents

files = get_all_files(files_url)
print('number of files:', len(files))
print(files)


import os
import requests
import base64

class Repo:
    def __init__(self, repo_url, token=os.getenv('GITHUB_TOKEN')):
        self.repo_url = repo_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def decode_file(self, file):
        file_content_base64 = file['content']
        return base64.b64decode(file_content_base64).decode('utf-8')

    def get_all_files(self, url):
        response = requests.get(url, headers=self.headers)
        files = response.json()
        file_contents = {}

        for file in files:
            if file['type'] == 'file' and [file['name'].endswith(ext) for ext in ['.py', '.js', '.ts', '.css']].count(True) > 0:
                file_response = requests.get(file['url'], headers=self.headers)
                file_content = self.decode_file(file_response.json())
                file_contents[file['path']] = file_content
            elif file['type'] == 'dir':
                file_contents.update(self.get_all_files(file['url']))

        return file_contents

    def load_files(self):
        return self.get_all_files(self.repo_url)

import requests
from bs4 import BeautifulSoup
import base64
import json

def get_file_structure(repo_url):
    owner, repo = repo_url.split('/')[-2:]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return [{'name': item['path'], 'type': 'file' if item['type'] == 'blob' else 'directory'} for item in data['tree']]
    return []

def get_readme_content(repo_url):
    owner, repo = repo_url.split('/')[-2:]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        return content
    return 'No README available'
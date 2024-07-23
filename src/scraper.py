import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def parse_stars(stars_str):
    if 'k' in stars_str:
        return int(float(stars_str.replace('k', '')) * 1000)
    elif 'M' in stars_str:
        return int(float(stars_str.replace('M', '')) * 1000000)
    else:
        return int(stars_str.replace(',', ''))

def get_trending_repos(date=None, language=None, since='daily'):
    url = "https://github.com/trending"
    params = {}
    if language:
        params['language'] = language
    if since:
        params['since'] = since

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for article in soup.select('article.Box-row'):
        repo = {}
        repo['name'] = article.select_one('h2 a').text.strip().replace('\n', '').replace(' ', '')
        repo['url'] = f"https://github.com{article.select_one('h2 a')['href']}"
        repo['author'] = repo['name'].split('/')[0]
        stars_elem = article.select_one('span.d-inline-block.float-sm-right')
        repo['stars'] = stars_elem.text.strip() if stars_elem else 'N/A'
        
        # 使用新的 parse_stars 函数来处理不同格式的 stars
        try:
            repo['stars_count'] = parse_stars(repo['stars'])
        except ValueError:
            repo['stars_count'] = 0
        
        description = article.select_one('p.col-9')
        repo['description'] = description.text.strip() if description else 'No description available'

        repos.append(repo)
    
    # 按 stars_count 降序排序
    repos.sort(key=lambda x: x['stars_count'], reverse=True)
    
    return repos
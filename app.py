from flask import Flask, render_template, request, jsonify
from src.scraper import get_trending_repos
from src.utils import get_readme_content, get_file_structure
import markdown
import traceback
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    date_str = request.args.get('date')
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    limit = int(request.args.get('limit', 10))

    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now().date()
    
    repos = get_trending_repos(date=date, language=language, since=since)[:limit]
    current_date = datetime.now().strftime('%Y-%m-%d')

    return render_template('index.html', repos=repos, current_date=current_date, 
                           selected_date=date_str, selected_language=language, 
                           selected_since=since, selected_limit=limit)

@app.route('/details/<path:repo_name>')
def details(repo_name):
    try:
        all_repos = get_trending_repos()
        repo = next((r for r in all_repos if r['name'] == repo_name), None)
        if repo:
            readme_content = get_readme_content(repo['url'])
            readme_html = markdown.markdown(readme_content)
            file_structure = get_file_structure(repo['url'])
            return render_template('details.html', repo=repo, readme_content=readme_html, file_structure=file_structure)
        return "Repository not found", 404
    except Exception as e:
        app.logger.error(f"Error in details route: {str(e)}")
        app.logger.error(traceback.format_exc())
        return f"An error occurred: {str(e)}", 500

@app.route('/update_trending')
def update_trending():
    date_str = request.args.get('date')
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    limit = int(request.args.get('limit', 10))

    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now().date()
    
    repos = get_trending_repos(date=date, language=language, since=since)[:limit]
    
    # 为了 JSON 序列化，我们需要将 stars_count 转换回字符串
    for repo in repos:
        repo['stars_count'] = str(repo['stars_count'])
    
    return jsonify(repos)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
from jinja2 import Environment, FileSystemLoader

def generate_html(repos):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('trending.html')
    
    html_content = template.render(repos=repos)
    
    with open('trending.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
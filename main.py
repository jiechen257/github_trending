from src.scraper import get_trending_repos
from src.html_generator import generate_html

def main():
    repos = get_trending_repos()
    generate_html(repos)
    print("HTML file generated: trending.html")

if __name__ == "__main__":
    main()
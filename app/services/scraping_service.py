import requests
from bs4 import BeautifulSoup

# scrape the website using the url
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator='\n')
    return text

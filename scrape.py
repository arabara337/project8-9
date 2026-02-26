import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://quotes.toscrape.com"

quotes_data = []
authors_data = []
authors_seen = set()


def scrape_author(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "html.parser")

    fullname = soup.find("h3", class_="author-title").get_text(strip=True)
    born_date = soup.find("span", class_="author-born-date").get_text(strip=True)
    born_location = soup.find("span", class_="author-born-location").get_text(strip=True)
    description = soup.find("div", class_="author-description").get_text(strip=True)

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes():
    page_url = BASE_URL

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            # Сбор данных об авторе
            if author not in authors_seen:
                author_relative_url = quote.find("a")["href"]
                author_url = urljoin(BASE_URL, author_relative_url)

                author_info = scrape_author(author_url)
                authors_data.append(author_info)
                authors_seen.add(author)

        next_button = soup.find("li", class_="next")
        if next_button:
            next_page = next_button.find("a")["href"]
            page_url = urljoin(BASE_URL, next_page)
        else:
            page_url = None


scrape_quotes()

# Сохранение файлов
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(authors_data, f, ensure_ascii=False, indent=4)

print("Scraping completed successfully!")python load_authors.py
python load_quotes.py
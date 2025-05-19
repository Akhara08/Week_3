# researcher.py
import requests
from bs4 import BeautifulSoup
from readability import Document

class Researcher:
    def __init__(self):
        pass

    def extract_main_text(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')

        # Try multiple known containers for article content
        selectors = [
            {'id': 'mw-content-text'},            # Wikipedia
            {'class': 'entry-content'},            # GeeksforGeeks
            {'class': 'post-content'},             # Blogs
            {'class': 'article-content'},          # Other
            {'id': 'content'},                     # Generic fallback
        ]

        content_div = None
        for sel in selectors:
            if 'id' in sel:
                content_div = soup.find('div', id=sel['id'])
            elif 'class' in sel:
                content_div = soup.find('div', class_=sel['class'])
            if content_div:
                break

        if content_div:
            paragraphs = content_div.find_all('p')
            text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            if text.strip():
                return text

        print("[Researcher] Warning: Main content div not found or empty, using readability fallback")

        # Fallback to readability-lxml extraction
        doc = Document(html)
        summary_html = doc.summary()
        summary_soup = BeautifulSoup(summary_html, 'html.parser')
        paragraphs = summary_soup.find_all('p')
        text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        return text

    async def process(self, url: str) -> str:
        print(f"[Researcher] Fetching URL: {url}")
        response = requests.get(url)
        html = response.text
        print(f"[Researcher] Fetched {len(html)} characters")

        main_text = self.extract_main_text(html)
        print(f"[Researcher] Extracted {len(main_text)} characters of main content")
        return main_text

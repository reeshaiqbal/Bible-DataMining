# Bible Data Mining Project
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import time

# Lists to store scraped data
books = []
chapters = []
verses = []
texts = []

# User-Agent to avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

# Example: Scraping Genesis chapters 1-2 from bible.com (ES version)
base_url = "https://www.bible.com/es/bible/146/GEN."

print("Scraping Bible text...")

for chapter in range(1, 3):  # Adjust range for more chapters
    url = f"{base_url}{chapter}.RVC"
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "html.parser")
    
    # Extract verses
    verse_spans = soup.find_all("span", attrs={"class":"ChapterContent_content__dkdqo"})
    for idx, v in enumerate(verse_spans, start=1):
        text = v.text.strip()
        if text:
            books.append("Genesis")
            chapters.append(chapter)
            verses.append(idx)
            texts.append(text)
    
    time.sleep(1)  # polite scraping

# Create DataFrame
bible_df = pd.DataFrame({
    "Book": books,
    "Chapter": chapters,
    "Verse": verses,
    "Text": texts
})

# Save to CSV
bible_df.to_csv("bible_genesis.csv", index=False, encoding="utf-8-sig")

print("Scraping completed! Data saved to bible_genesis.csv")

# --- Optional Data Science Analysis ---

# Example: Word frequency
from collections import Counter
import re

all_text = " ".join(bible_df["Text"].tolist()).lower()
words = re.findall(r"\b\w+\b", all_text)
word_freq = Counter(words)

# Top 20 most frequent words
top_words = word_freq.most_common(20)
print("Top 20 frequent words:", top_words)

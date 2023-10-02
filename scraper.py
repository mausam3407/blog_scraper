import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

source_url = "https://blog.tax2win.in/"
page = ""

data = []

n_pages = int(input("Enter Number of pages: "))

for i in range(n_pages):
    url = source_url + page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    page = soup.find("a", class_ = "wp-block-query-pagination-next")
    page = page.attrs['href']
    blogs = soup.find_all("a", {"target": "_self"})
    for blog in blogs:
        if blog.attrs.get("aria-current"):
            continue
        blog_link = blog.attrs.get('href')
        try:
            response = requests.get(blog_link)
            blog_soup = BeautifulSoup(response.text, 'html.parser')
            bl = blog_soup.find("div", class_ = "col-md-9 col-lg-9 pd0mobile")
            if bl:
                text = bl.text.strip()
            else:
                text = ""
            table = blog_soup.find_all("table")
            for tab in table:
                if tab:
                    df = pd.read_html(str(tab))[0]
                    text = text + "\n" + df.to_markdown()
            data.append({"title":blog.text, "content": text})
        except Exception as e:
            print(e)
            print(f"couldn't find {blog}")

with open("data.json", "w") as f:
    json.dump(data, f)
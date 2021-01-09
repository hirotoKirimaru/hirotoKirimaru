import requests
from bs4 import BeautifulSoup
# Webページを取得して解析する

load_url = "https://lapras.com/public/JFCUKEW"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

# HTML全体を表示する
# print(soup)
content = ""
for tag in soup.find_all(name = "meta"):
    content = tag['content']
    if "https://media.lapras.com/media/public_setting" in content:
        break

print(content)

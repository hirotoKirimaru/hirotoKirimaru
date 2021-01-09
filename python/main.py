import requests
import sys
import os
from bs4 import BeautifulSoup
# Webページを取得して解析する

# 自分のURLを入力する
load_url = "https://lapras.com/public/JFCUKEW"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

content = ""
for tag in soup.find_all(name = "meta"):
    content = tag['content']
    if "https://media.lapras.com/media/public_setting" in content:
        break

# 事前にファイルのパスを持っておき、同一だった場合は更新しない
read = "";
with open("path.txt", "r") as path:
    read = path.read()
    # if read in content:
#         sys.exit()

# 先にREADMEを更新する
after = ""
with open("../README.md", "r") as readme:
    after = readme.read().replace(read, content)

with open("../README.md", "w") as readme:
    readme.write(after)

# 同一だったので更新する
with open("path.txt", "w") as path:
    path.write(content)


# os.system("git add .")
# os.system("git commit -m '[Auto] Update'")
# os.system("git push")

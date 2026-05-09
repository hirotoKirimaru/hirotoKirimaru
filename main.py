import requests
import sys
import os
from selectolax.parser import HTMLParser
# Webページを取得して解析する

# 自分のURLを入力する
load_url = "https://lapras.com/public/JFCUKEW"
html = requests.get(load_url)
tree = HTMLParser(html.content)

content = ""
for tag in tree.css("meta"):
    value = tag.attributes.get("content") or ""
    if "https://media.lapras.com/media/public_setting" in value:
        content = value
        break

# 事前にファイルのパスを持っておき、同一だった場合は更新しない
read = "";
with open("path.txt", "r") as path:
    read = path.read()
    if read in content:
        sys.exit()

# 先にREADMEを更新する
after = ""
with open("README.md", "r") as readme:
    after = readme.read().replace(read, content)

with open("README.md", "w") as readme:
    readme.write(after)

# 同一だったので更新する
with open("path.txt", "w") as path:
    path.write(content)

print(os.system("after"))

os.system("git config --local user.email 'nainaistar@gmail.com'")
os.system("git config --local user.name 'nainaistar'")
os.system("git add .")
os.system("git commit -m '[Auto] Update'")
os.system("git push")

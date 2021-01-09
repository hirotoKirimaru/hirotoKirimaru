import requests
import sys
import os
from bs4 import BeautifulSoup
# Webページを取得して解析する

load_url = "https://lapras.com/public/JFCUKEW"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

content = ""
for tag in soup.find_all(name = "meta"):
    content = tag['content']
    if "https://media.lapras.com/media/public_setting" in content:
        break

path = open("path.txt", "r")

if path.read() in content:
    sys.exit()
print("***********")

path = open("path.txt", "w")

path.write(content)

os.system("git add .")
os.system("git commit -m '[Auto] Update'")
os.system("git push")

# repo = git.Repo()
# print(repo)

# # repo = git.repo("https://github.com/hirotoKirimaru/hirotoKirimaru.git")
# print(repo.git.branch())
# print("*********")
# repo.git.add("path.txt")
# repo.git.commit("path.txt", "update file")
# repo.git.push('origin', "master")

print("***********")

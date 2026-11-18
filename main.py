"""LAPRAS の公開プロフィールからカード画像の URL を取り、README.md を更新して push する。

環境変数 DRY_RUN が空でなければ、README.md と path.txt の更新までで commit / push はしない
（pull_request のワークフローで使う）。
"""

import os
import subprocess
import sys

import requests
from scrapling.parser import Selector

# 自分のURLを入力する
LOAD_URL = "https://lapras.com/public/JFCUKEW"
CARD_URL_PREFIX = "https://media.lapras.com/media/public_setting"


def fetch_card_url() -> str:
    response = requests.get(LOAD_URL, timeout=30)
    response.raise_for_status()
    page = Selector(response.text)
    for tag in page.css("meta"):
        value = tag.attrib.get("content") or ""
        if CARD_URL_PREFIX in value:
            return value
    return ""


def main() -> int:
    content = fetch_card_url()
    # 以前は見つからなくても先へ進み、README の画像 URL を空文字で置き換えて push していた
    if not content:
        print(f"カード画像の URL がページに見つかりません: {LOAD_URL}", file=sys.stderr)
        return 1

    # 事前にファイルのパスを持っておき、同一だった場合は更新しない
    with open("path.txt") as path:
        read = path.read()
    if read and read in content:
        print("変更なし")
        return 0

    with open("README.md") as readme:
        before = readme.read()
    if read not in before:
        print("README.md に以前のカード画像の URL がありません", file=sys.stderr)
        return 1
    with open("README.md", "w") as readme:
        readme.write(before.replace(read, content))
    with open("path.txt", "w") as path:
        path.write(content)

    if os.environ.get("DRY_RUN"):
        print("DRY_RUN のため commit / push しない")
        return 0

    # 失敗をそのまま落とす（以前は os.system で、push に失敗しても成功扱いになっていた）
    git = ["git", "-c", "user.email=nainaistar@gmail.com", "-c", "user.name=nainaistar"]
    subprocess.run([*git, "add", "README.md", "path.txt"], check=True)
    subprocess.run([*git, "commit", "-m", "[Auto] Update"], check=True)
    subprocess.run(["git", "push"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

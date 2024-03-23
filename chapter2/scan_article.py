#!/usr/bin/env python3

"""
URLを指定したらその文章の内容を要約するbot
"""

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import urllib.parse

# bs4って何?
# [10分で理解する Beautiful Soup \#Python \- Qiita](https://qiita.com/Chanmoro/items/db51658b073acddea4ac)

target_url = "https://netafull.net/macos/0147601.html"


# urlの内容を取得し、body部の articleタグ内のテキストを返す
def getArticleOfUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("article")
    return article.get_text()


def getBodyOfUrl(url):
    # urlの bodyタグの内容を返す
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find("body")
    return body.get_text()


# getBodyOfUrl を使うと プロンプトの長さ上限に達してしまう。サイトごとに適切な取得方法を選ぶ必要がある。

#
#
#
article = getArticleOfUrl(target_url)
article_quote = urllib.parse.quote(article)

prompt = f"""以下の記事の主要コンテンツを見つけ、100文字程度でまとめてください。
```
{article_quote}
```
"""

# prompt_quote = urllib.parse.quote(prompt)
# print(prompt_quote)

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

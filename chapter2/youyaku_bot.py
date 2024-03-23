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


# urlの内容を取得し、body部の articleタグ内のテキストを返す
def getContentOfUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("article")
    return article.get_text()


article = getContentOfUrl("https://netafull.net/macos/0147601.html")

prompt = f"""以下の記事を100文字程度で要約してください。
```
{article}
```
"""

prompt_quote = urllib.parse.quote(prompt)
# print(prompt_quote)

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_quote}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

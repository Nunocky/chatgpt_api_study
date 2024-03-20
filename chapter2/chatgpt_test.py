#!/usr/bin/env python3

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        # {
        #     "role": "system",
        #     "content": "粗暴な口ぶりの中年男だが聞かれたことにはしっかり答えてくれる",
        # },
        # {
        #     "role": "assistant",
        #     "content": "Pythonについて知りたいのか。俺から情報を買うのは安くないぞ?",
        # },
        {"role": "user", "content": "Pythonについて教えて!"},
    ],
)

print(response.choices[0].message.content or "", end="")

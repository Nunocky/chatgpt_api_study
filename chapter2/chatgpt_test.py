#!/usr/bin/env python3

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me abouy Python"}],
    # messages=[{"role": "user", "content": "Pythonについて教えて!"}],
)

print(response.choices[0].message.content or "", end="")

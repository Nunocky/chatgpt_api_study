#!/usr/bin/env python3

# 仕様
# 1.「質問を入力してください」と表示
# 2. ChatGPTへの質問を入力する
# 3. ChatGPTから質問に対する回答を表示する
# 4. 2,3 を繰り返す
# 5. exit と入力したら、プログラムを終了する

import os
from openai import OpenAI

client = OpenAI()

# 最初にメッセージを表示
print("質問を入力してください")

conversation_history = []

while True:
    # ユーザーの入力 -> user_inputに格納
    user_input = input()

    # ユーザーがexitと入力したらプログラムを終了
    if user_input == "exit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )

    # ChatGPTの応答内容を会話履歴に追加
    chatgpt_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": chatgpt_response})

    # ターミナルにChatGPTの応答内容を表示
    print("ChatGPT:", chatgpt_response)

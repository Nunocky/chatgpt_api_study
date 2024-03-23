#!/usr/bin/env python3

"""
仕様
app.pyを拡張し、 search.pyに質問を渡して回答を生成させる。
"""

import os
from openai import OpenAI
from search import answer_question

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

    answer = answer_question(user_input, conversation_history)

    print("ChatGPT:", answer)

    conversation_history.append({"role": "assistant", "content": answer})

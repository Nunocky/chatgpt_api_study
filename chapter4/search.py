#!/usr/bin/env python3


# [Embeddings_utils distance formulas - where did it move?](https://community.openai.com/t/embeddings-utils-distance-formulas-where-did-it-move/479868/2)

import os
import pandas as pd
from openai import OpenAI
import numpy as np
import tiktoken
from scipy.spatial.distance import cosine

client = OpenAI()


def get_embedding(text, model="text-embedding-ada-002"):
    # model = "deployment_name"
    return client.embeddings.create(input=[text], model=model).data[0].embedding


# 新しいAPIを使って、類似度を計算する
def distance_from_embeddings(x, y):
    return np.array([cosine(x, y_i) for y_i in y])


def create_context(question, df, max_len=1800):
    """
    質問と学習データを比較して、コンテキストを作成する
    """

    # 質問をベクトル化
    q_embeddings = (
        client.embeddings.create(input=question, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )

    # q_embeddings = (
    #     OpenAI.embeddings.create(input=question, model="text-embedding-ada-002")
    #     .data[0]
    #     .embedding
    # )

    # 質問と学習データと比較してコサイン類似度を計算し、 distances列に格納する

    # TODO 以下の実装は古いAPIを使用しており、使いことができない。
    #      これを改善したい。
    # df["distances"] = df["embeddings"].apply(
    #     lambda x: cosine(eval(x), q_embeddings)
    # )
    df["distances"] = distance_from_embeddings(
        q_embeddings, df["embeddings"].apply(eval)
    )

    # コンテキストを格納するためのリスト
    returns = []

    # コンテキストの現在の長さ
    cur_len = 0

    # 学習データを類似度順にソートし、トーク数の上限までコンテキストに追加する
    for i, row in df.sort_values("distances", ascending=True).iterrows():
        # テキストの長さを現在の長さに加える
        cur_len += row["n_tokens"] + 4

        # テキストが長すぎる場合はループを終了
        if cur_len > max_len:
            break

        # コンテキストのリストに追加
        returns.append(row["text"])

    # コンテキストを結合して返す
    return "\n\n###\n\n".join(returns)


def answer_question(question, conversation_history):
    """
    コンテキストに基づいて質問に答える
    """

    # 学習データを読み込む
    df = pd.read_csv("embeddings.csv")

    context = create_context(question, df, max_len=200)

    # プロンプトを作成し、会話の履歴に追加
    prompt = f"あなたはとあるホテルのスタッフです。コンテキストに基づいて、お客様からの質問に丁寧に答えてください。コンテキストが質問に対して回答できない場合は「わかりません」と答えてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question} \n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # ChatGPTからの回答を生成
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=1,
        )

        # ChatGPtの回答を返す
        return response.choices[0].message.content.strip()
    except Exception as e:
        # エラーが発生した場合は空の文字列を返す
        print(e)
        return ""

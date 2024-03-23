#!/usr/bin/env python3

import pandas as pd
import tiktoken
import openai

client = openai.Client()

# from openai.embeddings_utils import get_embedding
# openai.embeddings_utils is dropped in the latest version of openai-python
# https://github.com/openai/openai-python/issues/676


def get_embedding(text, model="text-embedding-ada-002"):
    # model = "deployment_name"
    return client.embeddings.create(input=[text], model=model).data[0].embedding


embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_tokens = 1500

df = pd.read_csv("scraped.csv")
df.columns = ["fname", "text"]

tokenizer = tiktoken.get_encoding(embedding_encoding)
df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))


def split_into_many(text, max_tokens=500):
    # テキストを文ごとに分割し、各文のトークン数を取得
    sentences = text.split("。")
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # 各文とトークンを組み合わせてループ処理
    for sentence, token in zip(sentences, n_tokens):
        # これまでのトークン数と現在の文のトークン数を合計した値が
        # 最大トークン数を超える場合は、チャンクをチャンクのリストに追加し、
        # チャンクとトークン数をリセットする
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # 現在の文のトークン数が最大トークン数より大きい場合は、次の文へ進む
        if token > max_tokens:
            continue

        # チャンクに文を追加し、トークン数を更新
        chunk.append(sentence)
        tokens_so_far += token + 1

    # 最後のチャンクをチャンクのリストに追加
    if chunk:
        chunks.append(". ".join(chunk) + ".")

    return chunks


# 短縮されたテキストを格納するための空のリスト
shortened = []

# DataFrameの各行に対してループ処理
for row in df.iterrows():
    # テキストが Noneの場合は、スキップ
    if row[1].text is None:
        continue

    # トークン数が最大トークン数より大きい場合は、テキストを shortendedリストに追加
    if row[1].n_tokens > max_tokens:
        shortened = split_into_many(row[1].text)
    else:
        shortened.append(row[1].text)

# shortened をもとに新しいDataFrameを作成し、列名を text とする
df = pd.DataFrame(shortened, columns=["text"])

# 各 text のトークン数を計算し、新しい列 n_tokens に格納する
df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# text 列のテキストに対して embedding を行い、 CSVファイルに保存
df["embeddings"] = df.text.apply(lambda x: get_embedding(x, embedding_model))
df.to_csv("embeddings.csv")

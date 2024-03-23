# 手順

チャットボットを作る章。ルールは data.txtで定義されている。

これを以下の手順で変換する。

```
data.txt -> (text_to_csv_converter.py) -> scraped.txt -> (text_embedding.py) -> embeddings.csv
```

生成された `embeddings.csv` を `app2.py`で使用する。
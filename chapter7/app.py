#! /usr/bin/env python3

from load_pdf import load_all_pdfs
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FuncFormatter


def write_to_csv(billing_data):
    # CSVファイル名
    csv_file = "invoices.csv"

    # ヘッダーを決定 (JSONのキーから)
    header = billing_data[0].keys()

    # CSVファイルを書き込みモードで開く
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for data in billing_data:
            writer.writerow(data)


def draw_graph(csvFileName):
    df = pd.read_csv(csvFileName, thousands=",")
    df["日付"] = pd.to_datetime(
        df["日付"].str.replace("年", "-").str.replace("月", "-").str.replace("日", ""),
        format="%Y-%m-%d",
    )

    # グラフの描画
    fig, ax = plt.subplots()
    ax.bar(df["日付"], df["請求金額 (合計)"])
    ax.set_xlabel("日付")
    ax.set_ylabel("請求金額 (合計)")
    ax.set_xticks(df["日付"])
    ax.set_xticklabels(df["日付"].dt.strftime("%Y-%m-%d"), rotation=45)

    # y軸の最小値を 0に設定
    ax.set_ylim(0, max(df["請求金額 (合計)"]) + 100000)

    # 縦軸のラベルを元の数字のまま表示
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    plt.tight_layout()
    plt.show()


def main():
    billing_data = load_all_pdfs("data")
    print("読み込みが完了しました")

    # JSON形式のデータを CSVに書き込む
    write_to_csv(billing_data)

    draw_graph("invoices.csv")


if __name__ == "__main__":
    main()

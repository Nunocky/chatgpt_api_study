#! /usr/bin/env python3

import os
import re
import json
from pprint import pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


def extract_and_parse_json(text):
    """
    テキストからJSON文字列を抽出し、辞書型に変換する。
    """
    # pprint("-----")
    # pprint(text)
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        json_string = match.group() if match else ""
        # pprint(json_string)
        j = json.loads(json_string)
        return j
        # pprint(j)
        # MEMO キーと値がシングルクオートで囲まれている。 JSON テキストとするにはダブルクオートで囲む必要がある。
        # そのために dumpsを使う。
        # json_output = json.dumps(j, ensure_ascii=False)
        # pprint(json_output)
        # return json_output
        # pprint("-----")
    except (AttributeError, json.JSONDecodeError):
        return {}


def load_all_pdfs(directory):
    """
    directory フォルダ以下のPDFファイルを読み込み、JSON形式のデータの配列を返す
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    # pprint(f"{pdf_files}")

    contents = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        prompt = f"""
            ### 指示
            以下に示すデータは、請求書の PDFデータをテキスト化したものです。
            請求書データを、下記のキーを持つ JSON形式に変換してください。

            キー:
                * 日付
                * 請求番号
                * インボイス番号
                * 会社名
                * 住所
                * 件名
                * 請求金額
                * お支払い期限
                * 詳細
                * 小計
                * 消費税
                * 請求金額 (合計)
                * 振込先

            ### 注意
            キーに該当するテキストが見つからなければ、値は空欄にしてください。

            下記は弊社の情報なので、JSONの出力に含めないでください。
            * AIビジネスソリューション株式会社
            * 〒135-0021 東京都江東区有明1-1-1

            出力はJSON形式の標準に従い、すべてのキーと値をダブルクオーテーションで囲んでください                        

            ### 例
            以下はとある請求書のデータを JSON形式に変換した場合の例です。

            {
                "日付", "2023年10月31日",
                "請求番号", "2023-1031",
                "インボイス番号", "T0123456789012",
                "会社名", "テクノロジーソリューションズ株式会社",
                "住所", "〒123-4567 東京都中央区銀座1-1-1",
                "件名", "ウェブサイトリニューアルプロジェクト",
                "請求金額", "667,810",
                "お支払い期限", "2023年11月30日",
                "詳細", "ディレクション費用 ¥100,000 / 開発費用 ¥150,000",
                "小計", "250,000",
                "消費税", "25,000",
                "請求金額 (合計)", "667,810",
                "振込先", "AA銀行 BB支店 普通口座 1234567"
            }

            ### 変換する請求書データ
            {pages[0].page_content}
        """

        result = llm([HumanMessage(content=prompt)])

        json = extract_and_parse_json(result.content)
        contents.append(json)
    return contents


if __name__ == "__main__":
    directory = "data"
    contents = load_all_pdfs(directory)
    print(contents)

#     text = """{
#      "日付": "2023年11月09日",
#      "請求番号": "20231109-001",
#      "インボイス番号": "",
#      "会社名": "株式会社テクノロジーサービス",
#      "住所": "〒1234568 東京都渋谷区1-1-2",
#      "件名": "新規ウェブサイト構築",
#      "請求金額": "330,000",
#      "お支払い期限": "2023年07月31日",
#      "詳細": "ディレクション費用 1300,000 300,000",
#      "小計": "300,000",
#      "消費税": "30,000",
#      "請求金額 (合計)": "330,000",
#      "振込先": "AA銀行 CC支店 普通 1234568"
#  }"""

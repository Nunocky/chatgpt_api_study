import openai
import pprint

client = openai.Client()

filename = "0_I_AM_A_CAT.m4a"
audio_file = open(filename, "rb")

#
# 文字起こし
#
print("## Translate into English\n")
transcription = client.audio.translations.create(model="whisper-1", file=audio_file)

# pprint.pp(transcription)

print(transcription.text)

#
#
#
print("## 要約 in Japanese\n")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"以下の文章を日本語に翻訳して、3行の箇条書きで要約してください。\n{transcription.text}",
        },
    ],
)

print(response.choices[0].message.content)

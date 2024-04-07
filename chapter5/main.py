from openai import OpenAI

client = OpenAI()

filename = "0_I_AM_A_CAT.m4a"

# 文字起こし
print("## 文字起こし")
print(f"ファイル名 : {filename}")
audio_file = open(filename, "rb")
transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(transcription.text)


# 要約
print("## 要約")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"以下の文章を140文字以内に要約してください。\n{transcription.text}",
        },
    ],
)

print(response.choices[0].message.content)

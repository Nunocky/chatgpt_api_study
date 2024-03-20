#!/usr/bin/env python3

# https://pypi.org/project/openai/
# tested on openai 1.14.2

# Webページに書いているのをそのまま書いてみたが動作しない。わからないので先送りにする

from openai import OpenAI

client = OpenAI()

#     thread_id=thread.id,
#               ^^^^^^
# NameError: name 'thread' is not defined

with client.beta.threads.runs.create_and_stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
) as stream:
    for event in stream:
        # Print the text from text delta events
        if event.type == "thread.message.delta" and event.data.delta.content:
            print(event.data.delta.content[0].text)

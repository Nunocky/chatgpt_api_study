#!/usr/bin/env python3

from pprint import pprint
from langchain.agents import Tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent


def create_question(user_input):
    return {
        "input": f"""
            あなたはニュース記事を書くブロガーです。
            下記のテーマについて、 google検索で最新情報を取得し、取得した情報に基づいてニュース記事を書いてください。
            1000文字以上で、日本語で出力してください。
            記事の末尾に参照元としてタイトルと URL を出力してください。
            ### テーマ : {user_input}
            """
    }


def define_tools():
    search = GoogleSearchAPIWrapper()
    return [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you nedd to answer questions about current events. you should ask targeted questions",
        )
    ]


def write_response_to_file(response, filename):
    # pprint(response)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response["output"])
    print("出力が完了しました")


if __name__ == "__main__":
    user_input = input("記事のテーマを入力してください: ")
    question = create_question(user_input)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=2000)
    tools = define_tools()
    prompt = hub.pull("hwchase17/openai-tools-agent")
    # TODO PromptTemplate はもう使われないの?
    pprint(prompt)

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = agent_executor.invoke(question)

    write_response_to_file(response, "output.txt")

# hub.pull("hwchase17/openai-tools-agent") を使ったときの promptの中身
# ChatPromptTemplate(
#     input_variables=['agent_scratchpad', 'input'],
#     input_types={'chat_history': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]],
#                  'agent_scratchpad': typing.List[typing.Union[langchain_core.messages.ai.AIMessage, langchain_core.messages.human.HumanMessage, langchain_core.messages.chat.ChatMessage, langchain_core.messages.system.SystemMessage, langchain_core.messages.function.FunctionMessage, langchain_core.messages.tool.ToolMessage]]
#     },
#     metadata={
#         'lc_hub_owner': 'hwchase17',
#         'lc_hub_repo': 'openai-tools-agent',
#         'lc_hub_commit_hash': 'c18672812789a3b9697656dd539edf0120285dcae36396d0b548ae42a4ed66f5'
#     },
#     messages=[
#         SystemMessagePromptTemplate(
#             prompt=PromptTemplate(
#                 input_variables=[],
#                 template='You are a helpful assistant')
#             ),
#         MessagesPlaceholder(
#             variable_name='chat_history',
#             optional=True
#             ),
#         HumanMessagePromptTemplate(
#             prompt=PromptTemplate(
#                 input_variables=['input'],
#                 template='{input}'
#                 )
#             ),
#         MessagesPlaceholder(
#             variable_name='agent_scratchpad'
#             )
#     ]
# )

#!/usr/bin/env python3

import pprint

# from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent


# LangChainDeprecationWarning: The function `initialize_agent` was deprecated in LangChain 0.1.0 and will be
# removed in 0.2.0. Use Use new agent constructor methods like
# create_react_agent, create_json_agent, create_structured_chat_agent, etc. instead.


def create_prompt(user_input):
    prompt = PromptTemplate(
        input_variables=["theme"],
        # user_input=user_input,
        # agent_type=AgentType.CHAT,
        # agent_name="ChatOpenAI",
        # agent=ChatOpenAI,
        # tool=Tool.OPENAI,
        template="""
        あなたはニュース記事を書くブロガーです。
        下記のテーマについて、 google検索で最新情報を取得し、取得した情報に基づいてニュース記事を書いてください。
        1000文字以上で、日本語で出力してください。
        記事の末尾に参照元としてタイトルと URL を出力してください。
        ### テーマ : {theme}
        """,
    )
    return prompt.format(theme=user_input)


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
    pprint.pprint(response)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response["output"])
    print("出力が完了しました")


def main():
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=2000)

    tools = define_tools()

    # agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

    # theme = input("記事のテーマを入力してください: ")
    # prompt = create_prompt(theme)
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # response = agent.run(prompt)
    model = ChatOpenAI()

    agent = create_openai_tools_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    response = agent_executor.invoke({"input": "what is (4.5*2.1)^2.2?"})

    write_response_to_file(response, "output.txt")


if __name__ == "__main__":
    main()

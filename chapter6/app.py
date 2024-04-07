from langchain.agents import initialize_agent, Tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI


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
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response)
    print("出力が完了しました")


def main():
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=2000)

    tools = define_tools()

    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

    theme = input("記事のテーマを入力してください: ")
    prompt = create_prompt(theme)

    response = agent.run(prompt)

    write_response_to_file(response, "output.txt")


if __name__ == "__main__":
    main()

import os
import time

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

from prompts import MONTH_SUMMARY_PROMPT

dotenv.load_dotenv()

# 1 prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    template=MONTH_SUMMARY_PROMPT,
)

human_prompt = HumanMessagePromptTemplate.from_template(
    template="只生我的思考",
)

chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    human_prompt,
])

# 2 llm
# llm = ChatOpenAI(
#     model="openai/gpt-oss-20b:free",
#     api_key=os.getenv("OPEN_ROUTER_API_KEY"),
#     base_url=os.getenv("OPEN_ROUTER_URL"),
#     temperature=0
# )
llm = ChatOpenAI(
    model="qwen/qwen3-235b-a22b:free",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url=os.getenv("OPEN_ROUTER_URL"),
    temperature=0
)

# 3 chain
chain = chat_prompt | llm | StrOutputParser()

print(chain.invoke({}))

start_time = time.time()

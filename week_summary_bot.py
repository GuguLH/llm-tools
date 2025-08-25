import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from prompts import WEEK_SUMMARY_PROMPT

dotenv.load_dotenv()

# 1 prompt
prompt = PromptTemplate.from_template(
    template=WEEK_SUMMARY_PROMPT,
)

# 2 llm
llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url=os.getenv("OPEN_ROUTER_URL"),
    temperature=0
)

# 3 chain
chain = prompt | llm | StrOutputParser()

print(chain.invoke({}))

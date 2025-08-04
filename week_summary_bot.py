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
    model="deepseek-chat",
    api_key=os.getenv("DS_API_KEY"),
    base_url=os.getenv("DS_BASE"),
    temperature=0
)

# 3 chain
chain = prompt | llm | StrOutputParser()

print(chain.invoke({}))

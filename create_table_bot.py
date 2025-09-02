import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from prompts import CREATE_TABLE_PROMPT

dotenv.load_dotenv()

# 数据准备
table_fields = """
| 列名                  | 数据类型 | 约束       | 默认值 | 描述                                 |
| --------------------- | -------- | ---------- | ------ | ------------------------------------ |
| **chunk_id**          | BIGINT   | 主键，自增 | —      | 唯一主键 ID                          |
| **document_id**       | BIGINT   | NOT NULL   | —      | 外键，关联到 `documents` 表          |
| **chunk_text**        | TEXT     | NOT NULL   | —      | 分块的文本内容，用于送入 LLM         |
| **start_char_offset** | BIGINT   | NULL       | —      | 文本分块在原始文档中的起始字符偏移量 |
| **metadata**          | JSON     | NULL       | —      | 分块级别的元数据，如标题、章节等     |
"""

# 1 prompt
prompt = PromptTemplate.from_template(
    template=CREATE_TABLE_PROMPT,
)

# 2 llm
llm = ChatOpenAI(
    model="qwen/qwen3-235b-a22b:free",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url=os.getenv("OPEN_ROUTER_URL"),
    temperature=0
)

# llm = ChatOpenAI(
#     model="openai/gpt-oss-20b:free",
#     api_key=os.getenv("OPEN_ROUTER_API_KEY"),
#     base_url=os.getenv("OPEN_ROUTER_URL"),
#     temperature=0
# )

# 3 chain
chain = prompt | llm | StrOutputParser()

print(chain.invoke({
    "table_fields": table_fields,
}))

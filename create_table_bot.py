import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from prompts import CREATE_TABLE_PROMPT

dotenv.load_dotenv()

# 数据准备
general_fields = """
| 列名       | 数据类型     | 约束     | 默认值 | 描述                     |
| ---------- | ------------ | -------- | ------ | ------------------------ |
| udf01      | VARCHAR(100) | NULL     | —      | 自定义1                  |
| udf02      | VARCHAR(100) | NULL     | —      | 自定义2                  |
| udf03      | VARCHAR(100) | NULL     | —      | 自定义3                  |
| status     | TINYINT      | NOT NULL | 1      | 状态：`1` 启用，`0` 禁用 |
| created_by | BIGINT       | NOT NULL | —      | 创建人用户ID             |
| created_at | DATETIME     | NOT NULL | NOW()  | 创建时间                 |
| update_by  | BIGINT       | NOT NULL | —      | 更新人用户ID             |
| updated_at | DATETIME     | NOT NULL | NOW()  | 最后更新时间             |
"""

table_fields = """
| 列名            | 数据类型     | 约束        | 默认值 | 描述         |
| --------------- | ------------ | ----------- | ------ | ------------ |
| id              | BIGINT       | PRIMARY KEY | —      | 主键ID,自增  |
| conversation_id | varchar(50)  | NOT NULL    | —      | 会话 ID      |
| tool_id         | varchar(100) | NOT NULL    | —      | 工具ID       |
| tool_name       | varchar(100) | NOT NULL    | —      | 工具名称     |
| tool_args       | varchar(255) | NULL        | —      | 工具参数     |
| tool_resp       | varchar(255) | NULL        | —      | 工具调用结果 |
"""

# 1 prompt
prompt = PromptTemplate.from_template(
    template=CREATE_TABLE_PROMPT,
    partial_variables={
        "general_fields": general_fields,
    }
)

# 2 llm
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DS_API_KEY"),
    base_url=os.getenv("DS_BASE"),
    temperature=0
)
# llm = ChatOpenAI(
#     model="deepseek-ai/DeepSeek-V3",
#     api_key=os.getenv("SF_API_KEY"),
#     base_url=os.getenv("SF_BASE"),
#     temperature=0
# )

# 3 chain
chain = prompt | llm | StrOutputParser()

print(chain.invoke({
    "db_type": "MySQL",
    "table_fields": table_fields,
}))

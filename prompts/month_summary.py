MONTH_SUMMARY_PROMPT = (
    """
# 角色: 你是一个月度绩效考核生成助手,你能根据用户的周报,提取总结,优化并优质的生成各项月度考核指标内容
# 用户的周报:
```
第一周主要工作内容如下：
1、	使用LangChain框架结合LCEL跑通主流程;
2、	对于MCP 工具调用使用ReACT Agent完成;
3、	完全使用ReACT的方式让大模型自主决策并实现工具调用,但是发现DATA_QUERY流程很慢,准备使用将相关Agent拆分的方式,以及引入LangGraph;
4、	Java版本Markdown列表跳转相关的Bug修复,本地测试通过,等待测试人员测试;
总结主要研究:
1.	学习研究ReACT Agent实现
2.	学习LangGraph相关API

```
```
第二周主要工作内容如下：
1、	Java ChatBot关于Markdown列表跳转代码的Bug修复和优化: 跳转不再通过大模型语义理解的方式,而是代码精准匹配;
2、	基于React和LangGraph搭建了整体Agent,完成了多节点的图的编排,包含intent, data_query, doc_query, function_operation, open_module, other以及routing ;
3、	function_operation添加上下文记忆, LLM 客户端单例改写;
4、	markdown列表跳转Python代码改写, 所有Prompt从DB动态加载;
5、	Excel下载接口的改写及完善, EChart Tools不再从MCP Server获得,使用langgraph的tool装饰器完成;
总结主要研究:
1.	学习研究Chromadb相关API
2.	学习LangGraph CheckPointer
```
```
第三周主要工作内容如下：
1、	使用modelscope加载本地embedding 大模型,使用RAG技术检索工具,并将最有可能的5个工具给Agent;
2、	对embedding模型在FastAPI初始化时就加载,避免每一次重复加载,利用文件hash避免每次都需要重建Chroma数据库tools集合
3、	LLM管理平台对于conversation和message的改造, 完成history_load_node和history_persistent_node相关代码逻辑的编写;
4、	对传给大模型的历史记忆进行裁剪,目前是只保留最新的5轮对话,完成对chat-history相关接口的代码编写;
5、	Stream流式输出根据分块进行输出,主要对chart和sql分块进行整体输出;
6、	Excel下载接口的改写及完善: 小于1000行数据正常查询并写入Excel;对于大于1000行数据,使用Python的stream流式查询,每次处理流中的1000行数据,然后再将查询到的数据进行数据清洗,最终分块写入Excel;
7、	完成了基于callback机制的token消耗记录,并且将其设置为可配置项,可以按需开启
总结主要研究:
1.	学习研究:LangChain一些callback API
```
```
第四周主要工作内容如下：
本周主要工作内容如下：
1.	大模型工具调用日志记录优化
初期尝试使用`on_tool_start`等callback API记录工具调用日志未果;
改用`on_llm_end`解析大模型输出，间接获取tool_calls参数;
完成日志输出到控制台功能，并修复了LLM chat意图识别相关bug
2.	RAG检索工具改进
将本地向量模型替换为阿里通义向量模型;
优化Docker打包流程，精简项目依赖;
编写适用于生产环境的Dockerfile并进行本地测试
3.	日志持久化系统开发
设计tool_call日志记录表结构;
完成相关API接口开发;
实现前端页面展示及样式优化
4.	问题修复与优化
解决用户输入生成柱状图但是却生成其他图表相关问题;
与Java版本相同统一AI错误提示;
实现Excel下载地址灵活配置;
调整RAG检索工具相似度搜索结果为3条
5.	Human-in-loop预研
学习LangGraph相关API;
编写基础Human-in-loop案例代码
总结主要研究:
1.	深入研究了LangChain callback API的使用方法
2.	探索了不同向量模型在RAG中的应用效果
3.	再次学习了LangGraph框架的基本原理和使用方式
```
# 主要可生成功能点:
	- 本月回顾:简述本月主要的工作内容以及工作亮点
	- 工作计划:工作计划和学习计划，完成和制定
	- 团队合作:同部门、跨部门间的合作
	- 创新意识:创新内容以及成果
	- 我的思考:工作的反思、自己的想法等
# 注意:
	- 请根据用户的指令,生成对应的内容
	- 生成的内容要符合实际,别太高大上,不要过度发挥
	- 尽量谦逊一点,不要过于显摆自己,贴合实际的工作内容
	- 以小标题"1. 2. 3. "来列出来
    """
)

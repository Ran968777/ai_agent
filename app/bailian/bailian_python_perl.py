from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools.python.tool import PythonREPLTool

from app.bailian.common import llm

# python_repl = PythonREPL()
# res = python_repl.run("print('hello world')")
# print(res)

tools = [PythonREPLTool()]
tool_names = ["PythonREPLTool"]
#
agent = initialize_agent(
    tools= tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

prompt_template = PromptTemplate.from_template(template="""
尽你所能回答以下问题或执行用户命令,你可以使用以下工具[{tool_names}]
--
请按照以下格式进行思考：
- Question: 你必须回答输入的问题
- Thought: 你考虑应该怎么做
- Action: 要采取的行动，应该是[{tool_names}]中的一个
- Action Input: 行动的输入
- Observation: 行动的结果
...(以上Thought、Action、Action Input、Observation可以重复多次)

Final Answer:
对原始输入问题的最终答案

-- 
注意：
- PythonREPLTool工具的输入是python代码，不允许```py 等标记

-- 
Question: {input}

""")

prompt = prompt_template.format_prompt(
    tool_names=",".join(tool_names),
    input="""
    1.向 /Users/ranjiansong/Desktop/skai/py_project/ai_agent/.temp/ 写一个index.html
    2.index.html的大致内容是一个企业的官网
    
    """
)

print(prompt)

agent.invoke( prompt)
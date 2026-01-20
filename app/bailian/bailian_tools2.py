from app.bailian.common import llm, chat_prompt_template
from langchain_core.tools import Tool,tool
from pydantic import BaseModel, Field


class AddSchema(BaseModel):
    a: int = Field(description="The first integer to add")
    b: int = Field(description="The second integer to add")


@tool(
    description="""Add two integers. Use this tool to calculate the sum of two numbers. Inputs should be 'a' and 'b'.""",
    args_schema=AddSchema,
    return_direct=True
)
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

#
def create_calc_tools():
    return [add]

# 将模型和tool绑定
llm_with_tools= llm.bind_tools([add])

chain = chat_prompt_template | llm_with_tools

resp = chain.invoke(input={"role": "计算", "domain": "数学计算", "question": "100+200=?"})

print(resp)

tools_dict = {
    "add": add
}
# 调用工具

for tool_calls in resp.tool_calls:
    print(tool_calls)

    args = tool_calls["args"]
    print(args)

    func_name = tool_calls["name"]
    print(func_name)

    tool_func = tools_dict[func_name]

    tool_result = tool_func.invoke(args)
    print(tool_result)
#
# 以上是传统的方式比较，简单
# Traceback (most recent call last):
#   File "/Users/ranjiansong/Desktop/Doc/python/ai-agent/app/bailian/bailian_tools.py", line 42, in <module>
#     tool_result = tool_func(args["__arg1"])
# TypeError: add() missing 1 required positional argument: 'b'
# content='这个问题涉及简单的加法运算。我可以使用加法工具来计算100+200的结果。' additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_67186d25005946c2b306714d', 'function': {'arguments': '{"__arg1": "100+200"}', 'name': 'add'}, 'type': 'function'}]} response_metadata={'finish_reason': 'tool_calls', 'model_name': 'deepseek-v3.2'} id='run--019bdbd7-1725-7593-a8ac-efa168bd2107-0' tool_calls=[{'name': 'add', 'args': {'__arg1': '100+200'}, 'id': 'call_67186d25005946c2b306714d', 'type': 'tool_call'}]
# {'name': 'add', 'args': {'__arg1': '100+200'}, 'id': 'call_67186d25005946c2b306714d', 'type': 'tool_call'}
# {'__arg1': '100+200'}
# add

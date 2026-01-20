from app.bailian.common import llm, chat_prompt_template
from langchain_core.tools import Tool


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


# 把上面的func转为langchain可以理解的tool
add_tools = Tool.from_function(
    func=add,
    name="add",
    description="Add two integers. Use this tool to calculate the sum of two numbers. Inputs should be 'a' and 'b'."
)

# 将模型和tool绑定
llm_with_tools= llm.bind_tools([add_tools])

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

    tool_result = tool_func(args["__arg1"])
    print(tool_result)


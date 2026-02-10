import asyncio

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.code_agent.model.model import llm_qwen
from app.code_agent.tools.file_saver import FileSaver
from app.code_agent.tools.file_tools import file_toos
from app.code_agent.tools.shell_tools import get_stdio_shell_tools


def format_debug_output(name: str, content:str) -> None:
    print(f"🤔 【{name}】")
    print("----\n", content, "\n----")


async def run_agent():
    memory = MemorySaver()
    shell_tools = await get_stdio_shell_tools()
    tools = file_toos + shell_tools

    agent = create_react_agent(
        model=llm_qwen,
        tools=tools,
        checkpointer=memory,
        debug=False,
    )
    config = RunnableConfig(configurable={
        "thread_id": 3,
    })

    while True:
        user_inpt = input("用户：")
        if user_inpt.lower() == "exit" or user_inpt.lower() == "quit":
            print("bye！")
            break

        print("\n🤖 正在思考和处理...")
        print("=" * 60)

        iteration_count = 0
        async for chuck in agent.astream(input={"messages": user_inpt}, config=config):
            iteration_count += 1

            print(f"\n迭代次数: {iteration_count}")
            print("-" * 30)
            items = chuck.items()
            for key, value in items:
                print(f"{key}: {value}")
                if "messages" in value:
                    for msg in value["messages"]:
                        if isinstance(msg, AIMessage):
                            if msg.content:
                                format_debug_output("AI思考",msg.content)
                            else:
                                for tool in msg.tool_calls:
                                    format_debug_output("工具调用",f"{tool['name']} :{tool['args']}")

                        elif isinstance(msg,ToolMessage):
                            tool_name = getattr(msg, "name", "unknown")
                            content = msg.content
                            tool_result = f"""
🔧 工具：{tool_name}
                            
执行结果：
{content}
✅ 状态： 执行完成
                            """
                            format_debug_output(tool_name,tool_result)




        # resp = await agent.ainvoke(input={"messages": user_inpt}, config=config)
        # print("助理：", resp['messages'][-1].content)
        # print()


asyncio.run(run_agent())

import asyncio

from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

from app.bailian.common import llm


async def create_client():
    server_params = StdioServerParameters(command="python", args=[
        "/Users/ranjiansong/Desktop/skai/py_project/ai_agent/app/mcp/stdio/mcp_stdio_server.py"], )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await  session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
            )

            resp = await agent.ainvoke("请计算1+1* 5=？")
            return resp


asyncio.run(create_client())



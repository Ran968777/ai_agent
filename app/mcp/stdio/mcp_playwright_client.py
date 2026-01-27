import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langgraph.prebuilt import create_react_agent

from app.bailian.common import llm


#
# {
#   "mcpServers": {
#     "playwright": {
#       "command": "npx",
#       "args": ["-y", "@executeautomation/playwright-mcp-server"]
#     }
#   }
# }
async def mcp_client():
    # server_parameters = StdioServerParameters(
    #     command="npx", args=["-y", "@executeautomation/playwright-mcp-server"]
    # 本地安装后启动
    server_parameters = StdioServerParameters(
        command="node", args=[
            "/Users/ranjiansong/.nvm/versions/node/v20.19.4/lib/node_modules/@executeautomation/playwright-mcp-server/dist/index.js"]
    )

    async with stdio_client(server_parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("获取到的工具\n", tools)

            agent = create_react_agent(model=llm, tools=tools, debug=True)
            resp = await agent.ainvoke(input={"messages": [
                ("system",
                 "You are a helpful assistant. When using tools, ensure that the arguments are clean strings. Do NOT wrap URLs or other string arguments in Markdown backticks or extra spaces. For example, use 'https://www.baidu.com' instead of ' `https://www.baidu.com` '."),
                ("user", "在百度中查询今天北京的天气")
            ]})
            print(resp)


asyncio.run(mcp_client())

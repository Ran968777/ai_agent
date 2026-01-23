import asyncio
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import ChatMessagePromptTemplate, PromptTemplate

from app.bailian.common import llm

# Load environment variables from .env file
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient


async def create_mcp_client():
    amap_key = os.environ.get("AMAP_KEY")

    mcp_config = {
        "amap": {
            "url": f"https://mcp.amap.com/sse?key={amap_key}",
            "transport": "sse",
        }
    }
    mcp_client = MultiServerMCPClient(mcp_config)
    # print(mcp_client)

    tools = await mcp_client.get_tools()
    # print(tools)
    return mcp_client, tools


async def create_and_run_agent():
    client, tools = await create_mcp_client()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate.from_template(
        "你是一个智能助手，可以调用高德 MCP 工具。\n\n问题: {input}"
    )

   #  prompt = prompt_template.format(input="""
   # 提供杭州东站的坐标
   #  """)

    prompt = prompt_template.format(input="""
    - 我五月底端午节计划去杭州游玩4天。
    - 帮制作旅行攻略，考虑出行时间和路线，以及天气状况路线规划。
    - 制作网页地图自定义绘制旅游路线和位置。
        - 网页使用简约美观页面风格，景区图片以卡片展示。
    - 行程规划结果在高德地图app展示，并集成到h5页面中。
    - 同一天行程景区之间我想打车前往。
    """)

    print("prompt\n", prompt)
    resp = await agent.ainvoke(prompt)
    print("output\n", resp)
    return resp


asyncio.run(create_and_run_agent())

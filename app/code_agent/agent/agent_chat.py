from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.checkpoint.redis import RedisSaver
from langgraph.prebuilt import create_react_agent

from app.code_agent.model.model import llm_qwen
from app.code_agent.tools.file_tools import file_toos


def create_agent():
    # 由于本地 Redis 不支持 RediSearch (FT._LIST 命令)，暂时切换回 MemorySaver
    # 如果需要持久化，请使用 Redis Stack (docker run -p 6379:6379 redis/redis-stack:latest)
    memory = MemorySaver()

    #  使用redis server (需要 Redis Stack)
    # with RedisSaver.from_conn_string("redis://localhost:6379") as memory:
    #     memory.setup()

    # 使用mongoDb (需要 MongoDB), 注意需要手动close
    # with MongoDBSaver.from_conn_string("mongodb://localhost:27017","db_name") as memory:


    agent = create_react_agent(
        model=llm_qwen,
        tools=file_toos,
        checkpointer=memory,
        debug=True,

    )

    return agent


def run_agent():
    config = RunnableConfig(configurable={
        "thread_id": 1,
    })

    agent = create_agent()

    resp = agent.invoke(input={"messages": [("user", "我是Sam")]}, config=config)

    print(resp)
    print("=" * 60)

    resp = agent.invoke(input={"messages": [("user", "我是谁？")]}, config=config)
    print(resp)

if __name__ == '__main__':
    run_agent()
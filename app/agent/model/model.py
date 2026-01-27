from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm_qwen = ChatOpenAI(
    model="qwen-max",
    # model="qwen3-235b-a22b",
    api_key=SecretStr("sk-c22000b794334c718c11e41241589914"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm = ChatOpenAI(
    model="deepseek-v3.2",
    api_key=SecretStr("sk-5a06abe7121c485a9f4f6a8e5748ae2f"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

system_message = ChatMessagePromptTemplate.from_template(template="你是一位{role}专家，擅长回答{domain}领域问题",role="system")
human_message = ChatMessagePromptTemplate.from_template(template="用户问题：{question}", role="user")

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message,
    human_message
])
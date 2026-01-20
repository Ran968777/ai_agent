from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate,ChatMessagePromptTemplate

llm = ChatOpenAI(
    model="qwq-plus",
    api_key=SecretStr("sk-5a06abe7121c485a9f4f6a8e5748ae2f"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

# resp = llm.invoke("100+100=?")
# print(resp.content)

# resp = llm.stream("100+100=?")
# for chunk in resp:
#     print(chunk.content, end="")

# 创建提示词模板
# prompt_template = PromptTemplate.from_template("今天{something}真不错")
# print(prompt_template)
#
# # 模板转为提示词
# prompt = prompt_template.format(something="天气")
# print(prompt)

system_message = ChatMessagePromptTemplate.from_template(template="你是一位{role}专家，擅长回答{domain}领域问题",role="system")
user_message = ChatMessagePromptTemplate.from_template(template="用户问题：{question}",role="user")

chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message, user_message])

prompt = chat_prompt_template.format_messages(role="数学", domain="数学", question="你是谁，你擅长的领域是什么")

print('prompt :',prompt)
resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content, end="")

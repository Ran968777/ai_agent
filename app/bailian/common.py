from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr, BaseModel, Field

llm = ChatOpenAI(
    model="deepseek-v3.2",
    api_key=SecretStr("sk-5a06abe7121c485a9f4f6a8e5748ae2f"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

system_message = ChatMessagePromptTemplate.from_template(template="你是一位{role}专家，擅长回答{domain}领域问题",
                                                         role="system")
human_message = ChatMessagePromptTemplate.from_template(template="用户问题：{question}", role="user")

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message,
    human_message
])


class AddSchema(BaseModel):
    a: int = Field(description="The first integer to add")
    b: int = Field(description="The second integer to add")


@tool(
    description="""Add two integers. Use this tool to calculate the sum of two numbers. Inputs should be 'a' and 'b'.""",
    args_schema=AddSchema,
    return_direct=False,
)
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


#
def create_calc_tools():
    return [add]


calc_tools = create_calc_tools()

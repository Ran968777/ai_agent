from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field

from app.bailian.common import create_calc_tools, llm, chat_prompt_template


class Output(BaseModel):
    args: str = Field(description="用户问题中涉及的计算参数，例如 '100, 200'")
    result: str = Field(description="经过计算后的最终数值结果")


parser = JsonOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()
print(format_instructions)

agent = initialize_agent(
    tools=create_calc_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

prompt = chat_prompt_template.format_messages(
    role="计算",
    domain="数学",
    question=f"""
        请阅读下面的问题。如果需要，请使用工具进行计算。
        
        当你得出最终答案时，请以严格的 JSON 格式输出最终结果。
        注意：在调用工具时不要使用此格式，仅在最终回答（Final Answer）时使用。
        
        最终回答的 JSON 格式要求：
        {format_instructions}
        
        问题：
        100+200=？
            """
)

resp = agent.invoke(prompt)
print(resp)
print("output is \n",resp["output"])

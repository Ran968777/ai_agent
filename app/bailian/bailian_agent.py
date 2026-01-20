
from langchain.agents import initialize_agent, AgentType

from app.bailian.common import create_calc_tools, llm

agent = initialize_agent(
    tools=create_calc_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

resp = agent.invoke("100+200=?")
print(resp)

import uuid

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_message_histories import ChatMessageHistory, FileChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig

from app.agent.model.model import llm_qwen
from app.agent.prompts.multi_chat_prompts import multi_chat_prompt

store = {}
# 获取会话历史
# 存在内存中
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        print(store)
    return store[session_id]

def get_file_session_history(session_id: str):
    return FileChatMessageHistory(f"{session_id}.json")

chain = multi_chat_prompt | llm_qwen | StrOutputParser()



chat_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_file_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# chat_session_id = uuid.uuid4()
chat_session_id = "e02381ad-7d2c-4374-9db9-cc60d7b39ec4"
while True:
    user_inpt = input("用户：")
    if user_inpt.lower() == "exit" or user_inpt.lower() == "quit":
        print("bye！")
        break

    print("助理：",end="")
    # resp = chat_with_history.invoke({"question": user_inpt, }, config=RunnableConfig(
    #     configurable={"session_id": chat_session_id})
    #     )
    #
    # for chunk in resp:
    #     print(chunk, end="")

    # stream 输出
    for chunk in chat_with_history.stream({"question": user_inpt, }, config=RunnableConfig(
            configurable={"session_id": chat_session_id})
            ):
        print(chunk, end="")

    print("\n")

#
# for chuck in chain.stream({"question": "我的名字是什么", "chat_history": []}):
#     print(chuck, end="")

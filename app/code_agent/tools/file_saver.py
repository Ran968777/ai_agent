import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Self

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, Checkpoint, CheckpointMetadata, \
    ChannelVersions
import os

from langgraph.prebuilt import create_react_agent

from app.code_agent.model.model import llm_qwen
from app.code_agent.tools.file_tools import file_toos


class FileSaver(BaseCheckpointSaver[str]):
    def __init__(self, base_path: str = "/Users/ranjiansong/Desktop/Doc/python/ai-agent/.temp/checkpoint") -> None:
        super().__init__()
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

    def _get_checkpoint_path(self, thread_id: str, checkpoint_id: str):
        dir_path = os.path.join(self.base_path, thread_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, checkpoint_id + ".json")
        return file_path

    def _serialize_data(self, data) -> str:
        import pickle, base64
        pickled = pickle.dumps(data)
        return base64.b64encode(pickled).decode("utf-8")

    def _deserialize_data(self, data: str) -> Any:
        import pickle, base64
        decoded = base64.b64decode(data)
        return pickle.loads(decoded)

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        # 找到正确的checkpoint文件路径
        thread_id = config["configurable"]["thread_id"]
        # # checkpoint_id = config["configurable"].get("checkpoint_id")
        #
        # 读取文件内容
        dir_path = os.path.join(self.base_path, thread_id)
        checkpoint_files = list(Path(dir_path).glob("*.json"))
        checkpoint_files.sort(key=lambda x: x.stem, reverse=True)
        if len(checkpoint_files) == 0:
            return None

        latest_checkpoint = checkpoint_files[0]
        checkpoint_id = latest_checkpoint.stem
        checkpoint_path = self._get_checkpoint_path(thread_id, checkpoint_id)

        # 解析文件内容，反序列化
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        checkpoint = self._deserialize_data(data["checkpoint"])
        metadata = self._deserialize_data(data["metadata"])
        # 返回checkpoint对象

        return CheckpointTuple(
            config={
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id,
                }
            },
            checkpoint=checkpoint,
            metadata=metadata,
        )

    def put(
            self,
            config: RunnableConfig,
            checkpoint: Checkpoint,
            metadata: CheckpointMetadata,
            new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id = str(config["configurable"]["thread_id"])
        checkpoint_id = checkpoint["id"]
        checkpoint_path = self._get_checkpoint_path(thread_id, checkpoint_id)

        checkpoint_data = {
            "checkpoint": self._serialize_data(checkpoint),
            "metadata": self._serialize_data(metadata),
        }

        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint_id,
            }
        }

    def put_writes(
            self,
            config: RunnableConfig,
            writes: Sequence[tuple[str, Any]],
            task_id: str,
            task_path: str = "",
    ) -> None:
        pass


if __name__ == "__main__":
    memory = FileSaver()
    agent = create_react_agent(
        model=llm_qwen,
        tools=file_toos,
        checkpointer=memory,
        # debug=True,
    )
    config = RunnableConfig(configurable={
        "thread_id": 2,
    })

    while True:
        user_inpt = input("用户：")
        if user_inpt.lower() == "exit" or user_inpt.lower() == "quit":
            print("bye！")
            break
        resp = agent.invoke(input={"messages": user_inpt}, config=config)
        print("助理：",resp['messages'][-1].content)
        print()

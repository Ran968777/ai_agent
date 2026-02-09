import json
from collections.abc import Sequence
from typing import Any, Self

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, Checkpoint, CheckpointMetadata, \
    ChannelVersions
import os

from langgraph.prebuilt import create_react_agent

from app.code_agent.model.model import llm_qwen
from app.code_agent.tools.file_tools import file_toos


class FileSaver(BaseCheckpointSaver[str]):
    def __init__(self, base_path: str = "/Users/ranjiansong/Desktop/skai/py_project/ai_agent/.temp/checkpoint") -> None:
        super().__init__()
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        pass

    def _get_checkpoint_path(self, thread_id: str, checkpoint_id: str):
        dir_path = os.path.join(self.base_path, thread_id, checkpoint_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, checkpoint_id + ".json")
        return file_path

    def _serialize_data(self, data) -> str:
        import pickle, base64
        pickled = pickle.dumps(data)
        return base64.b64encode(pickled).decode("utf-8")

    def put(
            self,
            config: RunnableConfig,
            checkpoint: Checkpoint,
            metadata: CheckpointMetadata,
            new_versions: ChannelVersions,
    ) -> RunnableConfig:
        # 生成存储的文件路径
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]
        checkpoint_path = self._get_checkpoint_path(thread_id, checkpoint_id)

        # 将checkpoint 序列化为json
        checkpoint_data = {
            "checkpoint": self._serialize_data(checkpoint),
            "metadata": self._serialize_data(metadata),
        }

        # 存储到文件
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
            # f.write(self._serialize_data(checkpoint_data))

        # 生成返回值
        return {
            "configurable":{
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
        debug=True,
    )
    config = RunnableConfig(configurable={
        "thread_id": 1,
    })
    resp = agent.invoke(input={"messages": [("user", "我是Sam")]}, config=config)
    print(resp)

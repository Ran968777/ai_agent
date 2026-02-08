import os
from collections.abc import Sequence
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, Checkpoint, CheckpointMetadata, \
    ChannelVersions
from langgraph.prebuilt import create_react_agent

from app.code_agent.model.model import llm_qwen
from app.code_agent.tools.file_tools import file_toos


class FileSaver(BaseCheckpointSaver[str]):
    def __init__(self, base_path: str = "/Users/ranjiansong/Desktop/Doc/python/ai-agent/.temp/checkpoint"):
        super().__init__()
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        """Fetch a checkpoint tuple using the given configuration.

        Args:
            config: Configuration specifying which checkpoint to retrieve.

        Returns:
            The requested checkpoint tuple, or `None` if not found.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        print("get_tuple")

    pass

    def put(
            self,
            config: RunnableConfig,
            checkpoint: Checkpoint,
            metadata: CheckpointMetadata,
            new_versions: ChannelVersions,
    ) -> RunnableConfig:
        print("put")
        pass


    def put_writes(
            self,
            config: RunnableConfig,
            writes: Sequence[tuple[str, Any]],
            task_id: str,
            task_path: str = "",
    ) -> None:
        print("put_writes")
        pass


if __name__ == '__main__':
    memory = FileSaver()
    agent = create_react_agent(
        model=llm_qwen,
        tools=file_toos,
        checkpointer=memory,
        debug=True,
    )

    config = RunnableConfig(configurable={"thread_id": 1})
    resp = agent.invoke(input={"messages": "我是sam，你是谁？"}, config=config)
    print(resp)


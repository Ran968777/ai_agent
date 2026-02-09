from collections.abc import Sequence
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, Checkpoint, CheckpointMetadata, \
    ChannelVersions
import os


class FileSaver(BaseCheckpointSaver[str]):
    def __init__(self, base_path: str = "/Users/ranjiansong/Desktop/skai/py_project/ai_agent/.temp/checkpoint") -> None:
        super().__init__()
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        pass

    def put(
            self,
            config: RunnableConfig,
            checkpoint: Checkpoint,
            metadata: CheckpointMetadata,
            new_versions: ChannelVersions,
    ) -> RunnableConfig:
        pass

    def put_writes(
            self,
            config: RunnableConfig,
            writes: Sequence[tuple[str, Any]],
            task_id: str,
            task_path: str = "",
    ) -> None:
        pass

if __name__ == "__main__":
    saver = FileSaver()

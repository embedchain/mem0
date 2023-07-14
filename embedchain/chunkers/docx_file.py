from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter

from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.AddConfig import ChunkerConfig


class DocxFileChunker(BaseChunker):
    """Chunker for .docx file."""

    def __init__(self, config: Optional[ChunkerConfig] = None):
        if config is None:
            config = ChunkerConfig(
                chunk_size=1000, chunk_overlap=0, length_function=len
            )
        text_splitter = RecursiveCharacterTextSplitter(config.as_dict())
        super().__init__(text_splitter)

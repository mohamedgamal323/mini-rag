from domain.models.asset import Asset
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

class FileAssetHandler:

    def process(self, asset: Asset, chunk_size: int = 500, overlap: int = 50):
        """
        Splits the file content into chunks using RecursiveCharacterTextSplitter.
        Returns a list of chunk dicts.
        """
        if not asset.content:
            return []

        content_str = asset.content.decode("utf-8", errors="ignore")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )
        chunks = splitter.split_text(content_str)
        return [
            {
                "chunk_id": uuid.uuid4().hex,  # Generate a unique chunk_id
                "project_id": asset.project_id,
                "asset_id": asset.asset_id,
                "content": chunk,
                "chunk_order": idx,
                "metadata": asset.metadata or {},
            }
            for idx, chunk in enumerate(chunks)
        ]
import os


class MetadataExtractor:
    """
    Extracts and standardizes metadata for code chunks.
    """

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".go": "go",
        ".rs": "rust",
    }

    def extract(self, chunk: dict) -> dict:
        """
        Extract metadata from one code chunk.

        Args:
            chunk: A dictionary returned by CodeChunker.

        Returns:
            A standardized metadata dictionary.
        """

        if not isinstance(chunk, dict):
            raise TypeError("chunk must be a dictionary")

        required_fields = (
            "file_path",
            "chunk_type",
            "name",
            "start_line",
            "end_line",
        )

        missing_fields = [field for field in required_fields if field not in chunk]

        if missing_fields:
            raise ValueError(f"Missing required chunk fields: {missing_fields}")

        file_path = chunk["file_path"]

        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string")

        extension = os.path.splitext(file_path)[1].lower()

        metadata = {
            "file_path": file_path,
            "language": self.LANGUAGE_MAP.get(extension, "unknown"),
            "chunk_type": chunk["chunk_type"],
            "name": chunk["name"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
        }

        # Include class_name only when it has a meaningful value.
        class_name = chunk.get("class_name")

        if class_name:
            metadata["class_name"] = class_name

        return metadata

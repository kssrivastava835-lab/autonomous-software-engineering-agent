from pathlib import Path

from ingestion.code_chunker import CodeChunker
from ingestion.code_parser import CodeParser
from ingestion.file_filter import FileFilter
from ingestion.metadata_extractor import MetadataExtractor
from ingestion.repository_scanner import RepositoryScanner


class IngestionPipeline:
    """
    Connects repository scanning, filtering, parsing,
    chunking, and metadata extraction into one pipeline.
    """

    def __init__(self):
        self.scanner = RepositoryScanner()
        self.file_filter = FileFilter()
        self.parser = CodeParser()
        self.chunker = CodeChunker()
        self.metadata_extractor = MetadataExtractor()

    def ingest(self, repo_path):
        repo_path = Path(repo_path).resolve()

        if not repo_path.is_dir():
            raise NotADirectoryError(f"Repository directory not found: {repo_path}")

        # Step 1: Discover repository files.
        all_files = self.scanner.scan(str(repo_path))

        # Step 2: Filter supported source files.
        supported_files = self.file_filter.filter_files(all_files)

        chunks = []
        errors = []
        files_processed = 0
        files_skipped = 0

        for scanned_path in supported_files:
            try:
                path = Path(scanned_path)

                # Normalize the path to be relative to the repository.
                if path.is_absolute():
                    path = path.resolve().relative_to(repo_path)

                relative_path = path.as_posix()
                full_path = repo_path / path

                # CodeParser currently uses Python AST.
                if full_path.suffix.lower() != ".py":
                    files_skipped += 1
                    continue

                if not full_path.is_file():
                    raise FileNotFoundError(f"Source file not found: {full_path}")

                # Step 3: Parse Python source code.
                parsed_data = self.parser.parse_file(str(full_path))

                # Step 4: Create code chunks.
                file_chunks = self.chunker.chunk_files(
                    str(full_path),
                    parsed_data,
                )

                if file_chunks is None:
                    raise ValueError("CodeChunker returned None instead of a list.")

                # Step 5: Extract metadata and store chunks.
                for chunk in file_chunks:
                    if not isinstance(chunk, dict):
                        raise TypeError("CodeChunker must return dictionaries.")

                    source_code = chunk.get("source_code")

                    if not isinstance(source_code, str):
                        raise ValueError(
                            "Chunk must contain a valid source_code string."
                        )

                    # Store repository-relative paths in metadata.
                    chunk["file_path"] = relative_path

                    metadata = self.metadata_extractor.extract(chunk)

                    chunks.append(
                        {
                            "source_code": source_code,
                            "metadata": metadata,
                        }
                    )

                files_processed += 1

            except Exception as error:
                errors.append(
                    {
                        "file_path": str(scanned_path),
                        "error": str(error),
                    }
                )

        # Step 6: Return the ingestion report.
        return {
            "repository_path": str(repo_path),
            "files_scanned": len(all_files),
            "supported_files": len(supported_files),
            "files_processed": files_processed,
            "files_skipped": files_skipped,
            "total_chunks": len(chunks),
            "chunks": chunks,
            "errors": errors,
        }

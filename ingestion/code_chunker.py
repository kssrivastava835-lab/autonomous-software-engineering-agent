from pathlib import Path


class CodeChunker:
    """
    Splits Python source code into chunks using parsed
    function and class line information.
    """

    def chunk_files(self, file_path, parsed_data):
        source_path = Path(file_path)

        with source_path.open("r", encoding="utf-8") as file:
            source_code = file.read()

        source_lines = source_code.splitlines()
        chunks = []

        # Create chunks for standalone functions.
        for function in parsed_data.get("functions", []):
            chunks.append(
                self._create_chunk(
                    source_lines=source_lines,
                    file_path=file_path,
                    chunk_type="function",
                    name=function["name"],
                    start_line=function["start_line"],
                    end_line=function["end_line"],
                )
            )

        # Create a chunk for each class and its methods.
        for class_info in parsed_data.get("classes", []):
            chunks.append(
                self._create_chunk(
                    source_lines=source_lines,
                    file_path=file_path,
                    chunk_type="class",
                    name=class_info["name"],
                    start_line=class_info["start_line"],
                    end_line=class_info["end_line"],
                )
            )

            for method in class_info.get("methods", []):
                chunks.append(
                    self._create_chunk(
                        source_lines=source_lines,
                        file_path=file_path,
                        chunk_type="method",
                        name=method["name"],
                        class_name=class_info["name"],
                        start_line=method["start_line"],
                        end_line=method["end_line"],
                    )
                )

        return chunks

    def _create_chunk(
        self,
        source_lines,
        file_path,
        chunk_type,
        name,
        start_line,
        end_line,
        class_name=None,
    ):
        # Validate 1-based, inclusive line numbers.
        if start_line < 1 or end_line < start_line:
            raise ValueError(f"Invalid line range: {start_line}-{end_line}")

        if end_line > len(source_lines):
            raise ValueError(
                f"End line {end_line} exceeds file length ({len(source_lines)} lines)"
            )

        source_code = "\n".join(source_lines[start_line - 1 : end_line])

        chunk = {
            "source_code": source_code,
            "file_path": str(file_path),
            "chunk_type": chunk_type,
            "name": name,
            "start_line": start_line,
            "end_line": end_line,
        }

        if class_name is not None:
            chunk["class_name"] = class_name

        return chunk

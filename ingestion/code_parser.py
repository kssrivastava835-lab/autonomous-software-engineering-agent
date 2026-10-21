import ast
from pathlib import Path


class CodeParser:
    def parse_file(self, file_path):

        file_path = Path(file_path)

        try:
            source_code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source_code, filename=str(file_path))

        except (OSError, SyntaxError, UnicodeDecodeError) as e:
            raise ValueError(f"Unable to parse file '{file_path}': {e}") from e

        imports = []
        functions = []
        classes = []

        def get_function_info(node):
            return {
                "name": node.name,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", None),
                "docstring": ast.get_docstring(node),
            }

        for node in ast.walk(tree):
            # Handle: import os
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"name": alias.name, "line": node.lineno})

            # Handle: from os import path
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imports.append(
                        {
                            "name": (
                                f"{module}.{alias.name}" if module else alias.name
                            ),
                            "line": node.lineno,
                        }
                    )

            # Handle regular and async functions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Avoid listing class methods twice in functions.
                if not isinstance(getattr(node, "parent", None), ast.ClassDef):
                    functions.append(get_function_info(node))

            # Handle classes and their methods
            elif isinstance(node, ast.ClassDef):
                methods = []

                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(get_function_info(child))

                classes.append(
                    {
                        "name": node.name,
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", None),
                        "docstring": ast.get_docstring(node),
                        "methods": methods,
                    }
                )

        return {
            "file": str(file_path),
            "imports": imports,
            "functions": functions,
            "classes": classes,
        }

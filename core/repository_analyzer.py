import os


class RepositoryAnalyzer:

    SOURCE_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".c",
        ".go",
        ".rs"
    }

    TEST_KEYWORDS = {
        "test",
        "tests"
    }

    def analyze(self, repo_path):

        files = []
        source_files = []
        test_files = []
        languages = {}
        directories = []

        for root, dirs, filenames in os.walk(repo_path):

            dirs[:] = [
                d for d in dirs
                if d not in {
                    ".git",
                    "venv",
                    "__pycache__",
                    "node_modules"
                }
            ]

            for directory in dirs:

                relative_directory = os.path.relpath(
                    os.path.join(root, directory),
                    repo_path
                )

                directories.append(relative_directory)

            for filename in filenames:

                full_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    full_path,
                    repo_path
                )

                files.append(relative_path)

                extension = os.path.splitext(
                    filename
                )[1].lower()

                if extension in self.SOURCE_EXTENSIONS:

                    source_files.append(relative_path)

                    language = extension[1:]

                    languages[language] = languages.get(
                        language, 0
                    ) + 1

                if (
                    "test" in filename.lower()
                    or any(
                        keyword in relative_path.lower().split(os.sep)
                        for keyword in self.TEST_KEYWORDS
                    )
                ):

                    test_files.append(relative_path)

        return {
            "total_files": len(files),
            "source_files": source_files,
            "test_files": test_files,
            "files": files,
            "languages": languages,
            "directories": directories
        }
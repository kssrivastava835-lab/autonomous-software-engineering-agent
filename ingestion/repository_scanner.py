import os


class RepositoryScanner:

    IGNORE_DIRECTORIES = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "venv",
        "env",
        ".venv",
        "node_modules"
    }

    def scan(self, repo_path):

        files = []

        for root, dirs, filenames in os.walk(repo_path):

            dirs[:] = [
                directory
                for directory in dirs
                if directory not in self.IGNORE_DIRECTORIES
            ]

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

        return files
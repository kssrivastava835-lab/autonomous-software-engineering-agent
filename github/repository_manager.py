import os
from git import Repo
from dotenv import load_dotenv


load_dotenv()


class RepositoryManager:

    def __init__(self, workspace="workspace"):
        self.workspace = workspace

    def clone_repository(self, repo_url, repo_name):

        repo_path = os.path.join(
            self.workspace,
            repo_name
        )

        os.makedirs(self.workspace, exist_ok=True)

        if os.path.exists(repo_path):

            print("Repository already exists.")

            return repo_path

        print(f"Cloning repository: {repo_url}")

        Repo.clone_from(
            repo_url,
            repo_path
        )

        print("Repository cloned successfully.")

        return repo_path
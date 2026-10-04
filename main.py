from github.repository_manager import RepositoryManager
from core.repository_analyzer import RepositoryAnalyzer

def main():
    repo_url = input("Enter Github repositary URL:")
    repo_name = input("Enter repositary name:")

    manager = RepositoryManager()
    repo_path = manager.clone_repository(
        repo_url,
        repo_name
    )
    analyzer  = RepositoryAnalyzer()
    result = analyzer.analyze(repo_path)
    

    print("\n========== REPOSITORY ANALYSIS ==========")

    print(f"Total Files: {result['total_files']}")

    print(
        f"Source Files :{len(result['source_files'])}"
    )

    print(
        f"Test Files: {len(result['test_files'])}"
    )

    print("\nLanguages:")

    for language, count in result["languages"].items():
        print(f"  - {language}: {count}")

    print("\nDirectories:")

    for directory in result["directories"]:
        print(f"  - {directory}")

    print("\nSource Files:")
    for file in result["source_files"]:
        print(f" - {file}")

    print("\nTest Files")
    for file in result["test_files"]:
        print(f" - {file}")

if __name__=="__main__":
    main()





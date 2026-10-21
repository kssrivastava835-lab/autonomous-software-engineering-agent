from ingestion.ingestion_pipeline import IngestionPipeline

REPO_PATH = "workspace/agent-test-repo"


def test_unified_ingestion_pipeline():
    print("\n========== UNIFIED INGESTION TEST ==========")

    pipeline = IngestionPipeline()
    result = pipeline.ingest(REPO_PATH)

    print("\n========== PIPELINE REPORT ==========")
    print("Files scanned:", result["files_scanned"])
    print("Supported files:", result["supported_files"])
    print("Files processed:", result["files_processed"])
    print("Files skipped:", result["files_skipped"])
    print("Total chunks:", result["total_chunks"])
    print("Errors:", len(result["errors"]))

    if result["errors"]:
        print("\nProcessing errors:")
        for error in result["errors"]:
            print(error)

    assert result["files_scanned"] > 0, "No files discovered."
    assert result["files_processed"] > 0, "No Python files processed."
    assert result["total_chunks"] > 0, "No chunks generated."

    for chunk in result["chunks"]:
        assert isinstance(chunk.get("source_code"), str)
        assert isinstance(chunk.get("metadata"), dict)

        for key in (
            "file_path",
            "language",
            "chunk_type",
            "name",
            "start_line",
            "end_line",
        ):
            assert key in chunk["metadata"], f"Missing metadata field: {key}"

    discovered_names = {chunk["metadata"]["name"] for chunk in result["chunks"]}

    expected_names = {"add", "divide", "create_user"}
    missing_names = expected_names - discovered_names

    assert not missing_names, f"Expected functions not found: {missing_names}"

    print("\nPASS: All unified ingestion tests passed!")


if __name__ == "__main__":
    test_unified_ingestion_pipeline()

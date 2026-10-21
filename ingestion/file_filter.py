import os


class FileFilter:
    SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs"}

    def is_supported(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()

        return extension in self.SUPPORTED_EXTENSIONS

    def filter_files(self, files):
        return [file for file in files if self.is_supported(file)]

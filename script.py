import os
import time
import shutil
from zipfile import ZipFile, BadZipFile


class FileOrganizer:
    def __init__(self, source, target_folder_param):
        self.source = source
        self.target_folder = target_folder_param

    def organize(self):
        if self.is_zip_file():
            self.process_zip_file()
        else:
            self.process_folder()

    def is_zip_file(self):
        try:
            with ZipFile(self.source) as _:
                return True
        except BadZipFile:
            return False

    def process_zip_file(self):
        with ZipFile(self.source, 'r') as zip_ref:
            for file in zip_ref.infolist():
                self.process_file(file.filename, zip_ref.extract(file))

    def process_folder(self):
        for root, _, files in os.walk(self.source):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_file(file, file_path)

    def process_file(self, file_name, file_path):
        if not os.path.isfile(file_path):
            return

        file_creation_time = os.path.getmtime(file_path)
        file_creation_date = time.gmtime(file_creation_time)
        year = file_creation_date.tm_year
        month = file_creation_date.tm_mon

        target_folder = os.path.join(self.target_folder, str(year), f"{month:02d}")
        os.makedirs(target_folder, exist_ok=True)

        shutil.copy2(file_path, os.path.join(target_folder, file_name))


if __name__ == "__main__":
    source = "icons.zip"
    target_folder = "files_by_year_month"
    run_script = FileOrganizer(source=source, target_folder_param=target_folder)
    run_script.organize()

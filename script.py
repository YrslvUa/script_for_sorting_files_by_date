import os
import time
import shutil
from zipfile import ZipFile


class FileOrganizer:
    def __init__(self, source, target_folder):
        self.source = source
        self.target_folder = target_folder

    def organize_files(self):
        if os.path.isdir(self.source):
            self.organize_files_from_folder()
        elif os.path.isfile(self.source) and self.source.endswith('.zip'):
            self.organize_files_from_zip()
        else:
            raise ValueError("Invalid source. Please provide a folder or a zip file.")

    def organize_files_from_folder(self):
        for root, _, files in os.walk(self.source):
            for file in files:
                self.process_file(os.path.join(root, file))

    def organize_files_from_zip(self):
        with ZipFile(self.source, 'r') as zip_ref:
            for file in zip_ref.infolist():
                self.process_file(file)

    def process_file(self, file_info):
        if isinstance(file_info, str):
            file_creation_time = os.path.getmtime(file_info)
            file_creation_date = time.gmtime(file_creation_time)
            year = file_creation_date.tm_year
            month = file_creation_date.tm_mon
        else:
            file_creation_time = file_info.date_time
            year, month = file_creation_time[0], file_creation_time[1]

        target_folder = os.path.join(self.target_folder, str(year), f"{month:02d}")
        os.makedirs(target_folder, exist_ok=True)

        if isinstance(file_info, str):
            shutil.copy2(file_info, target_folder)
        else:
            with ZipFile(self.source, 'r') as zip_ref:
                zip_ref.extract(file_info, target_folder)


if __name__ == "__main__":
    source = "icons.zip"
    target_folder = "icons_by_year_2"
    organizer = FileOrganizer(source, target_folder)
    organizer.organize_files()

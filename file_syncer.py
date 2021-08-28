import hashlib
from pathlib import Path
from shutil import copyfile
from datetime import datetime
import os
import json
import ntpath


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def is_file_exist(filename: str) -> bool:
    file = Path(filename)
    return file.exists()


class HashDbFile:
    isExist = None

    def __init__(self, db_file_name: str):
        self.db_file_name = db_file_name

    def get_prev_hash(self, file_name: str):
        last_hash = str()
        if is_file_exist(self.db_file_name) is False:
            self.isExist = False
            print(f"There is no {self.db_file_name} file! The clear {self.db_file_name} file will be created")
            return last_hash

        db_hash_list = []
        with open(self.db_file_name, encoding='utf8') as f:
            for line in f:
                db_hash_list.append(line.strip())

        self.isExist = True
        if db_hash_list:
            last_hash = db_hash_list[-1]
        return last_hash

    def add_hash(self, current_hash):
        file_handler = open(self.db_file_name, "a", encoding='utf-8')
        file_handler.write(current_hash + "\n")
        return


def calculate_hash(filename: str):
    sha256_hash = hashlib.sha256()
    chunk_size = 4096  # bytes
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of chunk_size bytes
        for byte_block in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    print("start file backup")

    with open("config.json", 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)

    hash_db = HashDbFile(config["program"]["hash_db_file_name"])
    files_to_backup = config["backup_files"]

    for key in files_to_backup:
        file_data = files_to_backup[key]
        source_path = str(file_data["source"])
        dest_path = str(file_data["dest"])

        if is_file_exist(source_path) is False:
            print(f"source file with label: {key} doesn't exist")
            return

        current_hash = calculate_hash(source_path)
        writing_time = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

        file_name_without_ext, source_file_extension = os.path.splitext(source_path)
        source_file_name = path_leaf(file_name_without_ext)
        dest_path = str(f"{dest_path}{source_file_name}_{writing_time}{source_file_extension}")

        prev_hash = hash_db.get_prev_hash(source_file_name)

        if current_hash != prev_hash:
            copyfile(source_path, dest_path)
            hash_db.add_hash(current_hash)
            print(f"file with label \"{key}\" synced")
        else:
            print(f"file with label \"{key}\" has already been synced")

    print("end file backup")
    return 0


if __name__ == '__main__':
    main()

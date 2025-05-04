import os
import time
from variables import MAX_SIZE, HOLDING_FOLDER, QUARANTINE_FOLDER, PRODUCTION_FOLDER
from send_to_s3 import que_s3_uploader


def is_suspicious(file_path):
    if os.path.getsize(file_path) > MAX_SIZE:
        return True
    with open(file_path, "rb") as f:
        content = f.read()
        if b"good_file" not in content:
            return True
    return False


def scan():
    print(f"[cron] scanner.py started at {time.ctime()}")
    if not os.path.exists(HOLDING_FOLDER):
        os.makedirs(HOLDING_FOLDER)
    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)
    if not os.path.exists(PRODUCTION_FOLDER):
        os.makedirs(PRODUCTION_FOLDER)
    for fname in os.listdir(HOLDING_FOLDER):
        fpath = os.path.join(HOLDING_FOLDER, fname)
        if not os.path.isfile(fpath):
            continue
        if is_suspicious(fpath):
            move_file(fpath, QUARANTINE_FOLDER)
        else:
            move_file(fpath, PRODUCTION_FOLDER)
    que_s3_uploader()


def move_file(file_path, dest_folder):
    filename = os.path.basename(file_path)
    print(f"[cron] Moving {filename} to {dest_folder}...")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    dest_file_name = os.path.join(dest_folder, filename)
    os.rename(file_path, dest_file_name)


if __name__ == "__main__":
    scan()

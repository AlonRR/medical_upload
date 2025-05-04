import os
import time
from botocore.exceptions import ClientError
import boto3
from dotenv import load_dotenv
from variables import QUARANTINE_FOLDER, PRODUCTION_FOLDER, ALERT_LOG

load_dotenv()

QUARANTINE_BUCKET = os.getenv("QUARANTINE_BUCKET")
PRODUCTION_BUCKET = os.getenv("PRODUCTION_BUCKET")
AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")
REGION = os.getenv("AWS_REGION")

s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET,
    region_name=REGION,
)


def que_s3_uploader():
    # if not os.path.exists(QUARANTINE_FOLDER):
    #     os.makedirs(QUARANTINE_FOLDER)
    # if not os.path.exists(PRODUCTION_FOLDER):
    #     os.makedirs(PRODUCTION_FOLDER)
    print(f"[cron] que_s3_uploader.py started at {time.ctime()}")
    quarantine_files = os.listdir(path=QUARANTINE_FOLDER)
    production_files = os.listdir(path=PRODUCTION_FOLDER)
    for file in quarantine_files:
        file_path = os.path.join(QUARANTINE_FOLDER, file)
        if os.path.isfile(file_path):
            try:
                s3.upload_file(file_path, QUARANTINE_BUCKET, file)
                alert(f"Uploaded {file} to {QUARANTINE_BUCKET}")
                print(f"[cron] uploded {file} to {QUARANTINE_BUCKET}...", flush=True)
                os.remove(file_path)
            except ClientError as e:
                alert(f"Failed to upload {file} to S3: {e}")
    for file in production_files:
        file_path = os.path.join(PRODUCTION_FOLDER, file)
        if os.path.isfile(file_path):
            try:
                s3.upload_file(file_path, PRODUCTION_BUCKET, file)
                print(f"[cron] uploaded {file} to {PRODUCTION_BUCKET}...", flush=True)
                os.remove(file_path)
            except ClientError as e:
                alert(f"Failed to upload {file} to S3: {e}")


def alert(msg):
    with open(ALERT_LOG, "a") as f:
        f.write(f"[!] {time.ctime()} ALERT: {msg}\n")
    print(f"[!] ALERT: {msg}")


que_s3_uploader()

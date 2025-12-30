import os
import time
import gzip
import uuid
import boto3
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = os.getenv("LOG_PATH")
SPOOL_DIR = os.getenv("SPOOL_DIR")
BUCKET = os.getenv("S3_BUCKET")
PREFIX = os.getenv("S3_PREFIX")
REGION = os.getenv("S3_REGION")

os.makedirs(SPOOL_DIR, exist_ok=True)

ENDPOINT = os.getenv("S3_ENDPOINT_URL")
ACCESS = os.getenv("S3_ACCESS_KEY")
SECRET = os.getenv("S3_SECRET_KEY")

s3 = boto3.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS,
    aws_secret_access_key=SECRET
)


def upload(lines):
    ts = datetime.now(timezone.utc)
    key = f"{PREFIX}/year={ts.year}/month={ts.month:02d}/day={ts.day:02d}/{uuid.uuid4()}.json.gz"
    local = Path(SPOOL_DIR) / "batch.json.gz"

    with gzip.open(local, "wt") as f:
        for line in lines:
            f.write(line)

    s3.upload_file(str(local), BUCKET, key)
    local.unlink()
    print(f"Uploaded {key}")

with open(LOG_PATH, "r") as f:
    f.seek(0, 2)
    buffer = []
    while True:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue
        buffer.append(line)
        if len(buffer) >= 5:
            upload(buffer)
            buffer = []


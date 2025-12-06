import os
import boto3
from boto3.session import Config

SUPA_S3_ENDPOINT = os.getenv("SUPA_S3_ENDPOINT")
SUPA_S3_ACCESS_KEY = os.getenv("SUPA_S3_ACCESS_KEY")
SUPA_S3_SECRET_KEY = os.getenv("SUPA_S3_SECRET_KEY")
SUPA_REGION = os.getenv("SUPA_REGION")

s3 = boto3.client(
    "s3",
    endpoint_url=SUPA_S3_ENDPOINT,
    aws_access_key_id=SUPA_S3_ACCESS_KEY,
    aws_secret_access_key=SUPA_S3_SECRET_KEY,
    region_name=SUPA_REGION,
    config=Config(signature_version="s3v4"),
)

def test_list_buckets():
    try:
        response = s3.list_buckets()
        print("Connected successfully.")
        print("Buckets:")
        for bucket in response.get("Buckets", []):
            print(" -", bucket["Name"])
    except Exception as e:
        print("Connection failed:", e)

def get_signed_url(bucket: str, key: str, expires_seconds=3600) -> str:
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_seconds,
    )

def upload_pdf_to_supabase(bucket: str, file_bytes: bytes, filename: str) -> str:
    key = f"{filename}"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=file_bytes,
        ContentType="application/pdf",
    )
    return key

if __name__ == "__main__":
    test_list_buckets()
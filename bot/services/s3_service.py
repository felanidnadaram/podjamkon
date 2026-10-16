import boto3
from botocore.client import Config
from config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT, S3_BUCKET

# Create an S3 client configured for the custom endpoint (S3-compatible storage)
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version="s3v4"),
)

def generate_download_url(file_key: str, expiration: int = 600) -> str:
    """
    Generate a presigned URL to download an object from S3.
    The URL is valid for `expiration` seconds (default 10 minutes).
    """
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": file_key},
        ExpiresIn=expiration,
    )
    return url
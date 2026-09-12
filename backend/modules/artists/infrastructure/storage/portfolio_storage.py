import boto3
from botocore.config import Config
from django.conf import settings


class PortfolioStorage:
    def __init__(self) -> None:
        common = {
            "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
            "region_name": settings.S3_REGION_NAME,
            "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        }
        self.client = boto3.client("s3", endpoint_url=settings.S3_ENDPOINT_URL, **common)
        self.public_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_PUBLIC_ENDPOINT_URL,
            **common,
        )

    def create_upload_url(self, object_key: str, content_type: str) -> str:
        return self.public_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.S3_BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=settings.S3_UPLOAD_EXPIRATION_SECONDS,
        )

    def create_download_url(self, object_key: str) -> str:
        return self.public_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET_NAME, "Key": object_key},
            ExpiresIn=settings.S3_DOWNLOAD_EXPIRATION_SECONDS,
        )

    def inspect(self, object_key: str) -> tuple[int, str, bytes]:
        metadata = self.client.head_object(Bucket=settings.S3_BUCKET_NAME, Key=object_key)
        result = self.client.get_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=object_key,
            Range="bytes=0-15",
        )
        return metadata["ContentLength"], metadata["ContentType"], result["Body"].read()

    def delete(self, object_key: str) -> None:
        self.client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=object_key)

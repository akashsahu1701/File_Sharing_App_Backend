import configparser
import boto3
from botocore.exceptions import NoCredentialsError
from flask import current_app
from werkzeug.datastructures import FileStorage

config = configparser.ConfigParser()
config.read("config.ini")


class S3Service:
    def __init__(self):
        self.s3: boto3.client = boto3.client(
            "s3",
            aws_access_key_id=config.get("settings", "AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config.get("settings", "AWS_SECRET_ACCESS_KEY"),
            region_name=config.get("settings", "AWS_S3_REGION"),
        )
        self.bucket_name = config.get("settings", "AWS_S3_BUCKET_NAME")

    def upload_file(self, file: FileStorage):
        try:
            filename = file.filename
            content_type = file.content_type

            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                filename,
                ExtraArgs={"ContentType": content_type},
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
        except NoCredentialsError:
            return None

    def delete_file(self, image_url: str):
        filename = image_url.split("/")[-1]
        self.s3.delete_object(Bucket=self.bucket_name, Key=filename)
        return True

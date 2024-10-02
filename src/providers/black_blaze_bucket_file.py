import boto3
import os
from botocore.exceptions import ClientError
from nest.core import Injectable
from src.config import configs_bucket
from fastapi import UploadFile


@Injectable
class BlackBlazeBucketFile:
    def __init__(self):
        self.configs = configs_bucket
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.configs['endpoint'],
            region_name=self.configs['region'],
            aws_access_key_id=self.configs['key_id'],
            aws_secret_access_key=self.configs['app_key']
        )
    async def delete_file(self, recognition_id: str, file_name: str) -> None:
        try:
            self.s3_client.delete_object(
                Bucket=self.configs['bucket_name'],
                Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}"
            )
            # deletar pasta
            self.s3_client.delete_object(
                Bucket=self.configs['bucket_name'],
                Key=f"{self.configs['upload_folder']}/{recognition_id}"
            )
        except ClientError as e:
            print(e)
            raise
        
    async def download_file(self, recognition_id: str, file_name: str) -> bytes:
        try:
            response = self.s3_client.get_object(
                Bucket=self.configs['bucket_name'],
                Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}"
            )
            print("Download completed successfully.")
            return response['Body'].read()
        except ClientError as e:
            print(e)
            raise 
    
    async def upload_file(self, file: UploadFile, recognition_id: str,file_name: str) -> dict:
        upload_id = None
        try:
            multipart_upload = self.s3_client.create_multipart_upload(
                Bucket=self.configs['bucket_name'],
                Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}",
            )
            upload_id = multipart_upload['UploadId']
            upload_promises = []

            num_parts_left = 5
            file_data = await file.read()  # Leitura do conteúdo do arquivo
            part_size = -(-len(file_data) // num_parts_left)  # Divisão por partes

            if not (part_size > 1024 * 1024 * 5):  # Verificar tamanho mínimo
                num_parts_left = 1
                part_size = -(-len(file_data) // num_parts_left)

            for i in range(num_parts_left):
                start = part_size * i
                end = min(start + part_size, len(file_data))
                part = file_data[start:end]

                response = self.s3_client.upload_part(
                    Bucket=self.configs['bucket_name'],
                    Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}",
                    PartNumber=i + 1,
                    UploadId=upload_id,
                    Body=part
                )
                upload_promises.append({
                    'ETag': response['ETag'],
                    'PartNumber': i + 1
                })

            file_response = self.s3_client.complete_multipart_upload(
                Bucket=self.configs['bucket_name'],
                Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}",
                UploadId=upload_id,
                MultipartUpload={'Parts': upload_promises}
            )
            print("Upload completed successfully.")
            #    'url': f"https://{os.getenv('BACKBLAZE_BUCKET')}.s3.{os.getenv('REGION')}.backblazeb2.com/{os.getenv('UPLOAD_FOLDER')}/{data['originalname']}",
            url = f"https://{self.configs['bucket_name']}.s3.{self.configs['region']}.backblazeb2.com/{self.configs['upload_folder']}/{recognition_id}/{file_name}"
            return url

        except Exception as e:
            print(e)
            if upload_id:
                self.s3_client.abort_multipart_upload(
                    Bucket=self.configs['bucket_name'],
                    Key=f"{self.configs['upload_folder']}/{recognition_id}/{file_name}",
                    UploadId=upload_id
                )
            raise

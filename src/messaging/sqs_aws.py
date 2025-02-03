import boto3
import logging
import json
from nest.core import Injectable
from src.config import configs_queue



logger = logging.getLogger(__name__)

@Injectable
class SqsAws:
    def __init__(self) -> None:
        self.configs = configs_queue
        self.sqs_client = boto3.client(
            'sqs',
            endpoint_url=self.configs['queue_url'],
            region_name=self.configs['region'],
            aws_access_key_id=self.configs['key_id'],
            aws_secret_access_key=self.configs['app_key']
        )

    def receive_message(self) -> dict:
        try:
            logger.info('Receiving message from SQS')
            response = self.sqs_client.receive_message(
                QueueUrl=self.configs['queue_url'],
                MaxNumberOfMessages=1,
                VisibilityTimeout=30,
                WaitTimeSeconds=20
            )
            if 'Messages' in response:
                return response['Messages'][0]
            return {}
        except Exception as e:
            logger.error('Error receiving message from SQS {}'.format(e))
            raise

    def delete_message(self, receipt_handle: str) -> None:
        try:
            logger.info('Deleting message from SQS')
            self.sqs_client.delete_message(
                QueueUrl=self.configs['queue_url'],
                ReceiptHandle=receipt_handle
            )
        except Exception as e:
            logger.error('Error deleting message from SQS {}'.format(e))
            raise

    def send_message(self, message: dict) -> None:
        try:
            logger.info('Sending message to SQS {}'.format(message))
            
            self.sqs_client.send_message(
                QueueUrl=self.configs['queue_url'],
                MessageAttributes={
                    'recognition_id': {
                        'DataType': 'String',
                        'StringValue': message['recognition_id']
                    },
                    'file_name': {
                        'DataType': 'String',
                        'StringValue': message['file_name']
                    },
                    'extension': {
                        'DataType': 'String',
                        'StringValue': message['extension']
                    },
                    'path_file': {
                        'DataType': 'String',
                        'StringValue': message['path_file']
                    }
                },
                MessageBody=json.dumps(message)
            )
        except Exception as e:
            logger.error('Error sending message to SQS {}'.format(e))
            raise
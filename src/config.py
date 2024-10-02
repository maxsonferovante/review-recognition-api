import os
from dotenv import load_dotenv
from nest.core.database.odm_provider import OdmProvider
from src.modules.recognition.recognition_entity import Recognition
from src.modules.review.review_entity import Review

load_dotenv()
config = OdmProvider(
    config_params={
        "db_name": os.getenv("DB_NAME", "review_recognition"),
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "port": os.getenv("DB_PORT", 27017),
    },
    document_models=[Recognition, Review],
)


version = "0.0.2"


configs_bucket = {
    'upload_folder' : os.getenv('UPLOAD_FOLDER'),
    'endpoint' : os.getenv('ENDPOINT_S3'),
    'key_id' : os.getenv('KEY_ID'),
    'app_key' : os.getenv('APP_KEY'),
    'bucket_name' : os.getenv('BACKBLAZE_BUCKET'),
    'region' : os.getenv('REGION'),
}
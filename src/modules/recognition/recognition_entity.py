from beanie import Document
from datetime import datetime
from typing import Dict        

class Recognition(Document):
    created_at: datetime
    file_name: str
    extension: str
    class Config:
        schema_extra = {
            "recognition": {
                    "file_name": "example.jpg",
                    "created_at": "2022-01-01T00:00:00.000Z",
                    "extension": "pdf"
                }
        }



def mongo_recognition_to_pydantic(document: Recognition) -> Dict:
    return {
        "id": str(document.id),
        "created_at": document.created_at,
        "file_name": document.file_name,
        "extension": document.extension
    }
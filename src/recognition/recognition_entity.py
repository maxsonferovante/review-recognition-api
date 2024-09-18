from beanie import Document
from datetime import datetime
        
class Recognition(Document):
    created_at: datetime
    file_name: str
    id: str
    
    class Config:
        schema_extra = {
            "recognition": {
                    "file_name": "example.jpg",
                    "id": "1234",
                    "created_at": "2022-01-01T00:00:00.000Z"
                }
        }

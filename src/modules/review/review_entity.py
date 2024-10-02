from beanie import Document
        
        
class Review(Document):
    name: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Example Name",
            }
        }

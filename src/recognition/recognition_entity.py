from beanie import Document
        
        
class Recognition(Document):
    name: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Example Name",
            }
        }

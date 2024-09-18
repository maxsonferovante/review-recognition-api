from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import unicodedata 


def genarete_id():
    return str(uuid.uuid4())

class Recognition(BaseModel):
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    file_name: str
    id: str = Field(init=False, default_factory=genarete_id)    
    
    
    def __post_init__(self):
        self.__normalize_file_name()
        
    def __normalize_file_name(self):
        self.file_name.lower().replace(" ", "_")
        self.file_name = unicodedata.normalize('NFKD', self.file_name).encode('ASCII', 'ignore').decode('utf-8')
        
        
        
    


from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

import unicodedata
import uuid

#enum de estados de processamento

class RecognitionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Recognition(BaseModel):    
    created_at: datetime = Field(default_factory=datetime.now, init=False)
    id: Optional[str] = Field(init=False, default=None)
    file_name: str
    extension: str
    status: RecognitionStatus = Field(default=RecognitionStatus.PENDING, init=False)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.__normalize_file_name()
        
    def __normalize_file_name(self):
        self.file_name = self.file_name.lower().replace(" ", "_")
        self.file_name = unicodedata.normalize('NFKD', self.file_name).encode('ASCII', 'ignore').decode('utf-8')

    def __setattr__(self, name, value):
        if name == 'id':
            value = str(value)
        super().__setattr__(name, value)
        


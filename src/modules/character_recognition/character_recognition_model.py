from datetime import datetime
from typing import Dict
from pydantic import BaseModel, Field

from src.modules.recognition.recognition_model import RecognitionStatus



# class que representa o reconhecimento em 
# processamento

class ProcessingRecognition(BaseModel):
    id: str
    progress: int = Field(default=0)
    status: RecognitionStatus = Field(default=RecognitionStatus.PROCESSING, init=False)
    updated_at: datetime = Field(default_factory=datetime.now, init=False)
    
    def __setattr__(self, name, value):
        # Lógica personalizada apenas para 'progress'
        if name == 'progress':
            if value < 0:
                value = 0
            if value > 100:
                value = 100
        # Atualiza 'updated_at' quando o progresso muda
        super().__setattr__(name, value)  # Chama o __setattr__ de BaseModel
        
        # Evitar recursão direta aqui, atualizando manualmente updated_at
        if name != 'updated_at':  # Prevenir loop ao modificar 'updated_at'
            object.__setattr__(self, 'updated_at', datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "progress": self.progress,
            "updated_at": self.updated_at.isoformat()
        }
        

# class que representa o reconhecimento concluído
class CompletedRecognition(BaseModel):
    id: str
    status: str = Field(default=RecognitionStatus.COMPLETED, init=False)
    data: Dict
    updated_at: datetime = Field(default_factory=datetime.now, init=False)
    
    
# class que representa a lista de reconhecimentos em processamento
class ProcessingRecognitions(BaseModel):
    recognitions: Dict[str, ProcessingRecognition] = Field(default_factory=dict)
    
    def add_recognition(self, recognition: ProcessingRecognition):
        self.recognitions[recognition.id] = recognition
    
    def remove_recognition(self, id: str):
        self.recognitions.pop(id, None)
    
    def get_recognition(self, id: str):
        return self.recognitions.get(id)
    
    def dict(self):
        return {id: recognition.dict() for id, recognition in self.recognitions.items()}
    
    def __iter__(self):
        return iter(self.recognitions.values())
    
    def __len__(self):
        return len(self.recognitions)
    
    def __contains__(self, id):
        return id in self.recognitions
    
# class que representa os reconhecimentos processados

class CompletedRecognitions(BaseModel):
    recognitions: Dict[str, CompletedRecognition] = Field(default_factory=dict)
    
    def add_recognition(self, recognition: CompletedRecognition):
        self.recognitions[recognition.id] = recognition
    
    def remove_recognition(self, id: str):
        self.recognitions.pop(id, None)
    
    def get_recognition(self, id: str):
        return self.recognitions.get(id, None)
    
    def dict(self):
        return {id: recognition.dict() for id, recognition in self.recognitions.items()}
    
    def __iter__(self):
        return iter(self.recognitions.values())
    
    def __len__(self):
        return len(self.recognitions)
    
    def __contains__(self, id):
        return id in self.recognitions
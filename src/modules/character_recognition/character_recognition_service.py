from nest.core import Injectable
from fastapi import UploadFile
from src.modules.recognition.recognition_model import RecognitionStatus
from src.modules.recognition.recognition_entity import Recognition as RecognitionEntity
from .character_recognition_model import ProcessingRecognition, CompletedRecognition, ProcessingRecognitions, CompletedRecognitions

import time
from datetime import datetime

import os

@Injectable
class CharacterRecognitionService:
    # Uma instância de ProcessingRecognitions para manter a lista de reconhecimentos em andamento
    processing_recognitions = ProcessingRecognitions()
    completed_recognitions = CompletedRecognitions()

   
    def run(self, id: str):
        try:
            # Adiciona uma nova entrada na lista de reconhecimentos em processamento
            self.processing_recognitions.add_recognition(
                    ProcessingRecognition(
                        id=id, progress=0
                        )
                    )

            for index in range(10):
                print(f"Running character recognition service ({id}) - [{'#' * index}{'-' * (10 - index)}] - {index}/10")
                time.sleep(10)
                self.updated_progress(id, (index + 1) * 10)

            print(f"Running character recognition service ({id}) - completed")
            self.save_results(id, "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
            print(f"Running character recognition service ({id}) - updated status")
        except Exception as e:
            print(f"Running character recognition service ({id}) - error: {e}")
            self.updated_status(id, RecognitionStatus.FAILED)
    
    def get_results(self, id: str):
        # Verifica se o reconhecimento está completo e retorna o resultado
        result = self.completed_recognitions.get_recognition(id)
        if result and result.status == RecognitionStatus.COMPLETED:
            return result
        return None

    def get_all_results(self):
        # Retorna todos os reconhecimentos em andamento
        return self.completed_recognitions.dict()

    def clear_results(self):
        # Limpa todos os reconhecimentos em andamento
        self.processing_recognitions = ProcessingRecognitions()

    def get_status(self, id: str):
        # Retorna o status de um reconhecimento específico
        recognition = self.processing_recognitions.get_recognition(id)
        if recognition:
            return recognition.dict()
        return None

    def save_results(self, id: str, data: str):
        # Atualiza os resultados quando o reconhecimento é concluído
        recognition = self.processing_recognitions.get_recognition(id)
        if recognition:
            completed_recognition = CompletedRecognition(id=id, data={"result": data})
            self.completed_recognitions.add_recognition(completed_recognition)
            self.processing_recognitions.remove_recognition(id)
            

    def updated_status(self, id: str, status: RecognitionStatus):
        # Atualiza o status de um reconhecimento em processamento
        recognition = self.processing_recognitions.get_recognition(id)
        if recognition:
            recognition.status = status

    def updated_progress(self, id: str, progress: int):
        # Atualiza o progresso de um reconhecimento em andamento
        recognition = self.processing_recognitions.get_recognition(id)
        if recognition:
            try:
                recognition.progress = progress
            except Exception as e:
                print(f"Error updating progress: {e}")
                recognition.status = RecognitionStatus.FAILED
        else:
            print(f"Recognition {id} not found")

    def save_file_in_disk(self, file: UploadFile, file_name: str, path_to_save: str):
        # Salva um arquivo no disco na pasta temp, que está na raiz do projeto
        #  usa path_to_save como nome da pasta onde o arquivo será salvo
        with open(f"temp/{path_to_save}/{file_name}", "wb") as f:
            os.makedirs(f"temp/{path_to_save}", exist_ok=True)
            f.write(file)
            f.close()
            print(f"File {file_name} saved in disk")
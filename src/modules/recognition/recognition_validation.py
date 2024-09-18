from fastapi import UploadFile
from .recognition_exceptions import FileTypeNotAllowed, FileSizeExceeded


# Definir tipos permitidos
ALLOWED_EXTENSIONS = {'application/pdf'}
# Definir tamanho máximo (em bytes)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def validate_file_type(file: UploadFile):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise FileTypeNotAllowed()

def validate_file_size(file: UploadFile):
    file_size = len(file.file.read())
    file.file.seek(0)  # Volta para o início do arquivo após leitura
    if file_size > MAX_FILE_SIZE:        
        raise FileSizeExceeded()

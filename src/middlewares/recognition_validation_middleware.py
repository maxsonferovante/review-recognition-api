from fastapi import UploadFile, Request, FastAPI
from fastapi.responses import StreamingResponse
from src.modules.recognition.recognition_exceptions import FileTypeNotAllowed, FileSizeExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse  # Importar JSONResponse

# Definir tipos permitidos
ALLOWED_EXTENSIONS = {'application/pdf'}
# Definir tamanho máximo (em bytes)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

class RecognitionValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        # lista de validações
        self.validations = [validate_file_type, validate_file_size]
        
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path == "/recognition/upload" and request.method == "POST":
            file = await request.form()
            for validation in self.validations:
                error = validation(file["file"])
                if error is not None:
                    return JSONResponse(
                        status_code=error.status_code,
                        content=error.detail
                    )
            # request.form = file
        # 
        return response

def validate_file_type(file: UploadFile):
    if file.content_type not in ALLOWED_EXTENSIONS:
        return FileTypeNotAllowed()
    return None
def validate_file_size(file: UploadFile):
    file_size = len(file.file.read())
    file.file.seek(0)  # Volta para o início do arquivo após leitura
    if file_size > MAX_FILE_SIZE:        
        return FileSizeExceeded()
    return None

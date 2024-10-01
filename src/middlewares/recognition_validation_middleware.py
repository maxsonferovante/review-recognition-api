from fastapi import UploadFile
from src.modules.recognition.recognition_exceptions import FileTypeNotAllowed, FileSizeExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse  # Importar JSONResponse

# Definir tipos permitidos
ALLOWED_EXTENSIONS = {'application/pdf'}
# Definir tamanho máximo (em bytes)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

class RecognitionValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # lista de validações
        self.validations = [validate_file_type, validate_file_size]
        
    async def dispatch(self, request, call_next):
        if request.url.path == "/recognition/upload" and request.method == "POST":
            file = await request.form()
            for validation in self.validations:
                error = validation(file["file"])
                if error:
                    """ 
                    error é uma instância de FileTypeNotAllowed ou FileSizeExceeded,
                    mas recebo o erro:    await response(scope, wrapped_receive, send)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'FileSizeExceeded' object is not callable
                    """
                    return JSONResponse(
                        status_code=error.status_code,
                        content=error.detail
                    )
        response = await call_next(request)
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

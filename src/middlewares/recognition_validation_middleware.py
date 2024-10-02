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
        
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path == "/recognition/upload" and request.method == "POST":
            errors = []            
            
            errors.append(validate_file_size(file_content=request.headers.get("content-length")))
            
            # errors.append(validate_file_type(content_type=request.headers.get("content-type")))
            
            for error in errors:
                if error is not None:
                    return JSONResponse(
                        status_code=error.status_code,
                        content=error.detail
                    )
            
            
            # file.file.seek(0) 
            pass
        return response

def validate_file_type(content_type: str = None):
    if content_type not in ALLOWED_EXTENSIONS:
        raise FileTypeNotAllowed()
    
def validate_file_size(file_content = None):
    if int(file_content) > MAX_FILE_SIZE:        
        return FileSizeExceeded()
    return None

from fastapi import HTTPException

class FileSizeExceeded(HTTPException):
    def __init__(self):
        super().__init__(status_code=422, detail=
                         [
                {
                    "loc": ["file"],
                    "msg": "File size exceeded. Max file size is 20MB",
                    "type": "file"
                }
            ]
        )
        
class FileTypeNotAllowed(HTTPException):
    def __init__(self):
        super().__init__(status_code=422, detail=
                         [
                {
                    "loc": ["file"],
                    "msg": "File type not allowed. Only PDF files are allowed",
                    "type": "file"
                }
            ]
        )
        
class RecognitionNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail=
                         [
                {
                    "loc": ["recognition"],
                    "msg": "Recognition not found",
                    "type": "recognition"
                }
            ]
        )


class InternalServerError(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=500, detail=
                         [
                {
                    "loc": ["internal"],
                    "detail": detail,
                    "type": "internal"
                }
            ]
        )        
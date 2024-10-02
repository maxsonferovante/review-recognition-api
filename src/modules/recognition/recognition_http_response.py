from fastapi.responses import JSONResponse
from .recognition_model import Recognition


class AcceptedResponse(JSONResponse):
    def __init__(self, recognition: Recognition):
        body = {
            'message': "Recognition accepted",
            'data': recognition.dict()
        }    
        super().__init__(content=body, status_code=201)



class ProcessingResponse(JSONResponse):
    def __init__(self, content=None):
        body = {
            "message": "Processing recognition"
        }
        if content:
            body.update(content)
        
        super().__init__(content=body, status_code=200)
        
        
class CompletedResponse(JSONResponse):
    def __init__(self, content=None):
        body = {
            "message": "Recognition completed",
            'data': content
        }        
        super().__init__(content=body, status_code=200)
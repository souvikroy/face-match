import asyncio
from types import SimpleNamespace
from .. import HTTPException, UploadFile

class Response(SimpleNamespace):
    def json(self):
        return getattr(self, 'data', None)

class TestClient:
    def __init__(self, app):
        self.app = app

    def post(self, path: str, files: dict):
        if path not in self.app.routes:
            raise HTTPException(status_code=404, detail='Not Found')
        filename, content, content_type = next(iter(files.values()))
        file = UploadFile(filename, content, content_type)
        func = self.app.routes[path]
        try:
            result = func(file=file)
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)
            return Response(status_code=200, data=result)
        except HTTPException as exc:
            return Response(status_code=exc.status_code, data={'detail': exc.detail})

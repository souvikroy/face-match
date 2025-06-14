class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class UploadFile:
    def __init__(self, filename: str, content: bytes = b"", content_type: str = "application/octet-stream"):
        self.filename = filename
        self.content_type = content_type
        self._content = content
    async def read(self) -> bytes:
        return self._content

class File:
    def __init__(self, default):
        self.default = default

class FastAPI:
    def __init__(self, title: str = ""):
        self.title = title
        self.routes = {}
    def post(self, path: str):
        def decorator(fn):
            self.routes[path] = fn
            return fn
        return decorator
    def add_middleware(self, middleware_cls, **kwargs):
        # Middleware is ignored in this stub
        return None


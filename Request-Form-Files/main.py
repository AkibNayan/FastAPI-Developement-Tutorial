from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated

app = FastAPI()

# Request Files
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"size": len(file)}

@app.post("/uploadfiles/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# Optional File Upload
@app.post("/files1/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    return {"size": len(file) if file else 0}

@app.post("/uploadfiles1/")
async def create_upload_file(file: UploadFile | None = None):
    return {"filename": file.filename if file else None}

@app.post("/files2/")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
    return {"file size": len(file)}

@app.post("/uploadfiles2/")
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as upload file")] = None):
    return {"filename": file.filename}

# Multiple File Uploads
@app.post("/files3/")
async def create_file(files: Annotated[list[bytes], File()]):
    return {"file size": [len(file) for file in files]}

@app.post("/uploadfiles3")
async def create_upload_file(files: list[UploadFile]):
    return {"filename": [file.filename for file in files]}

from starlette.responses import HTMLResponse
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# Request Forms and Files
@app.post("/files4/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type
    }
    
from os import stat
import fastapi
import fastapi.responses as _responses

app = fastapi.FastAPI()

import services

@app.get("/")
def root():
    return {"message": "Welcome to meme API"}

@app.get("/general-memes")
def get_general_memes():
    image_path = services.select_random_image("memes")
    return _responses.FileResponse(image_path)

@app.get("/cat-memes")
def get_cat_memes():
    image_path = services.select_random_image("Catmemes")
    return _responses.FileResponse(image_path)


@app.get("/programmer-memes")
def get_cat_memes():
    image_path = services.select_random_image("ProgrammerHumor")
    return _responses.FileResponse(image_path)

@app.post("/programmer-mems")
def create_programmer_meme(image: fastapi.UploadFile = fastapi.File(...)):
    file_path = services.upload_image("ProgrammerHumor", image)
    if file_path is None:
        return fastapi.HTTPException(status_code=409, detail="incorrect file type")
    return  _responses.FileResponse(file_path) 
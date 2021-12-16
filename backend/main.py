import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile

from src.pipeline import parse_document
from src.template import Ipid

# load env variables from .env from specified path
DOTENV_PATH = os.environ.get('DOTENV_PATH', './.env')
load_dotenv(dotenv_path=DOTENV_PATH, verbose=True)
PORT = int(os.environ.get('PORT'))


app = FastAPI()


@app.post("/file")
async def upload_file(file: UploadFile = File(...)) -> Ipid:
    bytes_file = await file.read()  # load pdf file
    parsed_document = parse_document(bytes_file)  # run pipeline
    return parsed_document


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)

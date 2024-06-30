from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
import shutil
import logging
import os

client = OpenAI(api_key="__")


from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Message(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/chat")
async def chat(message: Message):
    response_message = generate_response(message.message)
    return {"response": response_message}

def generate_response(message: str) -> str:
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ]
                )

    return response.choices[0].message.content

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Process the uploaded PDF file using LangChain
        # text = process_pdf(file_location)
        # return {"message": "File processed successfully", "content": text[:200]}  # Return first 200 characters for brevity
        return "yes"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


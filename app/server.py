from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
import os
import tempfile
from embedchain import App
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


app = FastAPI()
# Global variable to store the EmbedChain app
embed_app = App()

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
    response_message = embed_app.chat(message.message)
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
        contents = await file.read()
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
            # print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            # print(temp_file_path)

        logger.info("Processing file with EmbedChain")
        embed_app.add(temp_file_path, data_type="pdf_file")
        logger.info("Document processed and indexed")
        # Remove the temporary file
        os.unlink(temp_file_path)

        return JSONResponse(content={"message": f"File '{file.filename}' uploaded and processed successfully"}, status_code=200)
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


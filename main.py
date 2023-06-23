from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from chat import get_completion_from_messages,collect_messages_text
from pydantic import BaseModel



class Message(BaseModel):
    content: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    with open('templates/main.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/chat")
async def chat(message: Message):
    user_message = message.content
    response = collect_messages_text(user_message)

    return {"message": response}
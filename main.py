from fastapi import FastAPI
from users import router as users_router
from files import router as files_router
from chatbot import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(users_router, tags=["users"], prefix="/users")
app.include_router(files_router,tags=["files"],prefix="/files")
app.include_router(chat_router,tags=["chats"],prefix="/chats")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import  HTTPException, Depends , APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from functions.vectordb import context_vector_db
from functions.query_load import query_output, context_summary
from database import get_user_collection, get_db
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from functions.query_load import query_output
from bson.objectid import ObjectId

router = APIRouter()
class AssistantRequest(BaseModel):
    history: list
    prompt: str
    user_id: str

class SummaryRequest(BaseModel):
    user_id: str

userMap = {
    'assistant': 'ai',
    'user': 'human'
}

@router.post("/getAssistantResponse")
async def get_assistant_response(doc:AssistantRequest):
    history = doc.history
    user_id = doc.user_id
    prompt = doc.prompt
        
    QUERY = prompt + '\n\n'
    for chat in history:
        QUERY += chat['role'] + ": " + chat["content"] + "\n\n"
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docsearch = PineconeVectorStore(index_name=user_id, embedding=embeddings)
    response = query_output(QUERY, docsearch)
    return {"role": "assistant", "content": response['answer']}

def make_instance(userId :str, db=Depends(get_db)):
    try:
        users_collection = get_user_collection()
        user_data = users_collection.find_one({"_id": ObjectId(userId)})
        if user_data:
            context_vector_db(user_data['context'],userId)
        else:
            raise LookupError("Invalid credentials, Issue in making a vectordb instance")
    except Exception as e:
        print(str(e))




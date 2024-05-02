from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from models import FileUpload, ContextUpload
from database import get_db
from database import get_user_collection
from functions.file_processing_utils import process_pdf
from models import Session
from functions.vectordb import context_vector_db
import nest_asyncio
from bson.objectid import ObjectId
nest_asyncio.apply()

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(user_id: str = Form(...), file: UploadFile = Form(...), db: Session = Depends(get_db)):
    # print(len(file))
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format")
    file_path = './data/medical_document.pdf'
    file_data = await file.read()
    with open(file_path, "wb") as f:
            f.write(file_data)
    try:
        context = process_pdf(file_path)
        # print(len(context))
        await update_user_context(user_id, context, db)
    except Exception as e:
        return HTTPException(status_code=401, detail=str(e))
    return {"message": "success"}

@router.post('/update_context')
async def update_context_handler(doc:ContextUpload, db: Session = Depends(get_db)):
    user_id = doc.user_id
    context = doc.context
    
    try:
        await update_user_context(user_id, context, db)
    except Exception as e:
        return HTTPException(status_code=401, detail=str(e))
    return {"message": "success"}
    

async def update_user_context(user_id: str, context: str, db: Session = Depends(get_db)):
    user_collection = get_user_collection()
    try:
        _id = ObjectId(user_id)
        if user_collection.find_one(filter={
            '_id': _id
        }):
            user = user_collection.update_one(filter={
                '_id': _id
            }, update={
                '$push': {
                    'context': context
                }
            })
            context_vector_db(context, user_id)
        else:
            raise FileNotFoundError("User Not Found")
    except Exception as e:
        print(e)
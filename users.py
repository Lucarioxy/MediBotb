from fastapi import APIRouter, HTTPException, Depends, status
from models import User , Udisplay, LoginUser
from database import get_user_collection, get_db
from chatbot import make_instance

router = APIRouter()

@router.post("/signup/", response_model=Udisplay, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db=Depends(get_db)):
    users_collection = get_user_collection()
    users = None
    try:
        users = users_collection.find_one({"email": user.email})
    except Exception as e:
        print("Error is : ",e)
    if users is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = user.model_dump()
    user_id = users_collection.insert_one(user_data).inserted_id
    user_data['user_id'] = str(user_id)
    del user_data['password']

    temp = Udisplay(**user_data)
    print(temp)
    
    try:
        make_instance(str(user_id))
    except:
        users_collection.delete_one(filter={
            '_id': user_id
        })
        raise HTTPException(status_code=400, detail="Couldn\'t create an account")
    
    return temp

@router.post("/login/",response_model=Udisplay, status_code=status.HTTP_201_CREATED)
async def login(user:LoginUser, db=Depends(get_db)):
    users_collection = get_user_collection()
    userD = users_collection.find_one({"email": user.email, "password": user.password})
    print(userD)
    if userD:
        userD['user_id'] = str(userD['_id'])
        del userD['password']
        return Udisplay(**userD)
    raise HTTPException(status_code=401, detail="Invalid credentials")

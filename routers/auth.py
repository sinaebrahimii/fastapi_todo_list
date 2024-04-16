from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError

router=APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "xlntuzhvi3uqri9v3pbehinzk36oljp3"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]


def authenticate_user(username: str, password: str,db):
    #cheks and valodate entered username and password
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,role:str, expires_delta: timedelta = timedelta):
    encode={'sub':username,'id':user_id,"user_role":role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('user_role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user")
        return {'username': username, 'id': user_id,'user_role':user_role}
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user")
class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
@router.get("/users")
async def get_users(db:db_dependency):
    users=db.query(Users).all()
    return users


@router.post("/users",status_code=status.HTTP_201_CREATED)
async def create_users(db:db_dependency,create_user_request:CreateUserRequest):
    #creates a user and hashes the password
    create_user_model=Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True )
    db.add(create_user_model)
    db.commit()
    return create_user_model
@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:db_dependency):
    #uf user and pass is ok returns user or else returns false
    user= authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user")
    token = create_access_token(user.username,user.id,user.role,expires_delta=timedelta(minutes=20))
    return  {"access_token":token,"token_type":"bearer"}
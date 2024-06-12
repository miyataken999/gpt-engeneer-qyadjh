from fastapi import APIRouter, HTTPException
from api.app.models import User
from api.app.schemas import UserSchema

router = APIRouter()

@router.post("/register")
async def register_user(user: UserSchema):
    # check if username already exists
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id)
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

@router.post("/login")
async def login_user(username: str, password: str):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        return {"message": "Logged in successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
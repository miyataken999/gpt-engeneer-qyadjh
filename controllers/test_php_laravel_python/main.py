from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Team, Tag, UserTag

app = FastAPI()

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

@app.post("/register")
async def register_user(username: str, password: str):
    session = Session()
    if session.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return JSONResponse(status_code=201, content={"message": "User created successfully"})

@app.post("/login")
async def login(username: str, password: str):
    session = Session()
    user = session.query(User).filter_by(username=username, password=password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return JSONResponse(status_code=200, content={"message": "Logged in successfully"})

@app.get("/teams")
async def get_teams():
    session = Session()
    teams = session.query(Team).order_by(Team.created_at.desc()).all()
    return JSONResponse(status_code=200, content=[{"id": team.id, "name": team.name} for team in teams])

@app.post("/teams")
async def create_team(name: str):
    session = Session()
    team = Team(name=name)
    session.add(team)
    session.commit()
    return JSONResponse(status_code=201, content={"message": "Team created successfully"})

@app.get("/users")
async def get_users():
    session = Session()
    users = session.query(User).order_by(User.id.desc()).all()
    return JSONResponse(status_code=200, content=[{"id": user.id, "username": user.username, "profile": user.profile} for user in users])

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(status_code=200, content={"username": user.username, "profile": user.profile, "tags": [tag.name for tag in user.tags]})

@app.put("/users/{user_id}")
async def update_user(user_id: int, profile: str, team_id: int, tags: List[str]):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.profile = profile
    user.team_id = team_id
    user.tags = [session.query(Tag).filter_by(name=tag).first() for tag in tags]
    session.commit()
    return JSONResponse(status_code=200, content={"message": "User updated successfully"})
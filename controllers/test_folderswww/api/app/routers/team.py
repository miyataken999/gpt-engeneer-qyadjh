from fastapi import APIRouter
from api.app.models import Team
from api.app.schemas import TeamSchema

router = APIRouter()

@router.post("/teams")
async def create_team(team: TeamSchema):
    new_team = Team(name=team.name)
    session.add(new_team)
    session.commit()
    return {"message": "Team created successfully"}
from fastapi import APIRouter



actos = APIRouter()


@actos.get("/actos")
def getActos():
    return {"mensaje":"Hola Actos"}
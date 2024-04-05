from fastapi import APIRouter
from db.db import conn

indice = APIRouter()


@indice.get("/indice")
async def getIndice():
    with conn.cursor() as mycursor:
        mycursor.execute("select * from valores_usuales")
        rst = mycursor.fetchall()
    
    # conn.close()
    return rst
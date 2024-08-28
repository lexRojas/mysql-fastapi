from fastapi import APIRouter
from db.db import conn

user = APIRouter()

@user.get("/user")
async def geActos(idlogin = ""):
      with conn.cursor(dictionary=True) as cursor:
        # Read a single record
        if (idlogin==""):
          return None
        else:
          sql = "select * from usuario where login ='"+ str(idlogin)+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return(result)
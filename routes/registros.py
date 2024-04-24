from fastapi import APIRouter
from db.db import conn
registros = APIRouter();

@registros.get("/registros")
async def getRegistros():
      with conn.cursor(dictionary=True) as cursor:
        # Read a single record
        sql = "SELECT * FROM registro;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return( result)
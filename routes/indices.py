from fastapi import APIRouter
from db.db import conn
from datetime import date


indice = APIRouter()


@indice.get("/indice")
async def getIndice(version = 0):
    with conn.cursor(dictionary=True) as mycursor:
        mycursor.execute("select SQL_NO_CACHE * from valores_usuales")
        rst = mycursor.fetchall()
    
    # conn.close()
    return rst


@indice.get("/indice_by_dates")
async def getIndiceByDates(fecha_inicio:date=None, fecha_final:date=None, version= int):
    with conn.cursor(dictionary=True) as mycursor:

        sql = "select SQL_NO_CACHE *, %s from valores_usuales where fecha between %s and %s"
        params= [
                version,
                fecha_inicio, 
                fecha_final
        ]
        mycursor.execute(sql,params)
        rst = mycursor.fetchall()
    
    # conn.close()
    return rst
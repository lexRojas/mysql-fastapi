import uvicorn


if __name__== "__main__":
    uvicorn.run("api:app", reload=True,host='0.0.0.0', port=8000)
    # uvicorn.run("api:app", reload=True, port=8000)

# from sqlalchemy.orm import Session

# def obtener_registros(session: Session):
#     return session.query(TuModelo).order_by(TuModelo.fecha_actualizacion.desc()).all()

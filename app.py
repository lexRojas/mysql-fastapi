from fastapi import FastAPI
from routes.indices import indice


app = FastAPI()



@app.get("/")
def root():
    return {"mensaje":"hola a Rodrigo"}



app.include_router(indice)
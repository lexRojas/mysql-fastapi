from fastapi import FastAPI
from routes.indices import indice
from routes.actos   import actos


app = FastAPI()



@app.get("/")
def root():
    return {"mensaje":"hola a Rodrigo"}



app.include_router(indice)
app.include_router(actos)
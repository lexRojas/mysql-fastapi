from fastapi import FastAPI
from routes.indices import indice
from routes.actos   import actos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ['http://localhost:3000', 'https://lexnotario.netlify.app']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)






@app.get("/")
def root():
    return {"mensaje":"mysql-fastapi"}

app.include_router(indice)
app.include_router(actos)
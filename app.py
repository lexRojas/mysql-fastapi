from fastapi import FastAPI
# from routes.indices import indice
# from routes.actos   import actos
# from routes.registros import registros
# from routes.getMonto import calculadora
# from routes.users import user
import  db.database 
import  db.models 


from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()


origins = ['*','http://localhost:3000', 'https://lexnotario.netlify.app']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)






@app.get("/")
def root():
    return {"mensaje":"mysql-fastapi ver 11-09-2024-18:39"}

# app.include_router(indice)
# app.include_router(actos)
# app.include_router(registros)
# app.include_router(calculadora)
# app.include_router(user)

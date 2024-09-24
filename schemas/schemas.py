from pydantic import BaseModel


# Modelo de Pydantic para la creación de usuarios
class UserCreate(BaseModel):
    name: str
    email: str  




# Modelo para crear indices 
class ValoresUsualesCreate(BaseModel):
    folio_1: int  
    pag_1: str
    folio_2: int
    pag_2: str
    fecha: str
    escritura: int
    tomo: int
    partes: str
    hora: int
    minutos: int
    contrato: str
    entero: str
    firmas: int
    lugar: str
    
class RegistroCreate(BaseModel):
    registro_descripcion: str
    

class ActoCreate(BaseModel):
    acto_descripcion : str
    porcentaje_tarifa : float
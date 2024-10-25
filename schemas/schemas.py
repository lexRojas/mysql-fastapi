from pydantic import BaseModel
from typing import Optional
from datetime import date

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
    tomo_registro: int
    asiento: int

class ValoresUsualesUpdate(BaseModel):
    folio_1: Optional[int] = None
    pag_1: Optional[str]= None
    folio_2: Optional[int]= None
    pag_2: Optional[str]= None
    fecha: Optional[date]= None
    escritura: Optional[int]= None
    tomo: Optional[int]= None
    partes: Optional[str]= None
    hora: Optional[int]= None
    minutos: Optional[int]= None
    contrato: Optional[str]= None
    entero: Optional[str]= None
    firmas: Optional[int]= None
    lugar: Optional[str]= None
    tomo_registro: Optional[int] = None
    asiento: Optional[int] = None


class RegistroCreate(BaseModel):
    registro_descripcion: str
    

class ActoCreate(BaseModel):
    acto_descripcion : str
    porcentaje_tarifa : float
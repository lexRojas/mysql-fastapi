import json
from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.future import select
from sqlalchemy import desc, and_,or_

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from models.models import User, ValoresUsuales,Registro ,Timbre, Tarifario, Acto,Base, RegistroActo, RangoTimbre, Honorarios, Variables, Usuario
from schemas.schemas import UserCreate,ValoresUsualesCreate, RegistroCreate, ActoCreate , ValoresUsualesUpdate


def print_row(row):
    result_dict = {column.name: getattr(row, column.name) for column in row.__table__.columns}
    result_json = json.dumps(result_dict)
    print(result_json)




# Configuración de la base de datos MySQL asíncrona usando mysql+asyncmy
# DATABASE_URL = "mysql+asyncmy://rorojas1:C0c*l0c4@18.221.154.102:3306/notario"
DATABASE_URL="mysql+asyncmy://admin:RcKrNVUC@mysql-187830-0.cloudclusters.net:10072/notario"
# Crear el motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión asíncrona
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta en el startup
    print("Aplicación iniciada")
    async with engine.begin() as conn:
        # Crear las tablas si no existen
        await conn.run_sync(Base.metadata.create_all)
    
    # Aquí se podrían inicializar conexiones, recursos, etc.
    yield  # Espera que la aplicación esté funcionando
    
    # Código que se ejecuta en el shutdown
    print("Aplicación cerrada")
    # Aquí se podrían cerrar conexiones, limpiar recursos, etc.

# Crear la aplicación FastAPI
app = FastAPI(lifespan=lifespan)


# Defino el CORS para acceso desde mi app netlify 
origins = ['*','http://localhost:3000', 'https://lexnotario.netlify.app']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



# Dependencia para obtener la sesión de la base de datos
async def get_db():
    async with async_session() as session:
        yield session


#Ruta Raiz 
@app.get("/")
async def root():
    miRoot = {
        "version":"1.0",
        "detalle":"usa SQLAlchemy and CORS"
        }
    return miRoot


# Ruta para crear un nuevo usuario
@app.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Ruta para obtener todos los usuarios
@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.get("/users_login")
async def getUser(idlogin = None, db: AsyncSession = Depends(get_db)):
    if(idlogin):
        stmt = select(Usuario).where(Usuario.login == idlogin)
        rows = await db.execute(stmt)
        result = rows.scalar()
        valores = result
    else:
        valores = None
    return(valores)

#Ruta para crear un registro en el indice
@app.post("/indice/")
async def create_valores_usuales(indice:ValoresUsualesCreate, db: AsyncSession = Depends(get_db)):
    db_indice = ValoresUsuales( 
        lugar       = indice.lugar,
        folio_1     = indice.folio_1,
        pag_1       = indice.pag_1,
        folio_2     = indice.folio_2,
        pag_2       = indice.pag_2,
        fecha       = indice.fecha,
        escritura   = indice.escritura,
        tomo        = indice.tomo,
        partes      = indice.partes,  
        hora        = indice.hora,
        minutos     = indice.minutos,
        contrato    = indice.contrato,
        entero      = indice.entero,
        firmas      = indice.firmas,
        tomo_registro = indice.tomo_registro,
        asiento = indice.asiento
    )
    
    db.add(db_indice)
    await db.commit()
    await db.refresh(db_indice)
    return db_indice
    

@app.patch("/indice/")
async def update_valores_usuales(id: int, valores_update: ValoresUsualesUpdate, session: AsyncSession = Depends(get_db)):
    # Buscar el registro por ID
    result = await session.execute(select(ValoresUsuales).filter_by(id=id))
    valor_usual = result.scalars().first()

    if not valor_usual:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Actualizar solo los campos proporcionados en el PATCH
    for key, value in valores_update.model_dump(exclude_unset=True).items():
        setattr(valor_usual, key, value)
    
    # Guardar los cambios
    await session.commit()

    return {"message": "Registro actualizado exitosamente", "data": valores_update}

# Ruta para obtener todos los indices
@app.get("/indice/")
async def read_valores_usuales(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ValoresUsuales).order_by(desc(ValoresUsuales.escritura)))
    valores = result.scalars().all()
    return valores



# Ruta para borrar un indice x
@app.delete("/indice/{id}")
async def delete_valores_usuales(id: int,  session: AsyncSession = Depends(get_db)):
    # Buscar el registro en la base de datos
    result = await session.execute(select(ValoresUsuales).where(ValoresUsuales.id == id))
    registro = result.scalars().first()

    if registro is None:
        # Si no se encuentra, levantar una excepción
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Eliminar el registro
    await session.delete(registro)
    await session.commit()

    return {"message": "Registro eliminado"}


#Ruta para obtener los indices por fecha 
@app.get("/indice_by_dates")
async def getIndiceByDates(fecha_inicio:date=None, fecha_final:date=None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ValoresUsuales).where(ValoresUsuales.fecha.between(fecha_inicio, fecha_final)).order_by(ValoresUsuales.escritura))
    rows = result.fetchall()
    data = [dict(row._mapping) for row in rows]
    return data  # FastAPI lo convierte automáticamente a JSON


#Ruta para obtener los indices por fecha 
@app.get("/indice_by_citas")
async def getIndiceByCitas(escritura:int=0, tomo:int=0, asiento:int=0, db: AsyncSession = Depends(get_db)):


    # Crear una lista de condiciones dinámicamente
    condiciones = []

    if escritura > 0:
        condiciones.append(ValoresUsuales.escritura == escritura)
    if tomo > 0:
        condiciones.append(ValoresUsuales.tomo_registro == tomo)
    if asiento > 0:
        condiciones.append(ValoresUsuales.asiento == asiento)



    result = await db.execute(select(ValoresUsuales).where(and_(*condiciones)).order_by(ValoresUsuales.escritura))

    
        
    
    
    rows = result.fetchall()
    data = [dict(row._mapping) for row in rows]
    return data  # FastAPI lo convierte automáticamente a JSON



# Ruta que obtiene los registros 
@app.get("/registros")
async def getRegistros(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Registro).order_by(Registro.registro_descripcion))
    valores = result.scalars().all()
    return valores

#Ruta para crear un registro en el indice
@app.post("/registro/")
async def create_valores_usuales(registro:RegistroCreate, db: AsyncSession = Depends(get_db)):
    db_registro = Registro( 
        registro_descripcion = registro.registro_descripcion
    )
    
    db.add(db_registro)
    await db.commit()
    await db.refresh(db_registro)
    return db_registro
    
    
@app.get("/actos")
async def geActos(idRegistro = None, db: AsyncSession = Depends(get_db)):
    if (idRegistro):
        
        stmt = select(Acto).join(Acto.registros_x_acto).where(RegistroActo.registro_id_registro==idRegistro).order_by(Acto.acto_descripcion)
        
        rows = await db.execute(stmt)
        result = rows.scalars().all()
        valores = result
        
        
    else:
        valores =[]
    return(valores)

#Ruta de calculos notariales 

@app.get("/get_monto")
async def get_monto(id_acto = None, monto=0, db: AsyncSession = Depends(get_db)):

    #defino las variables donde voy a guardar la informacion para el calculo 
    
    json_tarifas={}
    detalle_tarifas = []
    total_honorarios = 0

    monto = float(monto)


    if (id_acto): #si el usuario mando un acto 
        
        stmt = select(Timbre).options(selectinload(Timbre.tarifas)).join(Timbre.tarifas).where(Tarifario.acto_id_acto==id_acto).order_by(Timbre.id_timbre)
        rst = await db.execute(stmt)
        row_timbre = rst.scalars().all()
        
        tarifario = {
            'tarifa':0,
            'honorarios':0,
            'total_tarifas':0
        }

        print('recorro la tabla de timbres....')
        for row in row_timbre:
            id_timbre = row.id_timbre
            timbre_descripcion = row.timbre_descripcion
            factor= str(row.factor)
            valor= float(row.valor)
            multiplo= float(row.multiplo)
            minimo= float(row.minimo)
            porcentaje = float(row.tarifas.porcentaje)
            timbre_id_rango_timbre = row.timbre_id_rango_timbre

            tarifa=0
            
#TIMBRE DEFINIDO POR MULTIPLO
            if (factor =='M'):
                
                tarifa = (monto / valor) * multiplo
                tarifa = tarifa  * porcentaje
                if (tarifa < minimo): 
                    tarifa = minimo
                #end if    
            #end if

#TIMBRE DEFINIDO POR VALOR ABSOLUTO
            if (factor =='A'):
                tarifa = valor
                tarifa = tarifa  * porcentaje
            #end if

#TIMBRE DEFINIDO POR PORCENTAJE

            if (factor=='P'):
                tarifa = monto * valor
                tarifa = tarifa  * porcentaje
                if (tarifa < minimo): 
                    tarifa = minimo
                #end if
            #end if
# TIMBRE DEFINIDO POR RANGO
    
            if (factor =='R'):
                print('INGRESO A LOS RANGOS....')
                stmt1 = select(RangoTimbre).where(RangoTimbre.id_rango_timbre == timbre_id_rango_timbre)
                rst1 = await db.execute(stmt1)
                row_rangos_1 = rst1.scalars().all()
                
# RECORRO LOS DISTINTOS RANGOS QUE APLICAN 
                for fila in row_rangos_1:   
                    rango_minimo = fila.minimo
                    rango_maximo = fila.maximo
                    rango_valor = fila.valor 
                    
                    if((monto > rango_minimo) and (monto <= rango_maximo)): 
                        tarifa  = rango_valor
                        tarifa =  tarifa * porcentaje
                    #end if
                #end for - rangos
            #end if 

            json_tarifas['id'] = id_timbre
            json_tarifas['descripcion'] = timbre_descripcion
            json_tarifas['tarifa'] = tarifa

    

            detalle_tarifas.append(json_tarifas.copy()) 

            json_tarifas = {}  # Crea un nuevo diccionario en cada iteración


            total_honorarios+=tarifa

        print('Termino recorrido la tabla de timbres....')
#OBTENGO EL COSTO POR HONORARIOS 

        stmt = select(Honorarios).order_by(Honorarios.id_honorario)
        rst = await db.execute(stmt)
        row_honorarios = rst.scalars().all()
        
        honorarios=0
        print('Recorro la tabla de honorarios....')
        for honorario in row_honorarios:
            minimo_honorarios = honorario.minimo
            maximo_honorarios = honorario.maximo
            porcentaje_honorarios = honorario.porcentaje

            if (monto > minimo_honorarios): 
                if (monto <= maximo_honorarios): 
                    honorarios  = (monto - minimo_honorarios) * porcentaje_honorarios + honorarios
                else:
                    honorarios = (maximo_honorarios - minimo_honorarios) * porcentaje_honorarios + honorarios
                #end if
            #end if
        
        print('Termino recorrido la tabla de honorarios....')
# OBTENGO EL VALOR MINIMO HONORARIOS Y SI ES SUPERIOR AL VALOR ACTUAL, SE SUSTITUYE

        stmt = select(Variables.valor).where(Variables.id==2)
        minimo_honorarios = await db.scalar(stmt)
        
        if (honorarios<minimo_honorarios):
            honorarios= minimo_honorarios

        json_tarifas['id'] = '+'
        json_tarifas['descripcion'] = 'Honorarios'
        json_tarifas['tarifa'] = honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 
        
        json_tarifas = {}  # Crea un nuevo diccionario en cada iteración
        
        total_honorarios+=honorarios

# OBTENGO EL VALOR DEL IVA 

        print('Saco IVA ....')
        stmt = select(Variables.valor).where(Variables.id==1)
        iva = await db.scalar(stmt)

        iva_honorarios = honorarios*iva

        json_tarifas['id'] = '++'
        json_tarifas['descripcion'] = 'IVA Honorarios'
        json_tarifas['tarifa'] = iva_honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 

        json_tarifas = {}  # Crea un nuevo diccionario en cada iteración
        
        print('Guardo IVA ....')
        total_honorarios+=iva_honorarios

        json_tarifas['id'] = '+++'
        json_tarifas['descripcion'] = 'Total Honorarios + timbres'
        json_tarifas['tarifa'] = total_honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 
        
        json_tarifas = {}  # Crea un nuevo diccionario en cada iteración

    return(detalle_tarifas)




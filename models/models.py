from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Mapped
from sqlalchemy import Column, Integer, String, BigInteger, Date, Double,  Float, ForeignKey , func


# Modelo base de SQLAlchemy
Base = declarative_base()

# Definir un modelo SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    
        
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    login = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    perfil = Column(String(30), nullable=False)
    

class ValoresUsuales(Base):
    __tablename__ = "valores_usuales"
    id        = Column(BigInteger,primary_key=True, index=True, autoincrement= "auto") 
    folio_1   = Column(Integer, default= 0)
    pag_1     = Column(String(100), default="")
    folio_2   = Column(Integer, default= 0)
    pag_2     = Column(String(100), default="")
    fecha     = Column(Date, server_default=func.current_date())
    escritura = Column(Integer, default= 0)
    tomo      = Column(Integer, default= 0)
    partes    = Column(String(200), default="") 
    hora      = Column(Integer, default= 0) 
    minutos   = Column(Integer, default= 0)
    contrato  = Column(String(100), default="")
    entero    = Column(String(100), default="")
    firmas    = Column(Integer, default= 0)
    lugar     = Column(String(100), default="", index=True )
    tomo_registro      = Column(Integer, default = 0)
    asiento   = Column(Integer, default = 0)

class Registro(Base):
    __tablename__="registro"
    id_registro = Column(Integer,primary_key=True, index=True, autoincrement= "auto") 
    registro_descripcion = Column(String(100))
    
    # Relaciones opcionales, si quieres acceder a los registros relacionados
    actos_x_registro: Mapped["RegistroActo"] = relationship(back_populates="registro")
    

class Acto(Base):
    __tablename__="acto"
    id_acto = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    acto_descripcion = Column(String(100))
    porcentaje_tarifa = Column(Float)
    
    # Relaciones opcionales, si quieres acceder a los registros relacionados
    registros_x_acto: Mapped["RegistroActo"] = relationship(back_populates="acto")
    tarifas : Mapped["Tarifario"] = relationship(back_populates="acto")

    
class RegistroActo(Base):
    __tablename__ = 'registro_acto'
    
    registro_id_registro = Column(Integer, ForeignKey('registro.id_registro', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    acto_id_acto = Column(Integer, ForeignKey('acto.id_acto', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # Relaciones opcionales, si quieres acceder a los registros relacionados
    registro: Mapped["Registro"] = relationship(back_populates="actos_x_registro")
    acto: Mapped["Acto"]   =  relationship( back_populates="registros_x_acto")
    
    
class Timbre(Base):
    __tablename__ = 'timbre'

    id_timbre = Column(Integer, primary_key=True, autoincrement=True)
    timbre_descripcion = Column(String(100), nullable=True)
    factor = Column(String(3), nullable=True)
    minimo = Column(Double, nullable=True)
    multiplo = Column(Double, nullable=True)
    valor = Column(Double, nullable=True)
    codigo = Column(Integer, nullable=False)
    timbre_id_rango_timbre = Column(Integer, ForeignKey('rango_timbre.id'), nullable=True)
    
    # Relaciones opcionales, si quieres acceder a los registros relacionados
    tarifas: Mapped["Tarifario"] = relationship(back_populates="timbres")
    
    

class Tarifario(Base):
    __tablename__ = 'tarifario'

    id_tarifa = Column(Integer, primary_key=True, autoincrement=True)
    acto_id_acto = Column(Integer, ForeignKey('acto.id_acto', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    timbre_id_timbre = Column(Integer, ForeignKey('timbre.id_timbre', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    porcentaje = Column(Double, nullable=False, default=1.0)
    
    # Relaciones opcionales para conectar con las tablas referenciadas
    acto : Mapped["Acto"] = relationship(back_populates="tarifas")
    timbres: Mapped["Timbre"] = relationship(back_populates="tarifas")
    
class RangoTimbre(Base):
    __tablename__ = 'rango_timbre'
    
    key_id = Column(Integer, primary_key=True, autoincrement=True)
    id_rango_timbre = Column(Integer, primary_key=True, nullable=False)
    minimo = Column(Float, nullable=True)
    maximo = Column(Float, nullable=True)
    valor = Column(Float, nullable=True)
    

class Honorarios(Base):
    __tablename__ = 'honorarios'

    id_honorario = Column(Integer, primary_key=True, autoincrement=True)
    minimo = Column(Double, nullable=True)
    maximo = Column(Double, nullable=True)
    porcentaje = Column(Double, nullable=True)
    

class Variables(Base):
    __tablename__ = 'variables'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(45), nullable=True)
    valor = Column(Float, nullable=True)
    
    

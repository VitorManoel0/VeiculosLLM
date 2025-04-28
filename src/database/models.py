from sqlalchemy import Column, Integer, String, Float, Date

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    motor = Column(String, nullable=False)
    combustivel = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    quilometragem = Column(Integer, nullable=False)
    portas = Column(Integer, nullable=False)
    cambio = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)

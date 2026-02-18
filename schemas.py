from pydantic import BaseModel

class IncidenciaBase(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    estado: str

class IncidenciaCreate(IncidenciaBase):
    pass

class IncidenciaOut(IncidenciaBase):
    id: int

    class Config:
        from_attributes = True

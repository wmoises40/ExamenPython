from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Incidencia
from schemas import IncidenciaCreate, IncidenciaOut
from auth import authenticate_user, create_access_token, get_current_user

from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="API Incidencias - FastAPI + MySQL + JWT")

Base.metadata.create_all(bind=engine)

@app.get("/incidencias", response_model=list[IncidenciaOut])
def listar_incidencias(db: Session = Depends(get_db)):
    incidencias = db.query(Incidencia).all()
    return incidencias


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"usuario_autenticado": username}


@app.post("/incidencias", response_model=IncidenciaOut)
def crear_incidencia(
    incidencia: IncidenciaCreate,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    nueva = Incidencia(
        titulo=incidencia.titulo,
        descripcion=incidencia.descripcion,
        prioridad=incidencia.prioridad,
        estado=incidencia.estado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.models.entities import Professional, Service, User
from app.routers import appointments

app = FastAPI(title="Barbearia Code", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)


def seed_data() -> None:
    db = SessionLocal()
    try:
        # Cada grupo é verificado separadamente; os dados existentes nunca são apagados.
        if not db.query(User).first():
            db.add(User(name="Cliente de teste", email="cliente@teste.com", phone="(00) 00000-0000"))
        if not db.query(Professional).first():
            db.add_all([Professional(name="Carlos", specialty="Cabelo e Barba"), Professional(name="Manoel", specialty="Estilo e Degradê")])
        if not db.query(Service).first():
            db.add_all([Service(name="Corte Simples", duration_minutes=30, price=35), Service(name="Barba Completa", duration_minutes=30, price=30), Service(name="Combo Cabelo e Barba", duration_minutes=60, price=60)])
        db.commit()
    finally:
        db.close()


seed_data()
app.include_router(appointments.router)
app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend", html=True), name="frontend")

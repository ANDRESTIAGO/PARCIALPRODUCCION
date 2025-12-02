from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.conection import Session as DBSession, engine, Base
from app.models.products import User, Product, Category
from fastapi.middleware.cors import CORSMiddleware

# Incluir los routers
from app.api.routers.users import router as users_router
from app.api.routers.products import router as products_router
from app.api.routers.categories import router as categories_router


app = FastAPI(
    title="Proyecto FastAPI",
    description="API para la gestión de productos y usuarios",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # tu React local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


app.include_router(users_router)
app.include_router(products_router)
app.include_router(categories_router)

# Dependencia para obtener sesión de la base de datos
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de gestión de productos y usuarios"}

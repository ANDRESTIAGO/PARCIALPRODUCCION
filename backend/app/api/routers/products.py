from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from app.database.conection import Session as DBSession
from app.models.products import Product
from app.schemas.tienda  import Product as ProductSchema, ProductCreate
from datetime import datetime

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Dependencia para obtener sesión de la base de datos
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        created_at=datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, new_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in new_data.__dict__.items():
        if key != "_sa_instance_state":
            setattr(product, key, value)
    db.commit()
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)): 
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product)
    db.commit()
    return {"ok": True}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.conection import Session as DBSession
from app.models.products import Category
from app.schemas.tienda import Category as CategorySchema, CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(category_id: int, new_data: CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in new_data.dict().items():
        setattr(category, key, value)
    db.commit()
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(category)
    db.commit()
    return {"ok": True}

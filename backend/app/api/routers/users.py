from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.conection import Session as DBSession
from app.models.products import User
from app.schemas.tienda import User as UserSchema, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, new_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in new_data.dict().items():
        setattr(user, key, value)
    db.commit()
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"ok": True}

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put('/profile/id/')
async def put_profile_id(id: int, name: Annotated[str, Query(max_length=100)], address: Annotated[str, Query(max_length=100)], mobile: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], email: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.put_profile_id(db, id, name, address, mobile, password, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/profile/id')
async def delete_profile_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_profile_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/')
async def get_users(db: Session = Depends(get_db)):
    try:
        return await service.get_users(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/id')
async def get_users_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_users_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/id/')
async def put_users_id(id: int, username: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], test: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.put_users_id(db, id, username, password, test)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/id')
async def delete_users_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_users_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/profile/')
async def get_profile(db: Session = Depends(get_db)):
    try:
        return await service.get_profile(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/profile/id')
async def get_profile_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_profile_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(username: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], test: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_users(db, username, password, test)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/user/records')
async def post_user_records(username: Annotated[str, Query(max_length=100)], address: Annotated[str, Query(max_length=100)], headers: Request, db: Session = Depends(get_db)):
    try:
        return await service.post_user_records(db, username, address, headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/login')
async def post_login(email: Annotated[str, Query(max_length=100, pattern='[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}')], password: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_login(db, email, password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/user/delete')
async def delete_user_delete(username: Annotated[str, Query(max_length=100)], address: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.delete_user_delete(db, username, address)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/profile/')
async def post_profile(name: Annotated[str, Query(max_length=100)], address: Annotated[str, Query(max_length=100)], mobile: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], email: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_profile(db, name, address, mobile, password, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


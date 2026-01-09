from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.url import URL, URLCreate, URLAnalytics, URLUpdate
from app.crud.url import (
    create_url, get_user_urls, get_url_by_short_code,
    update_url, delete_url, increment_url_clicks
)
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=URL)
def create_short_url(
    url: URLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if url.custom_code:
        existing_url = get_url_by_short_code(db, url.custom_code)
        if existing_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom code already exists"
            )
    
    db_url = create_url(db, url, current_user.id)
    return db_url


@router.get("/", response_model=List[URL])
def read_user_urls(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    urls = get_user_urls(db, current_user.id, skip=skip, limit=limit)
    return urls


@router.get("/{short_code}", response_model=URLAnalytics)
def get_url_info(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_url = get_url_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    if db_url.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return db_url


@router.put("/{url_id}", response_model=URL)
def update_url_info(
    url_id: int,
    url_update: URLUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    if db_url.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return update_url(db, url_id, url_update)


@router.delete("/{url_id}")
def delete_short_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    if db_url.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    delete_url(db, url_id)
    return {"message": "URL deleted successfully"}


@router.get("/{short_code}/redirect")
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db)
):
    db_url = get_url_by_short_code(db, short_code)
    if not db_url or not db_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found or inactive"
        )
    
    increment_url_clicks(db, db_url.id)
    
    return {"redirect_url": db_url.original_url}

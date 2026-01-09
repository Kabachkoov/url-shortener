from sqlalchemy.orm import Session
from datetime import datetime
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate
from app.utils.shortener import generate_short_code


def get_url_by_short_code(db: Session, short_code: str):
    return db.query(URL).filter(URL.short_code == short_code).first()


def get_user_urls(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(URL)\
        .filter(URL.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_all_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(URL).offset(skip).limit(limit).all()


def create_url(db: Session, url: URLCreate, user_id: int = None):
    if url.custom_code:
        short_code = url.custom_code
    else:
        short_code = generate_short_code()
    
    db_url = URL(
        original_url=str(url.original_url),
        short_code=short_code,
        user_id=user_id
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def update_url(db: Session, url_id: int, url_update: URLUpdate):
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if not db_url:
        return None
    
    for field, value in url_update.model_dump(exclude_unset=True).items():
        setattr(db_url, field, value)
    
    db.commit()
    db.refresh(db_url)
    return db_url


def increment_url_clicks(db: Session, url_id: int):
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if db_url:
        db_url.clicks += 1
        db_url.last_accessed = datetime.utcnow()
        db.commit()
        db.refresh(db_url)
    return db_url


def delete_url(db: Session, url_id: int):
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if db_url:
        db.delete(db_url)
        db.commit()
    return db_url


def get_inactive_urls(db: Session, days_inactive: int = 30):
    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days_inactive)
    
    return db.query(URL).filter(
        URL.last_accessed < cutoff_date,
        URL.is_active == True
    ).all()

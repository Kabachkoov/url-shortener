from celery import Celery
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import settings
from app.crud.url import get_inactive_urls, delete_url
from datetime import datetime, timedelta

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.beat_schedule = {
    'cleanup-inactive-urls-daily': {
        'task': 'app.tasks.cleanup.cleanup_inactive_urls',
        'schedule': timedelta(days=1),
    },
}


@celery_app.task
def cleanup_inactive_urls(days_inactive: int = 30):
    """Удаляет ссылки, которые не использовались более указанного количества дней"""
    db: Session = SessionLocal()
    try:
        inactive_urls = get_inactive_urls(db, days_inactive)
        deleted_count = 0
        
        for url in inactive_urls:
            delete_url(db, url.id)
            deleted_count += 1
        
        db.commit()
        return {"deleted_urls": deleted_count, "task": "cleanup_inactive_urls"}
    
    finally:
        db.close()


@celery_app.task
def deactivate_expired_urls(expiration_days: int = 365):
    """Деактивирует ссылки старше указанного количества дней"""
    db: Session = SessionLocal()
    try:
        from datetime import datetime, timedelta
        from app.models.url import URL
        
        cutoff_date = datetime.utcnow() - timedelta(days=expiration_days)
        
        expired_urls = db.query(URL).filter(
            URL.created_at < cutoff_date,
            URL.is_active == True
        ).all()
        
        deactivated_count = 0
        for url in expired_urls:
            url.is_active = False
            deactivated_count += 1
        
        db.commit()
        return {
            "deactivated_urls": deactivated_count,
            "task": "deactivate_expired_urls"
        }
    
    finally:
        db.close()

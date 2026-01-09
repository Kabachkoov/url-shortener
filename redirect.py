from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.url import get_url_by_short_code, increment_url_clicks

router = APIRouter()


@router.get("/{short_code}")
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    db_url = get_url_by_short_code(db, short_code)
    if not db_url or not db_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found or inactive"
        )
    
    increment_url_clicks(db, db_url.id)
    
    return RedirectResponse(url=db_url.original_url)

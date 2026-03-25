from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PhoneTI
from app.schemas import PhoneTIResponse

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/phones", response_model=list[PhoneTIResponse])
def get_phones(phone_number: str = Query(...), db: Session = Depends(get_db)):
    results = db.query(PhoneTI).filter(PhoneTI.phone_number == phone_number).all()
    if not results:
        raise HTTPException(status_code=404, detail="No records found")
    return results

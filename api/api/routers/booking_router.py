from fastapi import APIRouter, status, Depends
from core.multi_database_middleware import get_db_session
from sqlalchemy.orm import Session
from api.schemas.booking_schema import BookingSchema, BookingSpotSchema
from typing import List
from core.auth import logged_in_user
from api.repository.booking_transactions import create_booking, delete_booking, get_bookings

router = APIRouter(
    prefix="/booking",
    tags=['Booking']
)

@router.get('', status_code=status.HTTP_200_OK, response_model=List[BookingSpotSchema])
def get_booking_info(db: Session= Depends(get_db_session), user = Depends(logged_in_user)):   
    return get_bookings(db, user["id"])


@router.post('', status_code=status.HTTP_200_OK)
def create_Booking(request: BookingSchema, db: Session= Depends(get_db_session), user = Depends(logged_in_user)):   
    return create_booking(request, db, user["id"])
    

@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def cancel_Booking(id: int, db: Session= Depends(get_db_session), user = Depends(logged_in_user)):            
    return delete_booking(id, db, user["id"])
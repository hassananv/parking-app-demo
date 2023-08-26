from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session

from api.schemas.booking_schema import BookingSchema
from models.booking_model import BookingDatesModel
from models.spot_model import SpotModel




def delete_booking(id: int, db: Session, user_id):

    booking_query = db.query(BookingDatesModel).filter(BookingDatesModel.id==id)
    booking = booking_query.first()
    if ((not booking) or (booking.user_id != user_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to cancel booking.")

    booking_query.delete(synchronize_session=False)
    db.commit()      
    return 'Booking deleted.'


def get_bookings(db: Session, user_id):
    bookings = db.query(BookingDatesModel).filter(BookingDatesModel.user_id==user_id).all()
    return bookings



def create_booking(request: BookingSchema, db: Session, id):
    
    booking_request = request.dict()

    booking_request["user_id"] = id

    spot_id = booking_request["spot_id"]
    start_date = booking_request["start_date"]
    end_date = booking_request["end_date"]
    check_spot_available(spot_id, start_date, end_date, db)

    new_booking = BookingDatesModel(**booking_request)       
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking.id


def check_spot_available(id, start, end, db: Session):
    start_date = start.astimezone()
    end_date = end.astimezone()

    spot = db.query(SpotModel).filter(SpotModel.disabled==False, SpotModel.id==id).first()
    if not spot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Spot is not available.")

    booking_dates = spot.booking

    for booking_date in booking_dates:       

        if (
            (start_date >= booking_date.start_date and start_date < booking_date.end_date)
            or
            (end_date > booking_date.start_date and end_date <= booking_date.end_date)
            or
            (start_date <= booking_date.start_date and end_date >= booking_date.end_date)
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Spot is not available.")


        
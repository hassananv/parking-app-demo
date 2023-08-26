from sqlalchemy.orm.session import Session
from models.spot_model import SpotModel
from api.schemas.spot_schema import SpotSearchSchema
from api.schemas.booking_schema import BookingBase
from typing import List

def get_spots( db: Session):
    
    spots = db.query(SpotModel).filter( SpotModel.disabled==False).all()
    return spots


def search_available_spots(request: SpotSearchSchema, db: Session):
    
    start = request.start_date
    end = request.end_date
    start_date = start.astimezone()
    end_date = end.astimezone()

    spots = db.query(SpotModel).filter( SpotModel.disabled==False).all()

    for spot in spots:
        spot.available = check_spot_available(spot, start_date, end_date)

    return spots


def check_spot_available(spot, start_date, end_date):
   
    booking_dates: List[BookingBase] = spot.booking


    for booking_date in booking_dates:       

        if (
            (start_date >= booking_date.start_date and start_date < booking_date.end_date)
            or
            (end_date > booking_date.start_date and end_date <= booking_date.end_date)
            or
            (start_date <= booking_date.start_date and end_date >= booking_date.end_date)
        ):
            return False   

    return True
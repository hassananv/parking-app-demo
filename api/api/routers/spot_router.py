from fastapi import APIRouter, status, Depends
from core.multi_database_middleware import get_db_session
from sqlalchemy.orm import Session
from api.schemas.spot_schema import SpotSchema, SpotSearchSchema
from typing import List

from core.auth import logged_in_user
from api.repository.spot_transactions import get_spots, search_available_spots


router = APIRouter(
    prefix="/spot",
    tags=['Parking Spots']
)




@router.get('', status_code=status.HTTP_200_OK, response_model=List[SpotSchema])
def get_spots_info(db: Session= Depends(get_db_session), user = Depends(logged_in_user)):   
    return get_spots(db)


@router.post('', status_code=status.HTTP_200_OK, response_model=List[SpotSchema])
def search_Spots(request: SpotSearchSchema, db: Session= Depends(get_db_session), user = Depends(logged_in_user)):   
    return search_available_spots(request, db)
    
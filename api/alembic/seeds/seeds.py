 # data seed 
from datetime import datetime

def temp():
    spots = list()

    spots =  add_vehicle(spots,'Motorbike' , 10)
    spots =  add_vehicle(spots,'Car' , 20)
    spots =  add_vehicle(spots,'Truck' , 10)
        
    # op.bulk_insert(spot_table, spots)



def add_vehicle(spots, type, total):
    offset = len(spots)
    for i in range(1,total+1):
        spots.append({   
            'id':i+offset,
            'created_at': datetime.now(),
            'name': type[0]+str(i),
            'type':type,
            'disabled':False
        })
    return spots
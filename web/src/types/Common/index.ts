export interface parkingSpotInfoType {

    id: number;
    name: string;
    type: string;
    available?: boolean;
    booking?:bookingSearchInfoType[];

}

export interface bookingSearchInfoType {
    id?: string;    
    start_date: string;
    end_date: string;
    timezone: string; 
    license_plate:string; 
    spot?: parkingSpotInfoType;
}

export interface dateRangeInfoType {
    startDate: string;
    endDate: string;
}

export interface bookingStatesInfoType {    
    vehicleType: null | boolean;       
    spotNumber: null | boolean;
    endTime: null | boolean;
    startTime: null | boolean;
    date: null | boolean;
}





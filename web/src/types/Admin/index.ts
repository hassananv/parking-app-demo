export interface userInfoType {
    id?: number;    
    email: string;
    first_name: string;
    last_name: string;
    vehicle_type: string;
    license_plate: string;
    userName?: string;
    password?: string;
    old_password?: string;
}

export interface userCredentialsInfoType {
    email: string;
    password: string;
}

export interface vehicleTypeOptionsInfoType {
    text: string;
    value: string;
}

export interface userStatesInfoType {    
    email: null | boolean;  
    confirmEmail: null | boolean;            
    firstName: null | boolean;
    lastName: null | boolean;
    vehicleType: null | boolean;
    licensePlate: null | boolean;
    oldPassword: null | boolean;
    password: null | boolean;
    confirmPassword: null | boolean;
}

export interface loginStatesInfoType {
    email: null | boolean;
    password: null | boolean;
}
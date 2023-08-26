import { vehicleTypeOptionsInfoType } from "@/types/Admin";

export enum vehicleTypes {MOTORBIKE = 'Motorbike', CAR = 'Car', TRUCK = 'Truck'}

export const vehicleTypeOptions: vehicleTypeOptionsInfoType[] = [
    {text: 'Motorbike',    value: vehicleTypes.MOTORBIKE}, 
    {text: 'Car',          value: vehicleTypes.CAR},
    {text: 'Truck',        value: vehicleTypes.TRUCK}
]
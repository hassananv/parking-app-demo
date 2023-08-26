<template>
    <b-card class="bg-white border-white">           

        <loading-spinner color="#000" v-if="searching" waitingText="Loading Results ..." />
        
        <div v-else> 

            <b-card no-body border-variant="white" bg-variant="white" v-if="!parkingSpots.length">
                <span class="text-muted ml-4 mb-5">No records found.</span>
            </b-card> 
                 

            <b-card v-else class="home-content border-white p-0">
                <b-table
                    :items="getParkingSpots"
                    :fields="parkingSpotFields"
                    class="border-info"
                    sort-by="available"
                    sort-desc
                    sort-icon-left                                    
                    small
                    responsive="sm"> 

                    <template v-slot:cell(available)="data" > 
                        <span class="p-1 bg-danger text-white rounded" v-if="!data.value">Occupied</span>
                        <span class="p-1 bg-success text-white rounded" v-else>Available</span>                     
                    </template> 

                    <template v-slot:cell(nextAvailable)="data" > 
                        <div style="white-space: pre;" v-if="data.item.booking.length>0 && !data.item.available">{{getNextAvailable(data.item.booking)| beautify-date-next-available}}</div>                                     
                    </template>

                    <template v-slot:cell(edit)="data" >
                        <div>
                            <b-button style="font-size:12px" 
                                size="sm" 
                                :disabled="!data.item.available"
                                @click="bookParkingSpot(data.item);"
                                class="text-primary bg-info border-info mt-0 px-3" 
                                ><b>Book</b>
                            </b-button>                            
                        </div>                        
                    </template>
                    
                </b-table>

            
            </b-card>
        </div>

        <b-modal body-class="py-0" size="xl" v-model="showBookingWindow" header-class="bg-primary text-white" >
            <template v-slot:modal-title>
                <h1 class="my-2 ml-2">Parking Spot Reservation Request</h1> 
            </template>

            <b-card v-if="parkingSpotDataReady" class="border-white text-dark bg-white" body-class="py-0" :key="updatedBookingInfo"> 
                <b-row class="ml-auto mt-2 h2">
                    Your requested reservation details: 
                </b-row>
                <b-row class="mt-n2 h4">
                    <b-col class="text-primary">Spot Number</b-col>
                    <b-col>{{parkingSpot.name}}</b-col>
                </b-row>
                <b-row class="mt-n3 h4">
                    <b-col class="text-primary">Spot Type</b-col>
                    <b-col>{{parkingSpot.type}}</b-col>
                </b-row>
                <b-row class="mt-n3 h4">
                    <b-col class="text-primary">From</b-col>
                    <b-col>
                        <div>{{booking['date'].startDate | beautify-date-weekday-time}}</div>                     
                    </b-col>
                </b-row>
                <b-row class="mt-n3 h4">
                    <b-col class="text-primary">To</b-col>
                    <b-col>
                        <div>{{booking['date'].endDate | beautify-date-weekday-time}}</div>                        
                    </b-col>
                </b-row>
                <b-row class="mt-n3 h4">                    
                    <b-col class="text-primary">License Plate</b-col>
                    <b-col >
                        <b-form-group>
                            <b-form-input                   
                                style="display:inline"
                                :state="licensePlateState?null:false"                            
                                v-model="licensePlate">
                            </b-form-input> 
                        </b-form-group> 
                    </b-col>                       
                    
                </b-row>
            </b-card>            

            <template v-slot:modal-footer>
                
                <b-button class="mr-auto" variant="dark" @click="closeBookingWindow">Cancel</b-button>
                <b-button                     
                    variant="success" 
                    @click="saveNewBooking">
                    <b-icon-calendar-check-fill class="mr-2"/>Create Booking
                </b-button>
                
            </template>

            <template v-slot:modal-header-close>
                <b-button
                    variant="outline-dark"
                    class="closeButton"
                    @click="closeBookingWindow"
                    >&times;</b-button>
            </template>
        </b-modal> 

        <b-modal body-class="py-0" size="xl" v-model="bookingResultWindow" header-class="bg-primary text-white" >
            <template v-slot:modal-title>
                <h1 class="my-2 ml-2">Parking Reservation Request Status</h1> 
            </template>

            <b-card v-if="!bookingErr" border-variant="white" class="h3 text-center p-2 text-success text-white">
                Your booking has been confirmed.
            </b-card>
            <b-card v-else border-variant="white" class="h3 p-2 text-danger text-white">
                We are not able to process your request. {{bookingErr}}
            </b-card>

            <template v-slot:modal-footer class="text-center">                
                <b-button  variant="primary" @click="closeBookingResultWindow">OK</b-button>
            </template>
            <template v-slot:modal-header-close>
                <b-button
                    variant="outline-dark"
                    class="closeButton"
                    @click="closeBookingResultWindow"
                    >&times;</b-button>
            </template>
             
        </b-modal>     
    
    </b-card>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import * as _ from 'underscore';
import moment from 'moment-timezone';

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");
import { vehicleTypeOptions } from '../../utils/enums';

import { bookingSearchInfoType, bookingStatesInfoType, dateRangeInfoType, parkingSpotInfoType } from '@/types/Common';
import { userInfoType } from '@/types/Admin';

@Component
export default class SearchParkingSpotsTable extends Vue {

    @Prop({required: true})
    parkingSpots!: parkingSpotInfoType[];

    @Prop({required: true})
    searching!: boolean;  

    @Prop({required: true})
    bookingDates!: dateRangeInfoType;
    
    @Prop({required: true})
    vehicleType!: string;

    
    @commonState.State
    public user!: userInfoType;

    licensePlate ='';
    licensePlateState = true; 

    updatedBookingInfo = 0;
    vehicleTypeOptions;
    validVehicleTypeOptions;
    spotId = null;

    parkingSpotDataReady = false;
    showBookingWindow = false;

    bookingResultWindow = false;
    bookingErr=''

    parkingSpot = {} as parkingSpotInfoType; 
    bookingStates = {} as bookingStatesInfoType; 
    booking = {} as bookingSearchInfoType;    
   
    parkingSpotFields = [
        {key:'name',          label:'Spot Number',     sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:20%'},
        {key:'type',          label:'Spot Type',       sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:14%'},
        {key:'available',     label:'Status',          sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:21%'},
        {key:'nextAvailable', label:'Next Available',  sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:14%'},
        {key:'edit',          label:'',                sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:5%'}
    ]; 

    created(){
        this.vehicleTypeOptions = vehicleTypeOptions;
        
    }
   
    mounted() { 
        this.bookingStates = {} as bookingStatesInfoType;
        this.showBookingWindow = false;
        this.licensePlate = this.user.license_plate;
    }

    public bookParkingSpot(parkingSpotToBook: parkingSpotInfoType){              
        this.parkingSpot = parkingSpotToBook;
        this.booking = {} as bookingSearchInfoType;
        this.spotId = parkingSpotToBook.id;
        this.licensePlateState = true;
       
        this.prepopulateDefaultValues();
        
        this.showBookingWindow = true;
        this.parkingSpotDataReady = true;        
    }

    public prepopulateDefaultValues(){
       
        this.booking['date'] = this.bookingDates;       
        this.validVehicleTypeOptions = this.vehicleTypeOptions;
        this.booking['vehicleType'] = this.user.vehicle_type;
    }    
    
    public saveNewBooking(){

        this.licensePlateState = this.licensePlate?true:false;
        if(!this.licensePlateState) return

        this.bookingErr=''
        if (this.checkBookingStates()){ 

            const body ={
                "start_date": this.bookingDates.startDate,
                "end_date": this.bookingDates.endDate,
                "timezone": "UTC",
                "license_plate": this.licensePlate,
                "spot_id": this.spotId,
                "user_id": this.user.id
            }
            
            this.$http.post('/booking', body)
            .then((response) => {            
                if(response?.data){
                    this.closeBookingWindow();
                    this.bookingResultWindow = true;                
                }
                
            },(err) => {
                if(err.response.status == 409){
                    this.bookingErr="This parking spot is already booked for the selected period. Please select an available parking spot. In case no spots are available, refer to the next available field."
                }
                else
                    this.bookingErr=err.response.data.detail?err.response.data.detail:err.response.data
                this.showBookingWindow = false;
                Vue.nextTick(()=>this.bookingResultWindow = true);           
            });
        }        
    }    

    public checkBookingStates(){

        let stateCheck = true;      
        this.updatedBookingInfo ++;

        for(const field of Object.keys(this.bookingStates)){
            if(this.bookingStates[field]==false)
                stateCheck = false;
        }

        return stateCheck;            
    }
    
    public closeBookingWindow(){
        this.showBookingWindow = false; 
        this.clearStates();
    }

    public clearStates(){

        for(const field of Object.keys(this.bookingStates)){
            this.bookingStates[field] = null;                
        }                             
    }
    

    public getNextAvailable(bookings){

        const sortedBookings = _.sortBy(bookings, 'end_date')

        const start = moment(this.bookingDates.startDate)
        const end = moment(this.bookingDates.endDate)
        let endTimeConflict = false;

        const diffHours: number[] = []
        for(const booking of sortedBookings){
            const bookingStartDate = moment(booking['start_date'])
            const bookingEndDate = moment(booking['end_date'])
            const duration = moment.duration(bookingEndDate.diff(start)).asHours()
            
            if(duration>=0)
                diffHours.push(duration) 
            else 
                diffHours.push(100000)

            if(end > bookingStartDate && end <= bookingEndDate)
                endTimeConflict = true;
        }
        const min = Math.min(...diffHours)
        const nextAvailDateIndex = diffHours.indexOf(min)

        for(let nextTimeInx=nextAvailDateIndex; nextTimeInx< (sortedBookings.length-1); nextTimeInx++){
            const endTimeFirst =  sortedBookings[nextTimeInx]['end_date']
            const startTimeNext = sortedBookings[nextTimeInx+1]['start_date']
            const endTimeNext = sortedBookings[nextTimeInx+1]['end_date']            
            if(endTimeFirst!=startTimeNext){
                return {endTimeFirst:endTimeFirst, startTimeNext:startTimeNext, endTimeNext:endTimeNext, endTimeConflict:endTimeConflict}
            }
            else if(endTimeFirst==startTimeNext && nextTimeInx==(sortedBookings.length-2) ){
                return {endTimeFirst:endTimeNext, startTimeNext:null, endTimeNext:null, endTimeConflict:null}
            }
        }

        return {endTimeFirst:sortedBookings[nextAvailDateIndex]['end_date'], startTimeNext:null, endTimeNext:null, endTimeConflict:null}
    }

    get getParkingSpots(){
        enum vehicleTypes {Motorbike = 1, 'Car'=2, 'Truck'=3}
        return this.parkingSpots.filter(spot => (vehicleTypes[spot.type] >= vehicleTypes[this.vehicleType]))
    }

    public closeBookingResultWindow(){
        this.bookingResultWindow = false;
        if(!this.bookingErr)
            this.$router.push({ name: "manage-bookings" });
        this.bookingErr=''
    }

}
</script>

<style scoped lang="scss">

    .labels {
        font-size: 14px; font-weight:600; line-height: 1rem; color: rgb(12, 82, 114); margin-top:1rem;
    }

    .input-line {
        font-size: 14px; font-weight:600;
    }

    .closeButton {
        background-color: transparent !important;
        color: white;
        border: white;
        font-weight: 700;
        font-size: 2rem;
        padding-top: 0;
        margin-top: 0;
    }

</style>

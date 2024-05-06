<template>
    <b-card class="bg-white border-white">           

        <loading-spinner color="#000" v-if="searching" waitingText="Loading Results ..." />
        <div v-else> 

            <b-card no-body border-variant="white" bg-variant="white" v-if="!parkingSpots.length">
                <span class="text-muted ml-4 mb-5">No records found.</span>
            </b-card>

            <div v-else >

                <b-card  class="home-content border-primary py-1 text-center">
                    <b-row>
                        <b-col  v-for="motorBikeSpot in motorBikeSpots" 
                            :key="motorBikeSpot.id"
                            :id="'popover-button-variant'+motorBikeSpot.id">
                            <b-button
                                @click="bookParkingSpot(motorBikeSpot)"
                                :disabled="!motorBikeSpot.available || !motorBikeSpot['fit']"
                                class="bike-btn" 
                                variant="primary"
                                size="sm">
                                <i class="fa fa-motorcycle"></i>
                                    {{motorBikeSpot.name}}
                            </b-button>
                            <b-popover 
                                :key="'motor-'+motorBikeSpot.id+popoverKey"
                                custom-class="spot-info"
                                :disabled="motorBikeSpot.available && mobile && motorBikeSpot['fit']"                                                                
                                :target="'popover-button-variant'+motorBikeSpot.id"
                                triggers="hover"
                                placement="top"                                                                          
                                >
                                <parking-spot-details-popup @closePopover="popoverKey++;" :spotInfo="motorBikeSpot" :bookingDates="bookingDates"/>
                            </b-popover>
                        </b-col>
                    </b-row>
                </b-card>

                <div class="road-up">
                   <hr> 
                </div>
                <div class="road-down">
                   <hr> 
                </div>

                <b-card  class="home-content border-primary my-1 py-1 text-center">
                    <b-row>
                        <b-col  v-for="carSpot in carSpots.slice(0,10)" 
                            :key="carSpot.id"                            
                            :id="'popover-button-variant'+carSpot.id">
                            <b-button
                                @click="bookParkingSpot(carSpot)" 
                                :disabled="!carSpot.available || !carSpot['fit']"
                                class="car-btn" 
                                variant="primary">
                                <i class="fa fa-car"></i>
                                    {{carSpot.name}}
                            </b-button>
                            <b-popover 
                                :key="'car-1-'+carSpot.id+popoverKey"                               
                                custom-class="spot-info"                                
                                :disabled="carSpot.available && mobile && carSpot['fit']"                                                                
                                :target="'popover-button-variant'+carSpot.id"
                                triggers="hover"
                                placement="top">
                                <parking-spot-details-popup @closePopover="popoverKey++;" :spotInfo="carSpot" :bookingDates="bookingDates"/>
                            </b-popover>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col  v-for="carSpot in carSpots.slice(10,20)" 
                            :key="carSpot.id"                            
                            :id="'popover-button-variant'+carSpot.id">
                            <b-button 
                                @click="bookParkingSpot(carSpot)"
                                :disabled="!carSpot.available || !carSpot['fit']"
                                class="car-btn"  
                                variant="primary">
                                <i class="fa fa-car"></i>
                                    {{carSpot.name}}
                            </b-button>
                            <b-popover 
                                :key="'car-2-'+carSpot.id+popoverKey"
                                custom-class="spot-info"
                                :disabled="carSpot.available && mobile && carSpot['fit']"                                                                
                                :target="'popover-button-variant'+carSpot.id"
                                triggers="hover"
                                placement="top"                                                                          
                                >
                                <parking-spot-details-popup @closePopover="popoverKey++;" :spotInfo="carSpot" :bookingDates="bookingDates" />
                            </b-popover>
                        </b-col>
                    </b-row>                    
                </b-card>

                <div class="road-up">
                   <hr> 
                </div>
                <div class="road-down">
                   <hr> 
                </div>

                <b-card  class="home-content border-primary py-1 text-center">
                    <b-row>
                        <b-col v-for="truckSpot in truckSpots" 
                            :key="truckSpot.id"                            
                            :id="'popover-button-variant'+truckSpot.id">
                            <b-button
                                @click="bookParkingSpot(truckSpot)"
                                :disabled="!truckSpot.available || !truckSpot['fit']"
                                class="truck-btn"
                                variant="primary"
                                size="lg">
                                <b-icon-truck></b-icon-truck>
                                    {{truckSpot.name}}
                            </b-button>
                            <b-popover 
                                :key="'truck-'+truckSpot.id+popoverKey"
                                custom-class="spot-info"
                                :disabled="truckSpot.available && mobile && truckSpot['fit']"                                                                
                                :target="'popover-button-variant'+truckSpot.id"
                                triggers="hover"
                                placement="top"                                                                          
                                >
                                <parking-spot-details-popup @closePopover="popoverKey++;" :spotInfo="truckSpot" :bookingDates="bookingDates" />
                            </b-popover>
                        </b-col>
                    </b-row>
                </b-card>
                
                
            </div>      

         
        </div>

        <b-modal body-class="py-0" size="xl" v-model="showBookingWindow" header-class="bg-primary text-white" >
            <template v-slot:modal-title>
                <h1 class="parking-reservation-header my-2 ml-2">Parking Spot Reservation Request</h1> 
            </template>

            <b-card v-if="parkingSpotDataReady" class="border-white text-dark bg-white" body-class="py-0" :key="updatedBookingInfo"> 
                <b-row class="ml-auto mt-2 h2 parking-reservation-detail-txt">
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
                <h1 class="my-2 ml-2 parking-confirm-header">Parking Reservation Request Status</h1> 
            </template>

            <b-card v-if="!bookingErr" border-variant="white" class="h3 text-center p-2 text-success">
                Your booking has been confirmed.
            </b-card>
            <b-card v-else border-variant="white" class="h3 p-2 text-danger">
                We are not able to process your request. {{bookingErr}}
            </b-card>

            <template v-slot:modal-footer>                
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

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");
import { vehicleTypeOptions, vehicleTypes } from '../../utils/enums';

import { bookingSearchInfoType, bookingStatesInfoType, dateRangeInfoType, parkingSpotInfoType } from '@/types/Common';
import { userInfoType } from '@/types/Admin';
import ParkingSpotDetailsPopup from './ParkingSpotDetailsPopup.vue'

@Component({
    components:{
        ParkingSpotDetailsPopup
    }
})
export default class SearchParkingSpotsMap extends Vue {

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

    licensePlate = ''
    licensePlateState = true; 

    carSpots: parkingSpotInfoType[]=[];
    truckSpots: parkingSpotInfoType[]=[];
    motorBikeSpots: parkingSpotInfoType[]=[];

    motorBikeSpotMap = {};
   
    updatedBookingInfo = 0;
    vehicleTypeOptions;
    validVehicleTypeOptions;
    spotId = null;

    parkingSpotDataReady = false;
    showBookingWindow = false;

    bookingResultWindow = false;
    bookingErr=''
    mobile = false;
    popoverKey=0;

    parkingSpot = {} as parkingSpotInfoType; 
    bookingStates = {} as bookingStatesInfoType; 
    booking = {} as bookingSearchInfoType;    
   
    parkingSpotFields = [
        {key:'spotNumber',    label:'Spot Number',     sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:20%'},
        {key:'spotType',      label:'Spot Type',       sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:14%'},
        {key:'status',        label:'Status',          sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:21%'},
        {key:'nextAvailable', label:'Next Available',  sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:14%'},
        {key:'edit',          label:'',                sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', thStyle:'width:5%'}
    ]; 

    created(){
        this.vehicleTypeOptions = vehicleTypeOptions;
        
    }
   
    mounted() {
        this.mobile = false;
        if (window.innerWidth < 600) {
            this.mobile = true;
        } 
        this.showBookingWindow = false;
        this.bookingStates = {} as bookingStatesInfoType;
        this.showBookingWindow = false;
        this.extractInfo();
        this.licensePlate = this.user.license_plate;
    }

    public extractInfo(){
        const parkingSpots = this.getParkingSpots()        
        this.carSpots = parkingSpots.filter(spot=>{return spot.type == vehicleTypes.CAR})
        this.truckSpots = parkingSpots.filter(spot=>{return spot.type == vehicleTypes.TRUCK})
        this.motorBikeSpots = parkingSpots.filter(spot=>{return spot.type == vehicleTypes.MOTORBIKE})
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
    

    public getParkingSpots(){
        enum vehicleTypesNUM {Motorbike = 1, 'Car'=2, 'Truck'=3} 
        const spots = []
        for(const spot of this.parkingSpots){            
            spot['fit'] = (vehicleTypesNUM[spot.type] >= vehicleTypesNUM[this.vehicleType]);
            spots.push(spot)
        }

        return spots
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

    .road-up hr{
        border-top: 2px solid white;
        background: rgb(60, 60, 60);
        height: 2rem;
        margin-bottom: -1rem;
    }
    .road-down hr{
        border-top: 3px dashed white;
        background: rgb(60, 60, 60);
        height: 2rem;
    }

    .labels {
        font-size: 16px; font-weight:600; line-height: 1rem; color: rgb(12, 82, 114); margin-top:1rem;
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

    .bike-btn {
        background: rgb(231, 190, 53);
        width: 3rem;
        height: 5rem;;
    }

    .car-btn {
        background: rgb(53, 189, 231);
        width: 3.5rem;
        height: 5rem;;
    }

    .truck-btn {
        background: rgb(231, 53, 97);
        width: 5rem;
        height: 7rem;;
    }

  
    .popover{
        border-radius: 10px;
        border:1px solid #EEE;
        height: 21rem;
        max-height: 30rem;
        width: 30rem;
        max-width: 40rem;
        margin:0 -.5rem;
        padding: 0;
        box-shadow: 3px 3px 6px 6px #DDD;
        background: rgb(55, 98, 141);
    }

    @media screen and (max-width: 600px) {
        .popover.spot-info{
            height: 21rem;
            width:85%;
            max-width: 85%;
            box-shadow: none;
        }
        ::v-deep .modal-body{
            padding: 0 !important;
        }
        .parking-reservation-header{
            font-size: 16pt;            
        }
        .parking-reservation-detail-txt{
            font-size: 14pt;
        }
        .parking-confirm-header{
            font-size: 16pt;
        }
    }

</style>

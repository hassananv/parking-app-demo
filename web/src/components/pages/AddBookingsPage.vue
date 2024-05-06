<template>
    <b-card class="bg-white border-white w-100 add-booking-content">
        
        <loading-spinner color="#000" v-if="!dataReady" waitingText="Loading ..." />
        
        <b-card v-else class="bg-light border-white search-card"> 
                       
            <b-row class="search-wraper">                      
                <div :class="!dateState?'border border-danger date-picker':'date-picker'"> 
                    <div class="label">Date</div>                 
                    <booking-date-range-picker :key="update" :bookingRange="bookingDate" @datesAdded="addBookingDate"/>
                </div>                
                <div class="vehicle-type">
                    <div class="label">Vehicle Type</div> 
                    <b-form-group>
                        <b-form-select                             
                            style="display:inline"
                            @change="find"                            
                            :state="vehicleTypeState?null:false"
                            :options="vehicleTypeOptions"
                            v-model="vehicleType">
                        </b-form-select> 
                    </b-form-group>                    
                </div>               
                
                <div class="search-button">
                    <b-button
                        style="margin-top: 1.5rem; padding: 0.25rem 2rem; width: 100%;" 
                        :disabled="searching"
                        v-on:keyup.enter="find()"
                        variant="primary"
                        @click="find()"
                        ><spinner color="#FFF" v-if="searching" style="margin:0; padding: 0; height:2rem; transform:translate(0px,-24px);"/>
                        <span style="font-size: 20px;" v-else>Search</span>
                    </b-button>
                </div>
                
            </b-row> 

            <b-row  class="view-button-wraper">                
                <div class="view-button">
                    <b-button 
                        class="w-100"                                             
                        :disabled="searching"                        
                        variant="info"
                        @click="listView=true;find()"
                        ><i class="fa fa-list" style="margin-right:0.5rem;"></i>List View
                    </b-button>
                </div>
                <div class="view-button">
                    <b-button 
                        class="w-100"                      
                        :disabled="searching"                        
                        variant="info"
                        @click="listView=false;find()"
                        ><i class="fa fa-map" style="margin-right:0.5rem;"></i>Map View
                    </b-button>
                </div>                
            </b-row>                     
        </b-card>        

        
        <search-parking-spots-table            
            v-if="dataLoaded && listView"
            :parkingSpots="parkingSpots"
            :searching="searching"
            :vehicleType="vehicleType"
            :bookingDates="bookingDate" />

        <search-parking-spots-map            
            v-if="dataLoaded && !listView"
            :parkingSpots="parkingSpots"
            :vehicleType="vehicleType"
            :searching="searching"
            :bookingDates="bookingDate" />
        
    </b-card>
</template>

<script lang="ts">
import { Component, Vue} from 'vue-property-decorator';
import * as _ from 'underscore';
import moment from 'moment-timezone'

import Spinner from '@/components/utils/Spinner.vue'
import SearchParkingSpotsTable from "./components/SearchParkingSpotsTable.vue";
import SearchParkingSpotsMap from "./components/SearchParkingSpotsMap.vue";
import BookingDateRangePicker from "./components/BookingDateRangePicker.vue"



import { namespace } from "vuex-class";
import "@/store/modules/common";
import { dateRangeInfoType, parkingSpotInfoType } from '@/types/Common';

import { vehicleTypeOptions } from '../utils/enums';
import { userInfoType } from '@/types/Admin';


const commonState = namespace("Common");

@Component({
    components:{
        SearchParkingSpotsTable,
        SearchParkingSpotsMap,
        Spinner,
        BookingDateRangePicker

    }
})
export default class AddBookingsPage extends Vue {
    
    @commonState.State
    public user!: userInfoType;

    @commonState.Action
    public UpdateCurrentDate!: (string) => void;
    
    dataReady = false; 
    searching = false;
    dataLoaded = false; 
    listView = false;   
    
    vehicleType = '';
    vehicleTypeState = true; 
    
 
    updateTables =0

    parkingSpots: parkingSpotInfoType[] = [];

    bookingDate = {} as dateRangeInfoType;
    update = 0;
    dateState = true;
    
    vehicleTypeOptions; 

   

    created() {
        this.vehicleTypeOptions = vehicleTypeOptions;
    }

    mounted() {  
        this.dataLoaded = false;
        this.dataReady = false; 
        this.listView = true;
        this.vehicleTypeState = true;
        this.vehicleType = this.user.vehicle_type;
        this.dataReady = true;
        this.UpdateCurrentDate(moment().format("ddd MMM DD, YYYY HH:mm"))
    }

    public find(){
        this.UpdateCurrentDate(moment().format("ddd MMM DD, YYYY HH:mm"))
        this.dataLoaded = false;
        this.vehicleTypeState = this.vehicleType?true:false;

        this.dateState = (this.bookingDate.startDate && this.bookingDate.endDate)?true:false;

        if (this.vehicleTypeState && this.dateState){ 
            this.searching = true;
            this.parkingSpots = [];

            const body = {                
                "start_date":this.bookingDate.startDate,
                "end_date":this.bookingDate.endDate               
            }

            this.$http.post('/spot', body)
            .then((response) => {            
                if(response?.data){
                    this.parkingSpots =response.data;                    
                }
                this.searching = false;
                this.dataLoaded = true;
                
            },(err) => {
                this.searching = false; 
                this.dataLoaded = true;         
            });
            
        }
    }

    public addBookingDate(bookingDate){
        this.bookingDate = bookingDate
        this.update++;        
        this.find()
    }


}
</script>

<style scoped lang="scss">

    .label {
        font-size: 14pt; 
        font-weight:600;
        margin:-0.5rem 0 .5rem 0;
    }

    .search-wraper{    
        width: 70% !important;
        margin: 0 auto;
        display: flex;
        flex-wrap: wrap;
        align-content: center;
    }
    .date-picker{
        width: 63%;        
    }
    .vehicle-type{
        min-width: 20%;
        margin: 0rem 1% 0 1%;
    }
    .search-button{
        min-width: 15%;
        margin-top: 0.3rem;
    }

    .view-button-wraper{    
        width: 30% !important;
        margin: 0 auto;
        display: flex;
        flex-wrap: wrap;
        align-content: center;
    }
    .view-button{
        min-width: 40%;
        align-content: center;
        margin: 0.5rem 5%;
    }
    

    @media screen and (max-width: 600px) {
        .add-booking-content .card-body{
            margin: 0.1rem;
            padding: 0rem;
        }
        .search-card .card-body{
            margin: 0.5rem;
        }

        .label {
            font-size: 12pt; 
            font-weight:600;
            margin:0 0 0 0;
        }
        .search-wraper{    
            width: 100% !important;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            align-content: center;
        }
        .date-picker{
            width: 100%;
            margin-bottom: 1rem;
        }
        .vehicle-type{
            min-width: 100%;
            margin: 0;
        }
        .search-button{
            min-width: 100%;
            margin: 0 0 2rem 0;
        }

        .view-button-wraper{    
            width: 100% !important;
            margin: 2rem auto;
            display: flex;            
            flex-wrap: wrap;
            align-content: center;
        }

    }

</style>

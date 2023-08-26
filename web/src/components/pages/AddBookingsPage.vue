<template>
    <b-card class="bg-white border-white">
        
        <loading-spinner color="#000" v-if="!dataReady" waitingText="Loading ..." />
        
        <b-card v-else class="w-100 mx-auto my-1 bg-light border-white"> 
                       
           
            <b-row style="margin-top:-0.5rem">
                <b-col cols="2"></b-col>      
                <b-col cols="4" :class="!dateState?'border border-danger':''"> 
                    <div style="font-size:14pt; margin:-0.75rem 0 .5rem 0;">Date</div>                 
                    <booking-date-range-picker :key="update" :bookingRange="bookingDate" @datesAdded="addBookingDate"/>
                </b-col>                
                <b-col cols="2" style="margin-top:-0.75rem">
                    <b-form-group                     
                        label="Vehicle Type" 
                        label-for="vehicleType">
                        <b-form-select 
                            id="vehicleType"                            
                            style="display:inline"
                            @change="find"
                            :state="vehicleTypeState?null:false"
                            :options="vehicleTypeOptions"
                            v-model="vehicleType">
                        </b-form-select> 
                    </b-form-group>                    
                </b-col>               
                
                <b-col cols="2">
                    <b-button
                        name="search"
                        style="margin-top: 1.5rem; padding: 0.25rem 2rem; width: 100%;" 
                        :disabled="searching"
                        v-on:keyup.enter="find()"
                        variant="primary"
                        @click="find()"
                        ><spinner color="#FFF" v-if="searching" style="margin:0; padding: 0; height:2rem; transform:translate(0px,-24px);"/>
                        <span style="font-size: 20px;" v-else>Search</span>
                    </b-button>
                </b-col>
                <b-col cols="2"></b-col>
            </b-row> 
            <b-row  style="margin-top:-2rem">
                <b-col cols="4"></b-col>
                <b-col cols="2">
                    <b-button                        
                        style="margin-top: 1.5rem; padding: 0.25rem 0.5rem; width: 80%;" 
                        :disabled="searching"                        
                        variant="info"
                        @click="listView=true;find()"
                        ><i class="fa fa-list" style="margin-right:0.5rem;"></i>List View
                    </b-button>
                </b-col>
                <b-col cols="2">
                    <b-button                        
                        style="margin-top: 1.5rem; padding: 0.25rem 0.5rem; width: 80%;" 
                        :disabled="searching"                        
                        variant="info"
                        @click="listView=false;find()"
                        ><i class="fa fa-map" style="margin-right:0.5rem;"></i>Map View
                    </b-button>
                </b-col>
                <b-col cols="4"></b-col>
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

    .labels {
        font-size: 16px; font-weight:600;
    }

    .input-line {
        font-size: 12px; font-weight:600;
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

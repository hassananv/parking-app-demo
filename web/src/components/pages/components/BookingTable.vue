<template>
    <b-card class="bg-white border-white">                
            
       
        <div> 

            <b-card border-variant="info" bg-variant="info" v-if="!bookings.length">
                <div class="h3 mt-3 text-center">You have no reservations.</div>
            </b-card>      

            <b-card v-else class="home-content border-white p-0">
                <b-table
                    :items="bookings"
                    :fields="bookingFields"
                    sort-by="start_date"
                    class="border-info"                                    
                    small
                    sort-icon-left
                    responsive="sm">                    

                    <template v-slot:cell(start_date)="data" >
                        <span> 
                            {{data.value | beautify-date-weekday-time}}
                            
                        </span>
                    </template>  

                    <template v-slot:cell(end_date)="data" >
                        <span> 
                            {{data.value | beautify-date-weekday-time}}                            
                        </span>
                    </template>   

                    <template v-slot:cell(spotNumber)="data" >
                        <span> 
                            {{data.item.spot.name}}                            
                        </span>
                    </template> 

                    <template v-slot:cell(past)="data" >
                        <b-badge v-if="pastBooking(data.item.end_date)"> 
                            Passed                           
                        </b-badge>
                    </template>

                    <template v-slot:cell(spotType)="data" >
                        <span> 
                            {{data.item.spot.type}}                            
                        </span>
                    </template> 

                    <template v-slot:cell(cancel)="data">
                        <b-row  style="float: right;" class="mr-1">
                            <b-button size="sm" variant="transparent" class="my-0 py-0"
                                @click="confirmCancelBooking(data.item);"
                                v-b-tooltip.hover.noninteractive.left.v-danger
                                title="Cancel Reservation">
                                <b-icon-trash-fill font-scale="1.25" variant="danger"></b-icon-trash-fill>                    
                            </b-button>
                        </b-row> 
                    </template>                   
                    
                </b-table>

            
            </b-card>
        </div>



        <b-modal size="xl" v-model="showCancelBookingWindow" header-class="bg-primary text-white" >
            <template v-slot:modal-title>
                <h1 class="my-2 ml-2">Cancel Parking Spot Reservation</h1> 
            </template>           
              
            <b-card v-if="bookingDataReady" class="border-white" :key="updatedBookingInfo">

                <b-row class="mt-1 mb-4 ml-2 h2">
                    Are you sure you want to cancel your 
                    parking reservation in Spot number {{booking.spot.name}}?                       
                </b-row>                    
            </b-card>

            <template v-slot:modal-footer>
                
                <b-button class="mr-auto" variant="dark" @click="closeCancelBookingWindow">Keep Booking</b-button>
                <b-button
                    variant="danger" 
                    @click="cancelBooking">
                    <b-icon-x-circle-fill class="mr-2"/>Cancel Booking
                </b-button>
                
            </template>

            <template v-slot:modal-header-close>
                <b-button
                    variant="outline-dark"
                    class="closeButton"
                    @click="closeCancelBookingWindow"
                    >&times;</b-button
                >
            </template>
        </b-modal>        
    
    </b-card>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import * as _ from 'underscore';
import moment from 'moment-timezone'

import { bookingSearchInfoType } from '@/types/Common';


@Component
export default class BookingTable extends Vue {

    @Prop({required: true})
    bookings!: bookingSearchInfoType[];
    
 
    bookingDataReady = false;
    updatedBookingInfo = 0;

    showCancelBookingWindow = false; 
    booking = {} as bookingSearchInfoType;

    bookingFields = [        
        {key:'spotNumber',     label:'Parking Spot Number', sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle,', tdClass:'align-middle', },
        {key:'spotType',       label:'Parking Spot Type',   sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', },
        {key:'license_plate',   label:'License Plate Number',sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', },
        {key:'start_date',      label:'Start',               sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', },
        {key:'end_date',        label:'End',                 sortable:true,  cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', },
        {key:'past',           label:'',                    sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', },
        {key:'cancel',         label:'',                    sortable:false, cellStyle:'', thClass:'bg-primary text-white align-middle', tdClass:'align-middle', }
    ];

    mounted() { 
        this.booking = {} as bookingSearchInfoType;   
        this.bookingDataReady = false;    
    }
    
    public closeCancelBookingWindow(){
        this.showCancelBookingWindow = false;
    }   
    
    public confirmCancelBooking(bookingToCancel: bookingSearchInfoType){        
        this.booking = JSON.parse(JSON.stringify(bookingToCancel));
        this.showCancelBookingWindow = true;
        this.bookingDataReady = true;
    }

    public cancelBooking(){       
        
        this.$http.delete('/booking/' + this.booking.id)
        .then((response) => {            
            this.closeCancelBookingWindow();
            this.$emit('find'); 
            this.bookingDataReady = true;             
        },(err) => {
            this.bookingDataReady = true;         
        });       
        
    }  

    public pastBooking(endDate){
        const current = moment().format()
        if(endDate<=current) return true;
        return false;
    }

}
</script>

<style scoped lang="scss">

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
<template>
    <b-card v-if="dataReady" body-class="py-3" style="height:19.5rem">

        <b-card-header class="text-center h2 my-n2" >Parking Spot Details:</b-card-header>
        <b-card-body>
            <b-row class="mt-n2">
                <b-col class="text-primary">Spot Number</b-col>
                <b-col>{{spotInfo.name}}</b-col>
            </b-row>
            <b-row class="mt-n3">
                <b-col class="text-primary">Spot Type</b-col>
                <b-col>{{spotInfo.type}}</b-col>
            </b-row>
            <b-row class="mt-n3">
                <b-col class="text-primary">Status</b-col>
                <b-col>                    
                    <span class="p-1 bg-orange text-white rounded" v-if="!spotInfo['fit']">Irrelevant spot type</span>
                    <span class="p-1 bg-danger text-white rounded" v-else-if="!spotInfo.available">Occupied</span>
                    <span class="p-1 bg-success text-white rounded" v-else>Available</span>                     
                </b-col>
            </b-row>
            <b-row class="mt-n3">
                <b-col class="text-primary">Next Available</b-col>
                <b-col>
                    <div style="white-space: pre;" v-if="spotInfo.booking.length>0 && !spotInfo.available">{{getNextAvailable(spotInfo.booking)| beautify-date-next-available}}</div> 
                    
                </b-col>
            </b-row>

        </b-card-body>
        <b-button class="popover-close-btn" @click="closePopup()" size="sm" variant="dark">Close</b-button>
    </b-card>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import moment from 'moment-timezone';
import * as _ from 'underscore';

import { dateRangeInfoType, parkingSpotInfoType } from '@/types/Common';


@Component
export default class ParkingSpotDetailsPopup extends Vue {   

    @Prop({required: true})
    spotInfo!: parkingSpotInfoType;
    
    @Prop({required: true})
    bookingDates!: dateRangeInfoType;

    dataReady=false

        
    
    mounted(){
        this.dataReady=false
        this.dataReady=true
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

    closePopup(){        
        this.$emit('closePopover');
    }

}
</script>
<style scoped lang="scss">
    .popover-close-btn{
        display: none;
    }
    @media screen and (max-width: 600px) {
        .popover-body .card-body{
            margin: 0;
            padding: 0 0.1rem;
        }

        .popover-body .card-body .card-header{
            font-size: 14pt;
        }
        
        .popover-close-btn{
            display: flex;
            margin: 4rem auto 0 auto;
        }    
    }

</style>
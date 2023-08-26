<template>
    <b-card class="bg-white border-white">                
            
        <loading-spinner color="#000" v-if="!dataReady" waitingText="Loading ..." />
        
        <booking-table 
            v-else
            :bookings="bookings" 
            @find="find" />
    
    </b-card>
</template>

<script lang="ts">


import { Component, Vue} from 'vue-property-decorator';
import * as _ from 'underscore';
import moment from 'moment-timezone'

import BookingTable from './components/BookingTable.vue';
import { bookingSearchInfoType} from '@/types/Common';

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");

@Component({
    components:{
        BookingTable
    }
})
export default class ManageBookingsPage extends Vue {
    
    
    @commonState.Action
    public UpdateCurrentDate!: (string) => void;

    dataReady = false; 
    bookings: bookingSearchInfoType[] = [];  
  
   
    mounted() {  
        this.dataReady = false;
        this.find()
    }    

    public find(){
        this.UpdateCurrentDate(moment().format("ddd MMM DD, YYYY HH:mm"))
        this.bookings = [];

        this.$http.get('/booking')
        .then((response) => {            
            if(response?.data){                     
                this.bookings = response.data;                                      
            }
            this.dataReady = true;
            
        },(err) => {
            this.dataReady = true;
        });        
        
    }  

}
</script>


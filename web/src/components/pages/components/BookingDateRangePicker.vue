<template>
    <b-card body-class="p-0" id="booking-date-container"> 
        <b-button 
            @click="initDates();onShow=true;"
            id="popover-button-variant" 
            variant="transparent" 
            class="border-0" 
            style="width:100%; margin:0; padding:0.5rem 1rem;"
            >
            <span v-html="pickedDates">{{pickedDates}}</span> <b-icon-calendar style="float:right"/>
        </b-button>
        <b-popover 
            customClass="pop"
            target="popover-button-variant"  
            triggers="manual"
            placement="bottomleft"
            container="booking-date-container"
            ref="popover"
            :show.sync="onShow"           
            >
            <div>
                <b-row class="mt-1 py-0" >
                    <b-col cols="5 text-center bg-select h4 border ml-4">
                        <span v-if="dates[1]<dates[0]"><b class="text-danger">From: </b>{{dates[1]|beautify-date-weekday}}</span>
                        <span v-else><b class="text-danger">From: </b>{{dates[0]|beautify-date-weekday}}</span>
                    </b-col>
                    <b-col cols="1" />
                    <b-col cols="5 text-center bg-select h4 border ml-2">
                        <span v-if="dates[0]>dates[1]"><b class="text-danger">To: </b>{{dates[0]|beautify-date-weekday}}</span>
                        <span v-else ><b class="text-danger">To: </b>{{dates[1]|beautify-date-weekday}}</span>
                    </b-col>
                </b-row>
                <b-row class="py-0" style="margin-top:-3rem;">
                    <b-col cols="6">
                        <v-app style="height:24rem; padding:0; margin:1rem 0 -2rem 0;">                        
                            <v-date-picker
                                v-model="dates"
                                color="success"
                                :allowed-dates="allowedDates"                                                         
                                range                                
                                :picker-date.sync="pickerDateL"
                            ></v-date-picker>                            
                        </v-app>
                    </b-col>
                    <b-col cols="4">
                        <v-app style="height:24rem; padding:0; margin:1rem 0 -2rem 0;">                        
                            <v-date-picker
                                v-model="dates"
                                color="success"
                                :allowed-dates="allowedDates"                                 
                                range
                                :picker-date.sync="pickerDateR"                                
                            ></v-date-picker>                            
                        </v-app>
                    </b-col>
                </b-row>
            </div>

            <b-row style="margin-top:-2.25rem;">
                <b-col cols="3">                    
                    <div style="margin:0.25rem 0 0 0; font-size:13pt; font-weight: 600;">Start Time:</div>                     
                    <div v-if="startTimeError" style="line-height:1.2rem;" class="mt-n2 py-0 px-0 text-danger">Time is in the past.</div>
                </b-col>
                <b-col cols="3">                     
                    <b-form-select :state="startTimeState" v-model="startTime" :options="timeOptions"></b-form-select>                             
                </b-col>
                
                <b-col cols="3">                    
                    <div style="margin:0.25rem 0 0 0; font-size:13pt; font-weight: 600;">End Time:</div>
                    <div v-if="timeError" style="line-height:1rem;" class="mt-n2 py-0 px-0 text-danger"> Before start time!</div>
                </b-col>
                <b-col cols="3">
                    <b-form-select :state="endTimeState" v-model="endTime" :options="timeOptions"></b-form-select>
                </b-col>
                
            </b-row>

            <b-row class="border rounded mx-0" style="margin-top:1rem; box-shadow: 0px 0px 4px 2px #DDD;">
                <b-col>
                    <b-button @click="focusSearchButton();onShow=false" class="border" variant="white" style="width:7rem;" >Cancel</b-button>
                </b-col>
                <b-col>
                    <b-button @click="setDatesToday" style="width:7rem;" variant="primary">Today</b-button>
                </b-col>                
                <b-col>
                    <b-button @click="AddDates" class="px-4" variant="success" style="float:right; width:7rem;">Add</b-button>
                </b-col>
            </b-row>
        </b-popover>

    </b-card>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import moment from 'moment-timezone'

import * as _ from 'underscore';
import { dateRangeInfoType } from '@/types/Common';

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");


@Component
export default class BookingDateRangePicker extends Vue {
    
    @Prop({required: true})
    bookingRange!: dateRangeInfoType;

    @commonState.Action
    public UpdateCurrentDate!: (string) => void;

    onShow= false
    dates = []

    pickedDates=""
    pickerDateL=""
    pickerDateR=""
    startTime=''
    timeOptions = []
    endTime=''
    startTimeState = null
    endTimeState = null
    timeError = false
    startTimeError = false

    @Watch('pickerDateL')
    monthChange(newValue){
        this.pickerDateR = moment(newValue).add(1,'months').format("YYYY-MM")
    }

    @Watch('pickerDateR')
    monthChangeR(newValue){
        this.pickerDateL = moment(newValue).add(-1,'months').format("YYYY-MM")
    }
   

    mounted(){        
        this.timeError = false
        this.startTimeError = false
        this.initialTime()
        this.initDates()
    }


    public initialTime(){
        for(const time of [...Array(24).keys()]){            
            this.timeOptions.push(this.time24ToAmPm(time))            
        }
    }

    public initDates(){
        this.UpdateCurrentDate(moment().format("ddd MMM DD, YYYY HH:mm"));

        this.dates = []
     
        this.dates.push(this.bookingRange.startDate?.slice(0,10))
        this.dates.push(this.bookingRange.endDate?.slice(0,10))

        this.startTime = this.time24ToAmPm(this.bookingRange.startDate?.slice(11,13))
        this.endTime = this.time24ToAmPm(this.bookingRange.endDate?.slice(11,13))

        const newDates = this.CombineDateTime()
        this.getDatesText(newDates)

        if(this.bookingRange.startDate?.slice(0,7))
            this.pickerDateL = this.bookingRange.startDate.slice(0,7)
        else
            this.pickerDateL = moment().format("YYYY-MM")
    }


    public getDatesText(bookingDate){

        if(!bookingDate[1] || !bookingDate[0])
            this.pickedDates ='No dates'
        else
            this.pickedDates ='<b>From </b>'+ moment(bookingDate[0]).format("MMM DD, YYYY HH:mm") +
                              '<b>  To </b>'+  moment(bookingDate[1]).format("MMM DD, YYYY HH:mm");      
    }

    public CombineDateTime(){
        this.dates = _.sortBy(this.dates)
        if(!this.dates[1] || !this.dates[0])
            return this.dates

        return [
            this.startTime? this.dates[0]+'T'+this.timeTo24h(this.startTime) :this.dates[0],
            this.endTime?   this.dates[1]+'T'+this.timeTo24h(this.endTime)   :this.dates[1]
        ]
    }

    public AddDates(){
        this.timeError = false
        this.startTimeError = false
        this.startTimeState = this.startTime? null : false
        this.endTimeState = this.endTime? null : false
        if(!this.startTime || !this.endTime) return 


        if(!this.dates[1] && !this.dates[0])
            this.setDatesToday()
        else if(!this.dates[0])
            this.dates[0] = this.dates[1]
        else if(!this.dates[1])
            this.dates[1] = this.dates[0]
        
        const newDates = this.CombineDateTime()

        this.getDatesText(newDates)

        if(newDates[0] >= newDates[1]){
            this.startTimeState =  false
            this.endTimeState =  false
            this.timeError = true
            return
        }
        const currentTime = moment().format()
        if(newDates[0] < currentTime){
            this.startTimeState =  false
            this.startTimeError = true
            return
        }

        const dateRange: dateRangeInfoType = {
            startDate:moment(newDates[0]).format() ,
            endDate:moment(newDates[1]).format()
        }

        this.$emit('datesAdded',dateRange)
        this.onShow= false
    }

    public focusSearchButton(){
        Vue.nextTick(()=>{
            const el = document.getElementsByName("search")[0];
            if(el) el.focus();
        })        
    }

    public timeTo24h(time){
        const timeParts = time.split(' ')
        if(timeParts[1]=='AM' && Number(timeParts[0])<10)
            return '0'+timeParts[0]+':00'
        if(timeParts[1]=='AM' && Number(timeParts[0])==12)
            return '00:00'
        if(timeParts[1]=='PM' && Number(timeParts[0])==12)
            return '12:00'
        if(timeParts[1]=='AM' && Number(timeParts[0])>=10)
            return timeParts[0]+':00'
        if(timeParts[1]=='PM')
            return (Number(timeParts[0])+12)+':00'

    }

    public time24ToAmPm(timeStr){
        
        if(timeStr||timeStr=='0'||timeStr==0){ 
            const time = Number(timeStr)
            if (time == 0){
                return '12 AM'
            } else if (time == 12) {
                return '12 PM'
            } else if (time<12) {
                return (time +' AM')
            } else {
                return (time-12 +' PM')
            }
        }
        return ''
    }



    public setDatesToday(){
        const today = moment().format("YYYY-MM-DD")        
        this.dates=[today, today]
        this.pickerDateL = moment().format("YYYY-MM")
    }

    public allowedDates(date){
        const day = moment(date).format()
        const current = moment().startOf('day').format()
        if(day<current) return false
        else return true
    }

    
}
</script>

<style scoped lang="scss" >    
    .popover{
        border-radius: 10px;
        border:1px solid #EEE;
        height: 33rem;
        width: 40rem;
        max-width: 40rem;
        margin:0 -.5rem;
        padding: 0;
        box-shadow: 3px 3px 6px 6px #DDD;
    }
</style>
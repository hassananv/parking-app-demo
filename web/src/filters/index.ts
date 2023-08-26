import Vue from 'vue'
import moment from 'moment-timezone';
import * as _ from 'underscore';



Vue.filter('beautify-date', function(date){
	
	if(date)
		return moment(date).format('MMM DD, YYYY');
	else
		return ' '
})

Vue.filter('beautify-date-weekday-time', function(date){
	if(date)
		return	moment(date).format('ddd MMM DD, YYYY HH:mm');
	else
		return ''
})


Vue.filter('beautify-date-next-available', function(date){

	if(date.endTimeFirst){
		const currentDate = moment()
		const nextDate = moment(date.endTimeFirst)
		const duration = moment.duration(nextDate.diff(currentDate))
		const hours = Math.trunc(duration.asHours())
		if(date.endTimeConflict && date.startTimeNext && date.endTimeNext){			
			return (
				'Available from:\n'+nextDate.format("ddd MMM DD - HH:00") +
				' to:\n'+moment(date.startTimeNext).format("ddd MMM DD - HH:00") +
				' or after:\n'+moment(date.endTimeNext).format("ddd MMM DD - HH:00")
			)	
		}else if(hours==0){
			return ('Less than 1 Hour')
		}else if(hours==1){
			return ('1 Hour')
		}else 
			return (hours+ ' Hours')
	}
	else
		return ''
})


Vue.filter('beautify-date-weekday', function(date){
	if(date)
		return	moment(date).format('ddd, MMM DD, YYYY');
	else
		return ''
})



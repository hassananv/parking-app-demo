<template>
	<header v-if="user && user.userName" name="menu-bar" class="app-header" :key="update">
		<b-navbar toggleable="lg" class="navbar navbar-expand-lg navbar-dark m-0 p-0" style="background-color: #0c4433;">    
		
			<b-navbar-nav  class="my-0 mx-5">
                <b-nav-item 
					v-for="item,inx in bothGroup" 
					:key="inx"
					@click="ChangeClass(item.name); adminTab = false;" 
					:to="'/'+item.name"
					:class="bgClass[item.name]" >
					<div class="booking-tab">{{item.label}}</div>
				</b-nav-item>
				
			</b-navbar-nav>
			<div :key="updateTime" style="margin:0 3rem 0 auto; color:#FFF;">{{currentDate}}</div>
		</b-navbar> 
	</header>
</template>

<script lang="ts">
import { Component, Vue, Watch} from 'vue-property-decorator';	
import { Route } from 'vue-router';
import moment from 'moment-timezone'

import { namespace } from "vuex-class";   
import "@/store/modules/common";
import { userInfoType } from "@/types/Admin";
const commonState = namespace("Common");

@Component
export default class MenuBar extends Vue {
	
	@commonState.State
    public user!: userInfoType;

	@commonState.State
    public currentDate!: string;

	@commonState.Action
    public UpdateCurrentDate!: (string) => void;

	bgClass={}

	adminTab = false;
	update=0;

	updateTime=0;
	
	bothGroup=[
		{name:'manage-bookings', label:'Manage Bookings', super_admin:false},
		{name:'add-bookings', label:'Add Bookings', super_admin:false},
	]
	

	@Watch('$route', { immediate: true, deep: true })
	onUrlChange(newVal: Route) {			
		this.ChangeClass(newVal.name)
		this.update++;			
	}

	@Watch('currentDate')
    monthChange(newValue){
        this.updateTime++;
    }

	mounted(){
		this.UpdateCurrentDate(moment().format("ddd MMM DD, YYYY HH:mm"))
	}

	ChangeClass(type){
		const items = this.bothGroup
		for(const item of items)
			this.bgClass[item.name]=""
		
		this.bgClass[type]="bg-cyan"
	}

}
</script>

<style scoped>   

	.booking-tab{
		font-size:14pt; 
		display: inline-block; 
		white-space: nowrap;
		margin: 0 1rem;
	}

    ul >>> .dropdown-menu {
        width: 250px !important;
    }
</style>
<template>
    <div v-if="pageReady" >
            
            <b-card style="width:60rem; margin:0 auto;" no-body border-variant="white">
                <b-alert style="margin-top:0.8rem" :variant="alertType" :show="dismissCountDown"  @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">
                    <b v-if="alertType=='success'">{{message}} <b-icon-check-square-fill class="ml-1"/> </b>
                    <b v-else> {{message}}<b-icon-exclamation-circle-fill class="ml-1"/> </b>
                </b-alert> 
            </b-card>

            <b-card class="login-section my-4" :key="updateProfileInfo">
                <b-card-header class="card-header text-center h1">
                    Profile
                </b-card-header>
                <b-card-body>
                    <b-row>
                        <b-col>
                            <b-form-group                        
                                label="First Name" 
                                label-for="firstName">
                                <b-form-input 
                                    id="firstName"                                                          
                                    style="display:inline"
                                    v-model="userToEdit.first_name"
                                    :state="profileStates.firstName"
                                    placeholder="First Name"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group                        
                                label="Last Name" 
                                label-for="lastName">
                                <b-form-input 
                                    id="lastName"                                                          
                                    style="display:inline"
                                    v-model="userToEdit.last_name"
                                    :state="profileStates.lastName"
                                    placeholder="Last Name"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                    </b-row>  
                    <b-row>
                        <b-col>
                            <b-form-group                        
                                label="Vehicle Type" 
                                label-for="vehicleType">
                                <b-form-select 
                                    id="vehicleType"                                                          
                                    style="display:inline"
                                    :options="vehicleTypeOptions"
                                    :state="profileStates.vehicleType"
                                    v-model="userToEdit.vehicle_type"
                                >
                                </b-form-select> 
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group                        
                                label="License Plate Number" 
                                label-for="plateNumber">
                                <b-form-input 
                                    id="plateNumber"                                                          
                                    style="display:inline"
                                    :state="profileStates.licensePlate"
                                    v-model="userToEdit.license_plate"
                                    placeholder="License Plate Number"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                    </b-row>

                    <div v-if="!changePassword">
                        <b-row v-if="!isKeycloak" class="mt-4 text-center">
                            <b-col>
                                <b-button variant="danger" @click="changePassword=true;">
                                    Change Password
                                </b-button>
                            </b-col>
                        </b-row>
                    </div> 
                    <div v-else>
                        <b-row class="mt-5">
                            <b-col cols="12">
                                <b-form-group                        
                                    label="Old Password" 
                                    label-for="old-password">
                                    <b-form-input
                                        type="password" 
                                        id="old-password"                                                          
                                        style="display:inline"
                                        v-model="userToEdit.old_password"
                                        :state="profileStates.oldPassword"
                                        placeholder="Password"
                                    >
                                    </b-form-input> 
                                </b-form-group>
                            </b-col>                        
                        </b-row>    
                        <b-row>
                            <b-col cols="6">
                                <b-form-group                        
                                    label="New Password" 
                                    label-for="password">
                                    <b-form-input
                                        type="password" 
                                        id="password"                                                          
                                        style="display:inline"
                                        :state="profileStates.password"
                                        v-model="userToEdit.password"
                                        placeholder="Password"
                                    >
                                    </b-form-input> 
                                </b-form-group>
                            </b-col>
                            <b-col cols="6">
                                <b-form-group                        
                                    label="Confirm New Password" 
                                    label-for="confirm-password">
                                    <b-form-input
                                        type="password" 
                                        id="confirm-password"                                                          
                                        style="display:inline"
                                        :state="profileStates.confirmPassword"
                                        v-model="confirmPassword"
                                        placeholder="Password"
                                    >
                                    </b-form-input> 
                                </b-form-group>
                            </b-col>
                        </b-row> 
                    </div>
                    <b-row class="mt-5">
                        <div class="mx-auto">
                            <b-row>
                                <a class="nav-link"  @click="disclaimer.show = true" style="margin:-0.5rem -0.5rem 0 0; cursor: pointer;">Disclaimer</a> Terms: <b class="ml-3 text-success"> Accepted <b-icon-check2-square class="ml-2" scale="1.5" /> </b>
                            </b-row>
                        </div>
                    </b-row>
                    <b-row class="mt-5">
                        <b-button  
                            style="margin-top: 0.6rem; padding: 0.25rem 2rem; width: 100%;" 
                            :disabled="registering"
                            variant="primary"
                            @click="updateProfile()"
                            ><spinner color="#FFF" v-if="registering" style="margin:0; padding: 0; height:2rem; transform:translate(0px,-25px);"/>
                            <span style="font-size: 20px;" v-else>Save Changes</span>
                        </b-button>
                    </b-row>
                </b-card-body>
            </b-card>
        <disclaimer :disclaimer="disclaimer" :declineButton="false"/>
            
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Spinner from '@/components/utils/Spinner.vue'
import Disclaimer from "@/components/Disclaimer.vue"

import { namespace } from "vuex-class";   
import "@/store/modules/common";
import { userInfoType, userStatesInfoType } from '@/types/Admin';
const commonState = namespace("Common");


import { vehicleTypeOptions } from '../utils/enums';

@Component({
    components:{
        Spinner, 
        Disclaimer       
    }
})
export default class UserProfile extends Vue {
    
    @commonState.State
    public user!: userInfoType;

    @commonState.State
    public isKeycloak!: boolean;

    disclaimer = {show: false}

    changePassword = false
    oldPassword = ''
    confirmEmail = ''
    confirmPassword = ''    

    pageReady = false;
    registering = false;
    updateProfileInfo = 0;

    dismissCountDown =0
    alertType = '';
    message = '';

    profileStates = {} as userStatesInfoType;

    userToEdit = {} as userInfoType;  
    vehicleTypeOptions;  
    
    created() {
        this.vehicleTypeOptions = vehicleTypeOptions;
    }

    mounted() {
        this.pageReady = false;
        this.registering = false;
        this.profileStates = {} as userStatesInfoType;
        this.clearStates();
        this.getUserInformation();
    }
       
    public getUserInformation(){    

        this.$http.get('/user/info')
        .then(response =>{
            this.userToEdit = response.data
            this.pageReady = true;
        },err =>{
            this.message = err.response.data.detail;
            this.alertType="danger";
            this.dismissCountDown = 3;
            this.pageReady = true;

        });                 
    }    

    public updateProfile() {

        this.clearStates();
        if (this.checkProfileStates()){

            this.registering = true;
            this.$http.put('/user/update',this.userToEdit)
            .then(response =>{
                this.registering = false;
                this.alertType="success";
                this.dismissCountDown = 3;
                this.message = "You have successfully updated your profile information."
            
            },err =>{
                this.message = err.response.data.detail;
                this.alertType="danger";
                this.dismissCountDown = 3;
                this.registering = false;                
            });   
        } 
    }

    public checkProfileStates(){

        let stateCheck = true;
    
        this.profileStates.email = null;
        this.profileStates.confirmEmail = null;        
        this.profileStates.firstName = !(this.userToEdit.first_name)? false : null;
        this.profileStates.lastName = !(this.userToEdit.last_name)? false : null;
        this.profileStates.vehicleType = !(this.userToEdit.vehicle_type)? false : null;
        this.profileStates.licensePlate = !(this.userToEdit.license_plate)? false : null;
        if (this.changePassword){
            this.profileStates.oldPassword = !(this.userToEdit.old_password)? false : null;
            this.profileStates.password = !(this.userToEdit.password)? false : null;
            this.profileStates.confirmPassword = !(this.userToEdit.password && this.confirmPassword && this.userToEdit.password == this.confirmPassword)? false : null;      
        } else {
            this.profileStates.oldPassword = null;
            this.profileStates.password = null;
            this.profileStates.confirmPassword = null;
        }

        this.updateProfileInfo ++;

        for(const field of Object.keys(this.profileStates)){
            if(this.profileStates[field]==false)
                stateCheck = false;
        }   
        return stateCheck;            
    }

    public clearStates(){
        for(const field of Object.keys(this.profileStates)){
            this.profileStates[field] = null;                
        }
    }

    public countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
    }


  
}
</script>

<style scoped lang="scss">

.login-section {
  font-size: 24px;
  line-height: 1.6; 
  margin: 0 auto; 
  width: 40rem;
  border: 2px solid ;
  border-radius: 18px;
  background-color: rgba(235, 224, 205, 0.76);
  box-shadow: 5px 10px 10px 10px #DDD;
}

.card-header {
    background: rgb(23, 39, 43);
    color: white;
    border-radius: 10px !important;
    border:0px solid white;
}

</style>

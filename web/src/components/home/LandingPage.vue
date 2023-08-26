<template>
    <div v-if="pageReady">
        <b-container>

            <b-card class="info-section my-4">
                <b-card-header class="card-header text-center">
                    How it Works?
                </b-card-header>
                <b-card-body class="how-works-section">
                    To use the Online Parking Reservation Application you will need to set up a profile.
                    If you do not currently have an account you can register for one 
                    by clicking the Register button below.                    
                </b-card-body>
                <b-card-footer class="text-warning h3" style="font-size:16pt;">
                    This application is for demo purposes only. It is not referring to any actual parking lot.
                </b-card-footer>
            </b-card>

            <b-card class="info-section my-5">
                <b-row>
                    <b-col cols="6 text-center">
                        <b-button class="btn-lg bg-warning login-button" @click="register()">
                                Register
                        </b-button>                              
                    </b-col> 
                    <b-col cols="6 text-center">
                        <b-button class="btn-lg bg-warning login-button" @click="login()">
                                Login                                                                               
                        </b-button>                                               
                    </b-col>     
                </b-row>            
            </b-card>
            
            <b-card style="width:60rem; margin:0 auto;" no-body border-variant="white">
                <b-alert style="margin-top:0.8rem" :variant="alertType" :show="dismissCountDown"  @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">
                    <b v-if="alertType=='success'">{{message}} <b-icon-check-square-fill class="ml-1"/> </b>
                    <b v-else> {{message}}<b-icon-exclamation-circle-fill class="ml-1"/> </b>
                </b-alert> 
            </b-card>

            <b-card v-if="signUp && !signIn" class="register-section my-4" :key="updateRegisterInfo">
                <b-card-header class="text-center">
                    Register
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
                                    v-model="newUser.first_name"
                                    :state="registerStates.firstName"
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
                                    v-model="newUser.last_name"
                                    :state="registerStates.lastName"
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
                                    :state="registerStates.vehicleType"
                                    v-model="newUser.vehicle_type"
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
                                    v-model="newUser.license_plate"
                                    :state="registerStates.licensePlate"
                                    placeholder="License Plate Number"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row >
                        <b-col cols="6">
                            <b-form-group                        
                                label="Email Address" 
                                label-for="email">
                                <b-form-input 
                                    id="email"                                                          
                                    style="display:inline"
                                    v-model="newUser.email"
                                    :state="registerStates.email"
                                    placeholder="Email Address"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                        <b-col cols="6">
                            <b-form-group                        
                                label="Confirm Email Address" 
                                label-for="confirmEmail">
                                <b-form-input 
                                    id="confirmEmail"                                                          
                                    style="display:inline"
                                    v-model="confirmEmail"
                                    :state="registerStates.confirmEmail"
                                    placeholder="Email Address"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                    </b-row>     
                    <b-row>
                        <b-col cols="6">
                            <b-form-group                        
                                label="Password" 
                                label-for="password">
                                <b-form-input
                                    type="password" 
                                    id="password"                                                          
                                    style="display:inline"
                                    v-model="newUser.password"
                                    :state="registerStates.password"
                                    placeholder="Password"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                        <b-col cols="6">
                            <b-form-group                        
                                label="Confirm Password" 
                                label-for="confirmPassword">
                                <b-form-input
                                    type="password" 
                                    id="confirmPassword"                                                          
                                    style="display:inline"
                                    v-model="confirmPassword"
                                    :state="registerStates.confirmPassword"
                                    placeholder="Password"
                                >
                                </b-form-input> 
                            </b-form-group>
                        </b-col>
                    </b-row> 
                    <b-row>
                        <b-button 
                             style="margin: 0.6rem auto; padding: 0.5rem 2rem;"
                            :disabled="registering"
                            variant="primary"
                            @click="createProfile()"
                            ><spinner color="#FFF" v-if="registering" style="margin:0; padding: 0; height:2rem; transform:translate(0px,-25px);"/>
                            <span style="font-size: 20px;" v-else>Create Profile</span>
                        </b-button>
                    </b-row>
                </b-card-body>
            </b-card>

            <b-card v-else-if="signIn && !signUp" class="login-section my-4" :key="updateLoginInfo">
                <b-card-header class="text-center">
                    Login
                </b-card-header>
                <b-card-body>
                    <b-row class="my-2">
                        <b-form-group 
                            style="margin:0 auto;"                       
                            label="Email Address" 
                            label-for="email">
                            <b-form-input 
                                id="email"                                                          
                                style="display:inline"
                                v-model="credentials.email"
                                :state="loginStates.email"
                                placeholder="Email Address"
                            >
                            </b-form-input> 
                        </b-form-group>
                    </b-row>     
                    <b-row class="mt-4">
                        <b-form-group 
                            style="margin:0 auto;"                       
                            label="Password" 
                            label-for="password">
                            <b-form-input
                                type="password"
                                id="password"                                                          
                                style="display:inline"
                                v-model="credentials.password"
                                :state="loginStates.password"
                                placeholder="Password"
                            >
                            </b-form-input> 
                        </b-form-group>
                    </b-row> 
                    <b-row>
                        <b-button                                                        
                            style="margin:3rem auto 0 auto; padding: 0.25rem 2rem; width: 50%;" 
                            :disabled="authenticating"
                            variant="primary"
                            @click="authenticate()"
                            ><spinner color="#FFF" v-if="authenticating" style="margin:0; padding: 0; height:2rem; transform:translate(0px,-25px);"/>
                            <span style="font-size: 20px;" v-else>Sign In</span>
                        </b-button>
                    </b-row>    
                </b-card-body>
            </b-card>           
            
        </b-container>

        <disclaimer :disclaimer="disclaimer" :declineButton="true" @acceptTerms="areTermsAccepted"/>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { SessionManager } from "@/components/utils/utils";
import Spinner from '@/components/utils/Spinner.vue'

import Disclaimer from "../Disclaimer.vue"

import { namespace } from "vuex-class";   
import "@/store/modules/common";
import { loginStatesInfoType, userCredentialsInfoType, userInfoType, userStatesInfoType } from '@/types/Admin';
const commonState = namespace("Common");


import { vehicleTypeOptions } from '../utils/enums';

@Component({
    components:{
        Spinner, 
        Disclaimer,
    }
})
export default class LandingPage extends Vue {
    
    @commonState.State
    public user!: userInfoType;

    confirmEmail = ''
    confirmPassword = ''
    message = '';
    
    disclaimer = {show: false}

    isLoggedIn = false;
    pageReady = false;

    signUp = false;
    signIn = false;

    registering = false;
    authenticating = false;

    credentials = {} as userCredentialsInfoType;
    newUser = {} as userInfoType;  
    vehicleTypeOptions; 

    updateRegisterInfo = 0; 
    updateLoginInfo = 0; 
    
    dismissCountDown =0
    alertType=""

    registerStates = {} as userStatesInfoType;
    loginStates = {} as loginStatesInfoType;
    
    created() {
        this.vehicleTypeOptions = vehicleTypeOptions;
    }

    async mounted() {
        this.pageReady = false;
        this.registering = false;
        this.authenticating = false;        
        this.message = "";
        this.registerStates = {} as userStatesInfoType;
        this.loginStates = {} as loginStatesInfoType;

        if(this.$store.state.Common.token)            
            await SessionManager.getUserInfo(this.$store);
        
        if(this.user?.id){
            this.isLoggedIn = true
            this.$router.push({ name: "manage-bookings" });
        }else{
            this.isLoggedIn = false;
            this.pageReady = true;
        } 
    }
  
    public login() {         
        this.clearStates();  
        this.signUp = false;
        this.signIn = true;         
    }

    public authenticate() {
        if (this.checkLoginStates()){       
            
            this.message = "";
            this.authenticating = true;

            this.$http.post('/auth/login',this.credentials)
            .then(response =>{
                this.$router.push({ name: "manage-bookings" });
                this.authenticating = false;
            },err =>{
                this.message = err.response.data.detail;
                this.alertType="danger";
                this.dismissCountDown = 3;
                this.authenticating = false;
            });       
        }          
    }

    public register() {      
        this.clearStates();
        this.signIn = false;
        this.signUp = true;                 
    }

    public areTermsAccepted(accept){
        if(accept==true){
            this.registering = true;
            this.$http.post('/user/register',this.newUser)
            .then(response =>{
                this.registering = false;
                this.alertType="success";
                this.dismissCountDown = 3;
                this.message = "You have successfully enrolled in the parking reservation system."
                this.signUp = false;
                this.signIn = true; 
            },err =>{              
                this.message = err.response.data.detail;
                if(err.response.status==409 && err.response?.data?.detail?.split('Key')?.length>1) this.message = err.response.data.detail.split('Key')[1];
                this.alertType="danger";
                this.dismissCountDown = 3;
                this.registering = false;
            });
        }
    }

    public createProfile() {       
        if (this.checkRegisterStates()){
            this.disclaimer.show = true                
        }
    }

    public checkRegisterStates(){

        let stateCheck = true;
    
        this.registerStates.email = !(this.newUser.email)? false : null;
        this.registerStates.confirmEmail = !(this.newUser.email && this.confirmEmail && this.newUser.email == this.confirmEmail)? false : null;        
        this.registerStates.firstName = !(this.newUser.first_name)? false : null;
        this.registerStates.lastName = !(this.newUser.last_name)? false : null;
        this.registerStates.vehicleType = !(this.newUser.vehicle_type)? false : null;
        this.registerStates.licensePlate = !(this.newUser.license_plate)? false : null;
        this.registerStates.password = !(this.newUser.password)? false : null;
        this.registerStates.confirmPassword = !(this.newUser.password && this.confirmPassword && this.newUser.password == this.confirmPassword)? false : null;      
      
        this.updateRegisterInfo ++;
        for(const field of Object.keys(this.registerStates)){
            if(this.registerStates[field]==false)
                stateCheck = false;
        }   
        return stateCheck;            
    }

    public checkLoginStates(){

        let stateCheck = true;
    
        this.loginStates.email = !(this.credentials.email)? false : null;
        this.loginStates.password = !(this.credentials.password)? false : null;      
      
        this.updateLoginInfo ++;
        for(const field of Object.keys(this.loginStates)){
            if(this.loginStates[field]==false)
                stateCheck = false;
        }      

        return stateCheck;            
    }

    public clearStates(){

        for(const field of Object.keys(this.registerStates)){
            this.registerStates[field] = null;                
        }    
        
        for(const field of Object.keys(this.loginStates)){
            this.loginStates[field] = null;                
        }
    }

    public countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
    }
  
}
</script>

<style lang="scss">
    label {
        font-size: 14pt;    
        margin-bottom: 0;
    }
    @media (max-width:600px){
       label {
            font-size: 10pt;    
            margin-bottom: 0;
        } 
    }

</style>

<style scoped lang="scss">
    @import "src/styles/common";

    .info-section {
        font-size: 24px;
        line-height: 1.6;
        margin: 0 auto;
        width: 60rem;
        border: 2px solid rgba($new-pale-grey, 0.3);
        border-radius: 18px;
        background-color: rgba(9, 109, 112, 0.877); 
        color: $new-white;
    }

    @media (max-width:600px){
       .info-section{
            font-size: 20px;
            line-height: 1.6;
            margin: 0 0 0 -0.5rem;
            max-width: 400px;
            border: 2px solid rgba($new-pale-grey, 0.3);
            border-radius: 18px;
            background-color: rgba(9, 109, 112, 0.877); 
            color: $new-white;
        }
    }

    .register-section {
        font-size: 24px;
        line-height: 1.6; 
        margin: 0 auto; 
        width: 60rem;
        border: 2px solid rgba($new-pale-grey, 0.3);
        border-radius: 18px;
        background-color: rgba(180, 208, 209, 0.507); 
        color: black;
    }
    @media (max-width:600px){
        .register-section {
            font-size: 24px;
            line-height: 1.6; 
            margin: 0 0 0 -0.5rem; 
            max-width: 400px;
            border: 2px solid rgba($new-pale-grey, 0.3);
            border-radius: 18px;
            background-color: rgba(180, 208, 209, 0.507); 
            color: black;
        }
    }


    .login-section {
        font-size: 24px;
        line-height: 1.6; 
        margin: 0 auto; 
        width: 30rem;
        border: 2px solid rgba($new-pale-grey, 0.3);
        border-radius: 18px;
        background-color: rgba(92, 61, 3, 0.5); 
        color: $new-white;
    }

    @media (max-width:600px){
        .login-section {
            font-size: 24px;
            line-height: 1.6; 
            margin: 0 0 0 -0.5rem; 
            max-width: 400px;
            border: 2px solid rgba($new-pale-grey, 0.3);
            border-radius: 18px;
            background-color: rgba(92, 61, 3, 0.5); 
            color: $new-white;
        }
    }

    .login-button {
        color: black;
        font-weight: 600;
        margin: 0 auto 0 auto;
        width: 10rem;
        border: 2px solid rgb(231, 231, 231);
        &:hover,
        &:focus {
            color: rgb(155, 48, 6);
            border-color: rgba(29, 17, 10, 0.904);

        }
        &:active {
            border: 2px solid rgba($new-white, 0.8);
        }
    }

    .info-section .card-header {
        background: rgb(23, 39, 43);
        color: white;
        border-radius: 10px !important;
        border:0px solid white;
    }

    .register-section .card-header {
        background: rgb(33, 62, 70);
        color: white;
        border-radius: 10px !important;
        border:0px solid white;
    }

    .login-section .card-header {
        background: rgb(138, 96, 34);
        color: white;
        border-radius: 10px !important;
        border:0px solid white;
    }
</style>

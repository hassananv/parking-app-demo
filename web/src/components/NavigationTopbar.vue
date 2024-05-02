<template>
    <header name="navigation-topbar" class="app-header">

        <nav class="navbar navbar-expand-lg navbar-dark">

            <div class="container-fluid">

                <a class="navbar-brand"
                    href="https://pacificintelligent.com/"
                    style="max-width: 50px">
                    <img 
                        src="../images/image.png"
                        width="50"
                        height="50"
                        alt=""/>
                </a>

                <div class="navbar-brand navbar-text">                    
                    Pacific Intelligent Automation Ltd.                 
                </div>
                <div class="navbar-brand navbar-text font-weight-bold">                    
                    Parking Reservation Application (Demo)                 
                </div>

                <div class="navbar-extra">
                    <div id="app-profile">
                        <div v-if="user && user.userName" style="padding-right: rem">
                            <b-row>
                                <b-col>
                                    <b-dropdown id="profileDropdown"
                                                text="Profile"
                                                variant="primary btn-transparent"
                                                menu-class="w-10"
                                                >
                                        <template #button-content >
                                            <span class="fa fa-user mx-3"></span><span class="mr-2"> {{ user.userName }}</span>
                                        </template>
                                        <b-dropdown-item variant="text" @click="manageBookings()">
                                            <b-icon-list-ul class="mr-3"/>Manage Bookings
                                        </b-dropdown-item>
                                        <b-dropdown-item variant="info" @click="addBookings()">
                                            <b-icon-calendar2-plus class="mr-3"/>Add Bookings
                                        </b-dropdown-item>
                                        <b-dropdown-item variant="success" @click="userProfile()">
                                            <b-icon-card-text class="mr-3"/>User Profile
                                        </b-dropdown-item>
                                        <b-dropdown-item variant="danger" @click="logout()">
                                            <b-icon-box-arrow-left  class="mr-3"/>Logout
                                        </b-dropdown-item>                                
                                    </b-dropdown>
                                </b-col>                                                       
                                <b-alert style="margin-top:0.8rem" :variant="alertType" :show="dismissCountDown"  @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">
                                    <b v-if="alertType=='success'">Saved <b-icon-check-square-fill/> </b>
                                    <b v-else>Error <b-icon-exclamation-circle-fill class="ml-1"/> </b>
                                </b-alert>
                            </b-row>                          

                        </div>
                    </div>
                </div>

                <button class="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNavAltMarkup"
                    aria-controls="navbarNavAltMarkup"
                    aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            
        </nav>
        
    </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import * as _ from 'underscore';

import { namespace } from "vuex-class";   
import "@/store/modules/common";
import { userInfoType } from "@/types/Admin";
const commonState = namespace("Common");

@Component
export default class NavigationTopbar extends Vue {
    
    @commonState.State
    public user!: userInfoType;

    @commonState.Action
    UpdateUser!: (newUser: userInfoType) => void 
    
    @commonState.Action
    UpdateToken!:(newToken: string) => void

    dismissCountDown =0
    alertType=""


    public logout() {
        if(this.$store.state.Common.logoutUrl){
            this.UpdateUser(null);
            this.UpdateToken(null);
            window.location.replace(this.$store.state.Common.logoutUrl);
        } 
        else
            this.$http.get('/auth/logout').then(response =>{
                this.UpdateUser(null);
                this.UpdateToken(null);
                this.$router.push({ name: "home" });
            }) 
    }

    public userProfile(){
        if(!location.pathname.includes('/user-profile'))
            this.$router.push({ name: "user-profile" });
    }

    public manageBookings(){
        if(!location.pathname.includes('/manage-bookings'))
            this.$router.push({ name: "manage-bookings" });
    }

    public addBookings(){
        if(!location.pathname.includes('/add-bookings'))
            this.$router.push({ name: "add-bookings" });
    }

   
    public countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
    }

   

}
</script>

<style>
.btn-transparent {
  background-color: transparent !important;
  border-color: #ccc !important;
}
</style>

<style scoped lang="scss">
@import "../styles/common";
.navbar {
  padding-right: 170px;
  background: #0c4433;
}
.navbar-brand:not(.logo) {
  flex: 1 1 auto;
}
.navbar-extra {
  display: inline-block;
  flex: 1 1 auto;
  text-align: right;
}
.navbar .navbar-extra {
  display: inline-block;
  flex: 1 1 auto;
  text-align: right;
}

#app-profile {
  color: $new-white;
}

.alert{
    font-weight: 800;
    height: 2.4rem;
    margin:0;
    padding: 0.4rem 1rem;
}
</style>
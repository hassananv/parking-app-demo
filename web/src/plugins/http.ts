import axios from "axios";
import { AxiosError , AxiosRequestConfig } from 'axios'
import Vue from 'vue'
import store from "@/store";
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import {AxiosAuthRefreshOptions} from 'axios-auth-refresh';



const refreshAuthLogic = failedRequest => axios.get('/oidc/token').then(response => {
    if (response.status == 200 && response.data.access_token == null) {
        location.replace(response.data.login_url);
        return Promise.resolve();
    }
    store.commit('Common/setToken',response.data.access_token);

    if (failedRequest != null)
        failedRequest.response.config.headers['Authorization'] = 'Bearer ' + response.data.access_token;
    return Promise.resolve();
}).catch((error: AxiosError) => {
    console.error(error);
});

const options: AxiosAuthRefreshOptions = {
    statusCodes: [ 401, 403]
}

function successInterceptor(config: AxiosRequestConfig) {
  
    const token = store.state.Common.token;    
    config.headers['Authorization'] = 'Bearer ' + token; 
  
    return config;
}

function configureInstance(){
    createAuthRefreshInterceptor(axios, refreshAuthLogic, options);    

    axios.interceptors.request.use(successInterceptor);    
    axios.defaults.baseURL = process.env.BASE_URL +'api/v1'
    return axios;    
}

const httpInstance = configureInstance();

export default {
    install () {
        Vue.prototype.$http = httpInstance
    }
};


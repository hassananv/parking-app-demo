import { userInfoType } from '@/types/Admin';
import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

@Module({
    namespaced: true
})
class Common extends VuexModule {

    public token = '';
    public user = {} as userInfoType; 
    public currentDate: string = '' 
   
	@Mutation
	public setToken(token): void {   
	  this.token = token
	}
	@Action
	public UpdateToken(newToken): void {
	   this.context.commit('setToken', newToken)
	}
  
    @Mutation
    public setUser(user: userInfoType): void {
        this.user = user;
    }
    @Action
    public UpdateUser(newUser: userInfoType) {
        this.context.commit("setUser", newUser);
    }
    
    @Mutation
	public setCurrentDate(currentDate: string): void {   
	  this.currentDate = currentDate
	}
	@Action
	public UpdateCurrentDate(newCurrentDate: string): void {
	   this.context.commit('setCurrentDate', newCurrentDate)
	}
}

export default Common
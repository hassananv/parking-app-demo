import Axios from "axios";


export const SessionManager = {   

    getUserInfo: async function(store) {
        try {
            var response = await Axios.get('/user/info');
                        
            const user = response.data;             

            if (user.id) {        
                const userName = capitalize(user.first_name) + " " + capitalize(user.last_name);
                user.userName = userName
                store.commit("Common/setUser", user); 

            }
            return {userId:user.id};
        }
        catch (error) {
            console.log(error);
            return {userId:null};
        }
    }
}

function capitalize(str: string){	
	if(str)
		return str.charAt(0).toUpperCase() + (str.slice(1));
	else
		return ''	
}

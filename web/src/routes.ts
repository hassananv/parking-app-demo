import LandingPage from "@/components/home/LandingPage.vue";
import UserProfile from "@/components/user/UserProfile.vue";
import ManageBookingsPage from "@/components/pages/ManageBookingsPage.vue";
import AddBookingsPage from "@/components/pages/AddBookingsPage.vue";
import { SessionManager } from "@/components/utils/utils";
import VueResource from 'vue-resource';
import store from "@/store";


async function authGuard(to: any, from: any, next: any) {
  var result = await SessionManager.getUserInfo(store);
  
  if (result?.userId)
    next();
  else
    next({ path: '/' });
}

const routes = [
    {
      path: "/",
      name: "home",
      component: LandingPage
    },
    {
      path: "/parking-app",
      component: LandingPage
    },
    {
      path: "/user-profile",
      name: "user-profile",
      beforeEnter: authGuard,
      component: UserProfile,      
    },
    {
      path: "/manage-bookings",
      name: "manage-bookings",
      beforeEnter: authGuard,
      component: ManageBookingsPage
    },   
    {
      path: "/add-bookings",
      name: "add-bookings",
      beforeEnter: authGuard,
      component: AddBookingsPage
    }
   
];

export default routes;

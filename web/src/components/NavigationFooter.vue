<template>
  <footer name="navigation-footer">
    <nav  class="navbar navbar-expand-lg navbar-dark">
      <!-- Navbar content -->
      <ul class="navbar-nav">
        <li class="nav-item">
          <a
            name="disclaimer" class="nav-link" @click="disclaimer.show = true" style="cursor: pointer;"
            >Disclaimer</a
          >
        </li>
        <li class="nav-item">
          <a
            name="disclaimer" class="nav-link" @click="disclaimer.show = true" style="cursor: pointer;"
            >Privacy</a
          >
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            href="https://pacificintelligent.com/"
            target="_blank"
            >Copyright</a
          >
        </li>
        <li class="nav-item">
          <a name="contact-us" class="nav-link" @click="contactUs = true" style="cursor: pointer;">
            Contact Us</a>
        </li>
      </ul>
      <div class="text-info ml-auto"> Copyright <b-badge variant="info" style="transform:translate(0,-2px); border-radius:10px;" >c</b-badge> 2022 Pacific Intelligent Automation Ltd.</div>
    </nav>

    <b-modal size="lg" v-model="contactUs" header-class="bg-info">
      <template v-slot:modal-title>
        <h1 class="mb-0 text-primary">General and Technical Enquiries</h1>
      </template>
      <div class="m-3">
        <p>
          Please submit your enquiries through the  
          <a
            href="https://pacificintelligent.com/contact/"
            target="_blank"
          >Contact</a> 
          page on our website.           
        </p> 
        <p>
          Or Email us at:
          <a
            href="mailto:info@pacificintelligent.com"
          > info@pacificintelligent.com </a>
        </p>        
      </div>
      <template v-slot:modal-footer>
        <b-button variant="primary" @click="contactUs = false">Close</b-button>
      </template>
      <template v-slot:modal-header-close>
        <b-button
          variant="primary"          
          @click="contactUs = false"
          >&times;</b-button
        >
      </template>
    </b-modal>

    <disclaimer :disclaimer="disclaimer" :declineButton="false"/>

  </footer>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Disclaimer from "./Disclaimer.vue"

@Component({
    components:{
      Disclaimer
    }
})
export default class NavigationFooter extends Vue {
  contactUs = false;
  disclaimer = {show: false}
  mounted() {
    this.contactUs = false;
    this.disclaimer.show = false;
  }

}
</script>
<style scoped lang="scss">
.navbar {
  padding-right: 170px;
  background: #0c4433;
}
</style>
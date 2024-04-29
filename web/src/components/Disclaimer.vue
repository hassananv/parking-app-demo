<template>

    <b-modal class="modal" size="xl" v-model="disclaimer.show" header-class="bg-danger" no-close-on-backdrop hide-header-close>
      <template v-slot:modal-title>
        <h1 class="mb-0 text-white">Disclaimer / Terms of Use</h1>
      </template>
      <div class="m-3 h3" style="">        
        This application is for <i class="text-danger">demo</i> purposes only. It is not referring to any actual parking lot.         
      </div>
      
      <div class="mx-3 mt-5 h3 text-primary">Warranty Disclaimer</div>
      <div class="mx-3 text-justify">
        This application is provided by Pacific Intelligent Automation Ltd., 
        Greater Vancouver Area, British Columbia, Canada as a <i class="text-danger">demo</i> 
        of its custom application development capabilities.
      </div>
      <div class="mx-3 mt-2 text-justify">  
        This application and all of the information it contains are provided "as is" 
        without warranty of any kind, whether express or implied. 
        All implied warranties, including, without limitation, implied warranties of 
        merchantability, fitness for a particular purpose, and non-infringement, 
        are hereby expressly disclaimed. 
        Links and references to any other websites are provided for information only 
        and listing shall not be taken as endorsement of any kind. 
        Pacific Intelligent Automation Ltd. is not responsible for the content or reliability 
        of the linked websites and does not endorse the content, products, services or views 
        expressed within them.
      </div>

      <div class="mx-3 mt-5 h3 text-primary">Limitation of Liabilities</div>
      <div class="mx-3 text-justify">
        Under no circumstances will Pacific Intelligent Automation Ltd. be liable to 
        any person or business entity for any direct, indirect, special, incidental, 
        consequential, or other damages based on any use of this website or 
        any other website to which this site is linked, including, 
        without limitation, any lost profits, business interruption, 
        or loss of programs or information, even if Pacific Intelligent Automation Ltd. 
        has been specifically advised of the possibility of such damages.
      </div>

      <div class="mx-3 mt-5 h3 text-primary">Privacy Policy</div>
      <div class="mx-3 text-justify">
        The personal information collected through this portal is for the purposes of creating, verifying, and administering your account.
      </div>

      <div class="mx-3 mt-5 h3 text-primary">Terms of Use</div>
      <div class="mx-3 text-justify">
        Your acceptance of these Terms of Use and your express and unconditional undertaking to Pacific Intelligent Automation Ltd. Services to comply with them.
      </div>

      <div class="mx-3 mt-5 h3 text-primary">Account and Access</div>
      <div class="ml-5 mr-3 text-justify">
        <ul>
          <li>You may only use the Services through your own registered account. You may not share your registered account information or allow any other person to use your account.</li>
          <li>Your use of the Services will be tracked and logged to ensure the security and integrity of the Services.</li>
        </ul>
      </div>
        

      <div class="mx-3 mt-5 h3 text-primary">Data Security</div>
      <div class="ml-5 mr-3 text-justify">
        <ul>
          <li>Your use of the Services must not disrupt the operation of the Services or their accessibility to others. You must take reasonable precautions to ensure that all material you upload through the Services is free from viruses or other malicious code.</li>
          <li>Data scraping, data mining, framing, mirroring and deep linking of any content accessed through the Services are strictly prohibited.</li>
        </ul>
      </div>
      
      <div class="mx-3 mt-5 h3 text-primary">Termination</div>
      <div class="ml-5 mr-3 text-justify">
        <ul>
          <li>You may deactivate your registered user account at any time by <a href="mailto:info@pacificintelligent.com"> contacting us </a>. Following deactivation, Pacific Intelligent Automation Ltd. may retain your account information to ensure the security and integrity of the Services.</li>
          <li>Pacific Intelligent Automation Ltd. may suspend or deactivate your use of the Services at any time without notice.</li>
          <li>Pacific Intelligent Automation Ltd. reserves the right to terminate the Services without notice.</li>
        </ul>
      </div>

      <template v-slot:modal-footer>
        <b-button v-if="declineButton" class="mr-auto" variant="warning" size="lg" @click="decline()">Decline</b-button>
        <b-button variant="success" size="lg" @click="accept()">Accept</b-button>
      </template>
    </b-modal>

</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
@Component
export default class Disclaimer extends Vue {

  @Prop({required: true})
  disclaimer: any

  @Prop({required: true})
  declineButton: boolean
  
  accept() {
    this.$emit('acceptTerms',true)
    this.disclaimer.show = false
  }

  decline() {
    this.$emit('acceptTerms',false)
    this.disclaimer.show = false
  }


}
</script>
<style scoped lang="scss">

  ::v-deep {
    @media (max-width:600px){
      .modal{
        max-width: 600px;
        margin:0 0 0 0.2rem;
      }
    }
  }
</style>
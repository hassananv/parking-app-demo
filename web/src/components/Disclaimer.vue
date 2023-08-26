<template>

    <b-modal class="modal" size="xl" v-model="disclaimer.show" header-class="bg-danger" no-close-on-backdrop hide-header-close>
      <template v-slot:modal-title>
        <h1 class="mb-0 text-white">Disclaimer</h1>
      </template>
      <div class="m-3 h3" style="">        
        This application is for <i class="text-danger">demo</i> purposes only. It is not referring to any actual parking lot.         
      </div>
      
      <div class="mx-3 mt-5 h3">Warranty Disclaimer</div>
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

      <div class="mx-3 mt-5 h3">Limitation of Liabilities</div>
      <div class="mx-3 text-justify">
        Under no circumstances will Pacific Intelligent Automation Ltd. be liable to 
        any person or business entity for any direct, indirect, special, incidental, 
        consequential, or other damages based on any use of this website or 
        any other website to which this site is linked, including, 
        without limitation, any lost profits, business interruption, 
        or loss of programs or information, even if Pacific Intelligent Automation Ltd. 
        has been specifically advised of the possibility of such damages.
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
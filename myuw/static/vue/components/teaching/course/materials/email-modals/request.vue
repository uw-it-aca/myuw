<template>
  <b-modal
    :id="`emaillist_request_${sln}`"
    ref="request-modal"
    size="lg"
    title="Create Mailing List"
    title-class="h5 text-dark-beige myuw-font-encode-sans"
    @show="logClassEmailListRequest"
    @hidden="onHide()"
  >
    <template v-if="emailList.request_sent || requestSuccess">
      <div class="alert alert-success" role="alert">
        <font-awesome-icon :icon="faCheck" />
        Request submitted
      </div>
      <p>Please note:</p>
      <ul>
        <li class="mb-1">An email confirmation will be sent to {{netid}}@uw.edu</li>
        <li class="mb-1">Mailing lists may take up to 24 hours to activate</li>
      </ul>
    </template>
    <template v-else-if="!listView && !addError">
      <div v-if="!emailList.has_lists && emailList.has_joint">
        <b-alert variant="danger" :show="disableActions">
          This action is disabled while overriding as another user.
        </b-alert>
        <uw-request-joint v-model="formData" :email-list="emailList" />
      </div>
      <div v-else-if="!emailList.has_lists && !emailList.section_list.list_exists">
        <b-alert variant="danger" :show="disableActions">
          This action is disabled while overriding as another user.
        </b-alert>
        <uw-request-single-list
          v-model="formData"
          :email-list="emailList"
          @reqmulti="listView = true; formData = {}"
        />
      </div>
    </template>
    <template v-else-if="!addError">
      <uw-email-add-list v-model="formData" :email-list="emailList" />
    </template>
    <template v-else>
      <b-alert show variant="danger">
        An error has occurred. Please try again in a few minutes.
      </b-alert>
    </template>

    <template v-if="emailList.request_sent || requestSuccess" #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
      >Mailman help</a>
      <button type="button" class="btn btn-light"
        @click="$refs['request-modal'].hide()">Close</button>
    </template>

    <template v-else-if="!listView && !addError" #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
      >Mailman help</a>
      <button type="button" class="btn btn-light"
        @click="$refs['request-modal'].hide()">Close</button>
      <button type="button" class="btn btn-primary"
        :disabled="disableActions" @click="requestList()">Submit</button>
    </template>

    <template v-else-if="!addError" #modal-footer>
      <a
        href="https://itconnect.uw.edu/connect/email/resources/mailman/"
      >Mailman help</a>
      <button type="button" class="btn btn-light"
        @click="listView = false">
        <font-awesome-icon :icon="faArrowLeft" />Back
      </button>
      <button type="button" class="btn btn-light"
        @click="$refs['request-modal'].hide()">Close</button>
      <button type="button" class="btn btn-primary"
        :disabled="!hasAnyKeys(formData)"
        @click="requestCreateEmail({formData, onSuccess, onError})"
      >Submit</button>
    </template>

    <template v-else #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
      >Mailman help</a>
      <button type="button" class="btn btn-light"
        @click="$refs['request-modal'].hide()">Close</button>
    </template>
  </b-modal>
</template>

<script>
import {
  faCheck,
  faArrowLeft,
} from '@fortawesome/free-solid-svg-icons';
import {mapState, mapActions} from 'vuex';
import EmailAddList from './add_list.vue';
import RequestJointList from './request/joint.vue';
import RequestSingleList from './request/list.vue';

export default {
  components: {
    'uw-email-add-list': EmailAddList,
    'uw-request-joint': RequestJointList,
    'uw-request-single-list': RequestSingleList,
  },
  props: {
    emailList: {
      type: Object,
      required: true,
    },
    sln: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      listView: false,
      addError: false,
      requestSuccess: false,
      faCheck,
      faArrowLeft,
      formData: {},
    };
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      disableActions: (state) => state.disableActions,
    }),
  },
  methods: {
    // MUWM-5022
    // for a multi-course list, should return
    //  {section_joint_list: joint, section_id_A: <section_label>}
    // for single course list, return
    //  {section_joint_list: single, section_id_A: <section_label>}
    // Current code always returns {section_single_A: "2013,autumn,MUSEUM,700/A"}
    ...mapActions('emaillist', ['requestCreateEmail']),
    requestList() {
      if(this.formData.section_joint_list === "single"){
        this.requestSingle();
      } else if(this.formData.section_joint_list === "joint"){
        this.requestJoint();
      }
    },
    requestSingle() {
      this.requestCreateEmail({
        formData: {
          [`section_single_${this.emailList.section_list.section_id}`]:
            this.emailList.section_list.section_label,
        },
        onSuccess: this.onSuccess,
        onError: this.onError,
      });
    },
    requestJoint() {
      this.requestCreateEmail({
        formData: {
          'section_joint_list': "joint",
          [`section_id_${this.emailList.section_list.section_id}`]:
            this.emailList.section_list.section_label,
        },
        onSuccess: this.onSuccess,
        onError: this.onError,
      });
    },
    onSuccess() {
      this.requestSuccess = true;
    },
    onError() {
      this.addError = true;
    },
    onHide() {
      this.listView = false;
      this.addError = false;
      this.requestSuccess = false;
      this.formData = {};
    },
    logClassEmailListRequest() {
      this.$logger.classEmailList(this, "Request");
    }
  },
}
</script>
<template>
  <b-modal
    :id="`emaillist_request_${sln}`"
    ref="request-modal"
    title="Create Mailing List"
    @hidden="onHide()"
  >
    <template v-if="emailList.request_sent || requestSuccess">
      <b-alert variant="success" show>
        <font-awesome-icon :icon="faCheck" />
        Request submitted
      </b-alert>
      <p>Please note:</p>
      <ul>
        <li>An email confirmation will be sent to {{netid}}@uw.edu</li>
        <li>Mailing lists may take up to 24 hours to activate</li>
      </ul>
    </template>
    <template v-else-if="!listView && !addError">
      <div v-if="!emailList.has_lists && emailList.has_joint">
        <b-alert variant="danger" :show="disableActions">
          This action is disabled while overriding as another user.
        </b-alert>
        <b-form-group label="Request a single email list for:">
          <b-form-radio value="joint" checked>
            {{emailList.course_abbr}}
            {{emailList.course_number}}
            {{emailList.section_id}}
            <span v-for="(section, i) in emailList.joint_sections" :key="i">
              +
              {{section.course_abbr}}
              {{section.course_number}}
              {{section.section_id}}
            </span>
            <p>
              Mailing list address:
              {{emailList.joint_section_list.list_address}}@uw.edu
            </p>
          </b-form-radio>
          <b-form-radio value="single" checked>
            {{emailList.course_abbr}}
            {{emailList.course_number}}
            {{emailList.section_id}}
            <p>
              Mailing list address:
              {{emailList.section_list.list_address}}@uw.edu
            </p>
          </b-form-radio>
        </b-form-group>
      </div>
      <div v-else-if="!emailList.has_lists && !emailList.section_list.list_exists">
        <b-alert variant="danger" :show="disableActions">
          This action is disabled while overriding as another user.
        </b-alert>
        <p>
          <strong>
            Request a single email list for
            {{emailList.course_abbr}}
            {{emailList.course_number}}
            {{emailList.section_id}},
            {{titleCaseWord(emailList.quarter)}}
            {{emailList.year}}.
          </strong>
          <span v-if="!emailList.no_secondary_section && !emailList.has_lists">
            <br/>
            <span>
              Need more email lists for this class?
              <b-link @click="listView = true">
                Request multiple email lists.
              </b-link>
            </span>
          </span>
        </p>

        <ul>
          <li>
            Mailing list address:
            {{emailList.section_list.list_address}}@uw.edu
          </li>
          <li>Mailing list will stay synced with the official class list</li>
        </ul>
        <input type="hidden" :value="emailList.section_list.section_label"/>
      </div>
    </template>
    <template v-else-if="!addError">
      <uw-email-add-list v-model="selected" :email-list="emailList" />
    </template>
    <template v-else>
      <b-alert show variant="danger">
        An error has occurred. Please try again in a few minutes.
      </b-alert>
    </template>

    <template v-if="emailList.request_sent || requestSuccess" #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
         target="_blank"
      >Mailman help</a>
      <b-button variant="light" @click="$refs['request-modal'].hide()">
        Close
      </b-button>
    </template>

    <template v-else-if="!listView && !addError" #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
         target="_blank"
      >Mailman help</a>
      <b-button variant="light" @click="$refs['request-modal'].hide()">
        Close
      </b-button>
      <b-button :disabled="disableActions" variant="primary" @click="requestSingle()">
        Submit
      </b-button>
    </template>

    <template v-else-if="!addError" #modal-footer>
      <a v-out="'Mailman Help'"
         href="https://itconnect.uw.edu/connect/email/resources/mailman/" rel="help"
          target="_blank"
      >Mailman help</a>
      <b-button variant="outline-secondary" @click="listView = false">
        <font-awesome-icon :icon="faArrowLeft" />
        Back
      </b-button>
      <b-button variant="light" @click="$refs['request-modal'].hide()">
        Close
      </b-button>
      <b-button
        :disabled="selected.length === 0"
        variant="primary"
        @click="requestCreateEmail({list: selected, onSuccess, onError})"
      >
        Submit
      </b-button>
    </template>

    <template v-else #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
        target="_blank"
      >Mailman help</a>
      <b-button variant="light" @click="$refs['request-modal'].hide()">
        Close
      </b-button>
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

export default {
  components: {
    'uw-email-add-list': EmailAddList,
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
      selected: [],
    };
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      disableActions: (state) => state.disableActions,
    }),
  },
  methods: {
    ...mapActions('emaillist', ['requestCreateEmail']),
    requestSingle() {
      this.requestCreateEmail({
        list: [{
          key: `section_single_${this.emailList.section_list.section_id}`,
          label: this.emailList.section_list.section_label,
        }],
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
      this.selected = [];
    },
  },
}
</script>
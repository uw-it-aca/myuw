<template>
  <div>
    <b-modal
      :id="`emaillist_view_${sln}`"
      ref="view-modal"
      size="lg"
      :title="`${emailList.course_abbr} ${emailList.course_number} Mailing Lists`"
      title-class="h5 text-dark-beige myuw-font-encode-sans"
      @show="logClassEmailListOpen"
      @hidden="onHide()"
    >
      <template v-if="emailList.request_sent || requestSuccess">
        <b-alert variant="success" show>
          <font-awesome-icon :icon="faCheck" />
          Request submitted
        </b-alert>
        <p>Please note:</p>
        <ul>
          <li class="mb-1">An email confirmation will be sent to {{netid}}@uw.edu</li>
          <li class="mb-1">Mailing lists may take up to 24 hours to activate</li>
        </ul>
      </template>
      <template v-else-if="!addView">
        <div v-if="!emailList.is_primary && emailList.section_list.list_admin_url">
          <span>
            {{emailList.course_abbr}}
            {{emailList.course_number}}
            {{emailList.section_list.section_id}}
          </span>
          <span>
            <a :href="`mailto:${emailList.section_list.list_address}@uw.edu`">
              {{emailList.section_list.list_address}}@uw.edu
            </a>
            <a v-out="`Manage Email List for ${
                emailList.course_abbr
                } ${emailList.course_number} ${emailList.section_list.section_id}`"
              :href="emailList.section_list.list_admin_url"
            >Manage</a>
          </span>
        </div>

        <table v-if="emailList.is_primary" class="table table-sm table-hover">
          <thead>
            <tr>
              <th :id="`emaillist_section_${sln}`" class="w-50 border-0">Section</th>
              <th :id="`emaillist_maillist_${sln}`" class="border-0">Mailing List</th>
              <th :id="`emaillist_manage_${sln}`" class="border-0">
                <span class="sr-only">Manage list in Mailman</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="emailList.section_list.list_admin_url">
              <td :headers="`emaillist_section_${sln}`">
                {{emailList.course_abbr}}
                {{emailList.course_number}}
                {{emailList.section_list.section_id}}
              </td>
              <td :headers="`emaillist_maillist_${sln}`">
                <a :href="`mailto:${emailList.section_list.list_address}@uw.edu`">
                  {{emailList.section_list.list_address}}@uw.edu
                </a>
              </td>
              <td :headers="`emaillist_manage_${sln}`">
                <a v-out="`Manage Email List for ${
                      emailList.course_abbr
                    } ${emailList.course_number} ${emailList.section_list.section_id}`"
                  :href="emailList.section_list.list_admin_url"
                >Manage</a>
              </td>
            </tr>

            <template v-for="(email, i) in emailList.secondary_section_lists">
              <tr v-if="email.list_exists" :key="i">
                <td :headers="`emaillist_section_${sln}`">
                  {{emailList.course_abbr}}
                  {{emailList.course_number}}
                  {{email.section_id}}
                </td>
                <td :headers="`emaillist_maillist_${sln}`">
                  <a :href="`mailto:${email.list_address}@uw.edu`">
                    {{email.list_address}}@uw.edu
                  </a>
                </td>
                <td :headers="`emaillist_manage_${sln}`">
                  <a v-out="`Manage Email List for ${
                        emailList.course_abbr
                      } ${emailList.course_number} ${email.section_id}`"
                    :href="email.list_admin_url"
                  >Manage</a>
                </td>
              </tr>
            </template>
          </tbody>
        </table>

        <p>
          Need help with mailing lists?
          <a v-out="'Mailman Help'"
             href="https://itconnect.uw.edu/connect/email/resources/mailman/"
          >Mailman help documentation</a>
        </p>
      </template>

      <template v-else-if="!addViewError">
        <uw-email-add-list v-model="formData" :email-list="emailList" />
      </template>

      <template v-else>
        <b-alert show variant="danger">
          An error has occurred. Please try again in a few minutes.
        </b-alert>
      </template>


      <template v-if="emailList.request_sent || requestSuccess" #modal-footer>
        <a v-out="'Mailman Help'"
           href="https://itconnect.uw.edu/connect/email/resources/mailman/"
        >Mailman help</a>
        <button type="button" class="btn btn-light"
          @click="$refs['view-modal'].hide()">Close</button>
      </template>

      <template v-else-if="!addView" #modal-footer>
        <button v-if="emailList.total_course_wo_list"
          type="button" class="btn btn-primary"
          @click="addView=true"
        >
          Add Mailing List
        </button>
        <button type="button" class="btn btn-light"
          @click="$refs['view-modal'].hide()">Close</button>
      </template>

      <template v-else-if="!addViewError" #modal-footer>
        <button type="button" class="btn btn-outline-secondary"
          @click="addView=false">
          <font-awesome-icon :icon="faArrowLeft" />Back
        </button>
        <button type="button" class="btn btn-primary"
          :disabled="!hasAnyKeys(formData)"
          @click="requestCreateEmail({formData, onSuccess, onError})"
        >
          Submit
        </button>
        <button type="button" class="btn btn-light"
          @click="$refs['view-modal'].hide()">Close</button>
      </template>

      <template v-else #modal-footer>
        <a v-out="'Mailman Help'"
           href="https://itconnect.uw.edu/connect/email/resources/mailman/"
        >
          Mailman Help
        </a>
        <button type="button" class="btn btn-light"
          @click="$refs['view-modal'].hide()">Close</button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import {
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
      addView: false,
      addViewError: false,
      requestSuccess: false,
      formData: {},
      faArrowLeft,
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
    onHide() {
      this.addView = false;
      this.addViewError = false;
      this.requestSuccess = false;
      this.formData = {};
    },
    onSuccess() {
      this.requestSuccess = true;
    },
    onError() {
      this.addViewError = true;
    },
    logClassEmailListOpen() {
      this.$logger.classEmailList(this, "Manage");
    }
  }
}
</script>
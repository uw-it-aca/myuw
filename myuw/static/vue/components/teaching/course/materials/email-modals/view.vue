<template>
  <div>
    <b-modal
      :id="`emaillist_view_${sln}`"
      ref="view-modal"
      :title="`${emailList.course_abbr} ${emailList.course_number} Mailing Lists`"
      @hidden="onHide()"
    >
      <template v-if="!addView">
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
            <a :href="emailList.section_list.list_admin_url"
              target="_blank"
              :data-linklabel="`Manage Email List for ${
                emailList.course_abbr
                } ${emailList.course_number} ${emailList.section_list.section_id}`"
            >Manage</a>
          </span>
        </div>

        <table v-if="emailList.is_primary">
          <thead>
            <tr>
              <th :id="`emaillist_section_${sln}`">Section</th>
              <th :id="`emaillist_maillist_${sln}`">Mailing List</th>
              <th :id="`emaillist_manage_${sln}`">
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
                <a :href="emailList.section_list.list_admin_url"
                  target="_blank"
                  :data-linklabel="`Manage Email List for ${
                      emailList.course_abbr
                    } ${emailList.course_number} ${emailList.section_list.section_id}`"
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
                  <a :href="email.list_admin_url"
                    target="_blank"
                    :data-linklabel="`Manage Email List for ${
                        emailList.course_abbr
                      } ${emailList.course_number} ${email.section_id}`"
                  >Manage</a>
                </td>
              </tr>
            </template>
          </tbody>
        </table>

        <p>
          Need help with mailing lists?
          <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
            rel="help" target="_blank" data-linklabel="Mailman Help"
          >Mailman help documentation</a>
        </p>
      </template>

      <template v-else-if="!addViewError">
        <uw-email-add-list v-model="selected" :email-list="emailList" />
      </template>

      <template v-else>
        <b-alert show variant="danger">
          An error has occurred. Please try again in a few minutes.
        </b-alert>
      </template>

      <template v-if="!addView" #modal-footer>
        <b-button variant="primary"
          v-if="emailList.total_course_wo_list"
          @click="addView=true"
        >
          Add Mailing List
        </b-button>
        <b-button variant="light" @click="$refs['view-modal'].hide()">Close</b-button>
      </template>

      <template v-else-if="!addViewError" #modal-footer>
        <b-button @click="addView=false" variant="outline-secondary">
          <font-awesome-icon :icon="faArrowLeft" />
          Back
        </b-button>
        <b-button variant="primary"
          :disabled="selected.length === 0"
          @click="requestCreateEmail({list: selected, onError})"
        >
          Submit
        </b-button>
        <b-button variant="light" @click="$refs['view-modal'].hide()">Close</b-button>
      </template>

      <template v-else #modal-footer>
        <a href="http://watermelon.aca.uw.edu:8080/out?u=https%3A%2F%2Fitconnect.uw.edu%2Fconnect%2Femail%2Fresources%2Fmailman%2F&l=Mailman%20Help">
          Mailman Help
        </a>
        <b-button variant="light" @click="$refs['view-modal'].hide()">Close</b-button>
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
      selected: [],
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
      this.selected = [];
    },
    onError() {
      this.addViewError = true;
    }
  }
}
</script>
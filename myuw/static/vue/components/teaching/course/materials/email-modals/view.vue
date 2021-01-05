<template>
  <div>
    <b-modal
      :id="`emaillist_view_${sln}`"
      v-model="show"
      :title="`${emailList.course_abbr} ${emailList.course_number} Mailing Lists`"
    >
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
      <template #modal-footer>
        <b-button v-b-modal="`emaillist_request_${sln}`" @click="show=false">
          Add Mailing List
        </b-button>
        <button @click="show=false">Close</button>
      </template>
    </b-modal>
    <uw-request-model :email-list="emailList" :sln="sln" />
  </div>
</template>

<script>
import {
  faCheck,
} from '@fortawesome/free-solid-svg-icons';
import {mapState} from 'vuex';
import RequestModel from './request.vue';

export default {
  components: {
    'uw-request-model': RequestModel,
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
      show: false,
      faCheck,
    };
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      disableActions: (state) => state.disableActions,
    }),
  },
}
</script>
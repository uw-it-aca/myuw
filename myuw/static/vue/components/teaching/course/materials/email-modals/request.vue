<template>
  <b-modal
    :id="`emaillist_request_${sln}`"
    title="Create Mailing List"
  >
    <b-alert variant="danger" :show="disableActions">
      This action is disabled while overriding as another user.
    </b-alert>

    <div v-if="emailList.request_sent">
      <b-alert variant="success" :show="disableActions">
        <font-awesome-icon :icon="faCheck" />
        Request submitted
      </b-alert>
      <p>Please note:</p>
      <ul>
        <li>An email confirmation will be sent to {{netid}}@uw.edu</li>
        <li>Mailing lists may take up to 24 hours to activate</li>
      </ul>
    </div>
    <div v-else>
      <div v-if="!emailList.has_lists && emailList.has_joint">
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
        <p>
          <strong>
            Request a single email list for
            {{emailList.course_abbr}}
            {{emailList.course_number}}
            {{emailList.section_id}},
            {{ucfirst(emailList.quarter)}}
            {{emailList.year}}.
          </strong>
          <span v-if="!emailList.no_secondary_section && !emailList.has_lists">
            <br/>
            <span>
              Need more email lists for this class?
              <!-- TODO: add button event here -->
              <a href="#">
                Request multiple email lists.
              </a>
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
        <input type="hidden" value="{{emailList.section_list.section_label}}"/>
      </div>
      <div v-if="!emailList.no_secondary_section">
        <div v-show="!emailList.has_lists">
          <strong>
            Request multiple email lists, one for each section selected:
          </strong>
          <!-- TODO: continue from here https://github.com/uw-it-aca/myuw/blob/addf0042dd310a7d80c65636d8a6bf07b3d847d2/myuw/templates/handlebars/card/instructor_schedule/mailman/request_email_lists.html#L94 -->
        </div>
      </div>
    </div>
    <template #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
         rel="help" target="_blank" data-linklabel="Mailman Help"
      >Mailman help</a>
      <button>Close</button>
      <button v-if="!emailList.request_sent">Submit</button>
    </template>
  </b-modal>
</template>

<script>
import {
  faCheck,
} from '@fortawesome/free-solid-svg-icons';
import {mapState} from 'vuex';

export default {
  props: {
    emailList: {
      type: Array,
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
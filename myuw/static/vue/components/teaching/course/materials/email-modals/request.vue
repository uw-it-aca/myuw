<template>
  <b-modal
    :id="`emaillist_request_${sln}`"
    v-model="show"
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
        <b-form-group title="Request a single email list for:">
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
            {{titleCaseWord(emailList.quarter)}}
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
        <input type="hidden" :value="emailList.section_list.section_label"/>
      </div>
      <div v-if="!emailList.no_secondary_section">
        <div v-show="emailList.has_lists">
          <b-form-group
            v-slot="{ ariaDescribedby }"
            title="Request multiple email lists, one for each section selected:"
          >
            <b-form-checkbox
              v-model="allSelected"
              :indeterminate="indeterminate"
              aria-describedby="flavours"
              aria-controls="flavours"
              @change="toggleAll"
            >
              {{ allSelected ? 'Un-Select All' : 'Select All' }}
            </b-form-checkbox>
            <b-form-checkbox-group
              v-model="selected"
              :options="selectableEmailList"
              :aria-describedby="ariaDescribedby"
              stacked
            ></b-form-checkbox-group>
          </b-form-group>
        </div>
      </div>
    </div>
    <template #modal-footer>
      <a href="https://itconnect.uw.edu/connect/email/resources/mailman/"
         rel="help" target="_blank" label="Mailman Help"
      >Mailman help</a>
      <button v-if="!emailList.no_secondary_section && !emailList.has_lists">
        <font-awesome-icon :icon="faArrowLeft" />
        Back: request a single mailing list
      </button>
      <button @click="show = false">Close</button>
      <button v-if="!emailList.request_sent"
              :disabled="selected.length === 0"
      >
        Submit
      </button>
    </template>
  </b-modal>
</template>

<script>
import {
  faCheck,
  faArrowLeft,
} from '@fortawesome/free-solid-svg-icons';
import {mapState, mapActions} from 'vuex';

export default {
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
      faArrowLeft,
      selected: [],
      indeterminate: false,
      allSelected: false,
    };
  },
  computed: {
    ...mapState({
      netid: (state) => state.user.netid,
      disableActions: (state) => state.disableActions,
    }),
    selectableEmailList() {
      const options = [];
      if (this.emailList.section_list.list_exists) {
        options.push({
          text: `${this.emailList.course_abbr} ${
            this.emailList.course_number
          } ${this.emailList.section_list.section_id} - List already exists`,
          value: `section_single_${this.emailList.section_list.section_id}`,
          disabled: true,
        });
      } else {
        options.push({
          text: `${this.emailList.course_abbr} ${
            this.emailList.course_number
          } ${this.emailList.section_list.section_id}`,
          value: `section_single_${this.emailList.section_list.section_id}`,
        });
      }

      this.emailList.secondary_section_lists.forEach((section) => {
        if (section.list_exists) {
          options.push({
            text: `${this.emailList.course_abbr} ${
              this.emailList.course_number
            } ${section.section_id} - List already exists`,
            value: `secondary_single_${section.section_id}`,
            disabled: true,
          });
        } else {
          options.push({
            text: `${this.emailList.course_abbr} ${
              this.emailList.course_number
            } ${section.section_id}`,
            value: `secondary_single_${section.section_id}`,
          });
        }
      });

      return options;
    }
  },
  watch: {
    selected(newValue, oldValue) {
      if (newValue.length === 0) {
        this.indeterminate = false
        this.allSelected = false
      } else if (newValue.length === 
        this.selectableEmailList.filter((o) => !o.disabled).length
      ) {
        this.indeterminate = false
        this.allSelected = true
      } else {
        this.indeterminate = true
        this.allSelected = false
      }
    }
  },
  methods: {
    ...mapActions('emaillist', ['requestCreateEmail']),
    toggleAll(checked) {
      this.selected = checked ? 
        this.selectableEmailList.filter((o) => !o.disabled).map((o) => o.value) : [];
    },
  },
}
</script>
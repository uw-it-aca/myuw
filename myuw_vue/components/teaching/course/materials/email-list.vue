<template>
  <span v-if="section.email_list">
    <span>Email List:&nbsp;&nbsp;</span>
    <span v-if="
      section.email_list.section_list &&
      section.email_list.section_list.list_exists
    ">
      <span v-if="section.email_list.has_multiple_sections">
        <a v-uw-modal="`emaillist_view_${section.sln}`">
          Manage mailing lists
        </a>
        <uw-email-view-model :email-list="section.email_list" :sln="section.sln" />
      </span>
      <span v-else>
        <span>{{section.email_list.section_list.list_address}}@uw.edu</span>
        <a
          v-if="!section.pastTerm"
          v-out="'Manage Email List'"
          :href="section.email_list.section_list.list_admin_url"
          :title="`Manage Email List for ${
            section.email_list.course_abbr
          } ${section.email_list.course_number} ${
            section.email_list.section_list.section_id
          }`"
        >
          Manage
        </a>
      </span>
    </span>
    <span v-else-if="
      section.email_list.joint_section_list &&
      section.email_list.joint_section_list.list_exists
    ">
      <span>{{section.email_list.joint_section_list.list_address}}@uw.edu</span>
      <a
        v-if="!section.pastTerm"
        v-out="'Manage Email List (joint section)'"
        :href="section.email_list.joint_section_list.list_admin_url"
        :title="`Manage Joint Section Email List for ${
          section.email_list.course_abbr
        } ${section.email_list.course_number} ${
          section.email_list.joint_section_list.section_id
        }`"
      >
        Manage
      </a>
    </span>
    <span v-else-if="!section.pastTerm">
      <span v-if="section.email_list.has_secondary_lists">
        <a
          v-uw-modal="`emaillist_view_${section.sln}`">
          Manage mailing lists
        </a>
        <uw-email-view-model :email-list="section.email_list" :sln="section.sln" />
      </span>
      <span v-else>
        <a v-uw-modal="`emaillist_request_${section.sln}`">
          Create mailing lists
        </a>
        <uw-email-request-model :email-list="section.email_list" :sln="section.sln" />
      </span>
    </span>
  </span>
  <span v-else class="text-danger myuw-text-md">
    <font-awesome-icon :icon="faExclamationTriangle" />
    An error occurred with the
    <a v-out="`UW Mailman`" href="https://mailman.u.washington.edu/" target="_blank">
      email list</a>.
    Please try again later.
  </span>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import EmailRequestModel from './email-modals/request.vue';
import EmailViewModel from './email-modals/view.vue';

export default {
  components: {
    'uw-email-request-model': EmailRequestModel,
    'uw-email-view-model': EmailViewModel,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      faExclamationTriangle,
    };
  },
  computed: {
    emailSectionList() {
      return [this.section.email_list.section_list].concat(
          this.section.email_list.secondary_section_lists,
      );
    },
  },
};
</script>

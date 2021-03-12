<template>
  <li v-if="section.email_list">
    <span>Email List:&nbsp;&nbsp;</span>
    <span v-if="
      section.email_list.section_list &&
      section.email_list.section_list.list_exists
    ">
      <span v-if="section.email_list.has_multiple_sections">
        <b-link v-b-modal="`emaillist_view_${section.sln}`"
          v-out="'Manage Email List (multi_sections)'"
        >
          Manage mailing lists
        </b-link>
        <uw-email-view-model :email-list="section.email_list" :sln="section.sln" />
      </span>
      <span v-else>
        <span>{{section.email_list.section_list.list_address}}@uw.edu</span>
        <a :href="section.email_list.section_list.list_admin_url"
           target="_blank"
           v-out="'Manage Email List'"
           :title="`Manage Email List for ${
              section.email_list.course_abbr
            } ${section.email_list.course_number} ${
              section.email_list.section_list.section_id
            }`">
          Manage
        </a>
      </span>
    </span>
    <span v-else-if="
      section.email_list.joint_section_list &&
      section.email_list.joint_section_list.list_exists
    ">
      <span>{{section.email_list.joint_section_list.list_address}}@uw.edu</span>
      <a :href="section.email_list.joint_section_list.list_admin_url"
         target="_blank"
         v-out="'Manage Email List (joint section)'"
         :title="`Manage Joint Section Email List for ${
           section.email_list.course_abbr
          } ${section.email_list.course_number} ${
            section.email_list.joint_section_list.section_id
          }`">
         Manage
      </a>
    </span>
    <span v-else>
      <span v-if="section.email_list.has_secondary_lists">
        <b-link
          v-out="'Manage Email List (section with linked sections)'"
          v-b-modal="`emaillist_view_${section.sln}`">
          Manage mailing lists
        </b-link>
        <uw-email-view-model :email-list="section.email_list" :sln="section.sln" />
      </span>
      <span v-else>
        <b-link v-b-modal="`emaillist_request_${section.sln}`">
          Create mailing lists
        </b-link>
        <uw-email-request-model :email-list="section.email_list" :sln="section.sln" />
      </span>
    </span>
  </li>
</template>

<script>
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

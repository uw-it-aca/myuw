<template>
  <li v-if="section.email_list">
    <span>Email List:&nbsp;&nbsp;</span>
    <span v-if="section.email_list.section_list.list_exists">
      <span v-if="section.email_list.has_secondary_lists">
        <button v-b-modal="`emaillist_${section.sln}`">
          Manage mailing lists
        </button>
        <b-modal
          :id="`emaillist_${section.sln}`"
          v-model="show"
          :title="`${section.email_list.course_abbr} ${
            section.email_list.course_number} Mailing Lists`"
        >
          <table>
            <thead>
              <tr>
                <th :id="`emaillist_section_${section.sln}`">
                  Section
                </th>
                <th :id="`emaillist_maillist_${section.sln}`">
                  Mailing List
                </th>
                <th :id="`emaillist_manage_${section.sln}`">
                  Manage
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(emailSection, i) in emailSectionList"
                :key="i"
              >
                <td :headers="`emaillist_section_${section.sln}`">
                  {{ section.email_list.course_abbr }}
                  {{ section.email_list.course_number }}
                  {{ emailSection.section_id }}
                </td>
                <td :headers="`emaillist_maillist_${section.sln}`">
                  <a :href="`mailto:${emailSection.list_address}@uw.edu`">
                    {{ emailSection.list_address }}@uw.edu
                  </a>
                </td>
                <td :headers="`emaillist_manage_${section.sln}`">
                  <a :href="emailSection.list_admin_url">
                    Manage
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
          <template #modal-footer>
            <b-button
              variant="secondary"
              size="sm"
              class="float-right"
              @click="show=false"
            >
              Close
            </b-button>
            <b-button
              variant="primary"
              size="sm"
              class="float-right"
              @click="show=false"
            >
              Add Mailing List
            </b-button>
          </template>
        </b-modal>
      </span>
    </span>
  </li>
</template>

<script>
export default {
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

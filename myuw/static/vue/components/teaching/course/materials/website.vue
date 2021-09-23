<template>
  <span v-if="section.class_website_url">
    <span>Website:&nbsp;&nbsp;</span>
    <span>
      <a
        :href="section.class_website_url"
        :title="`Class Website of ${section.label}`"
        class="mr-2"
      >View class website</a>
      <span v-if="!pastTerm">
        <a
          v-out="'Update Course Website'"
          :title="`Update Class Website of ${section.label}`"
          @click="updateCourseWebsite"
        >Update</a>
      </span>
    </span>
  </span>
  <span v-else-if="section.pastTerm">
    <span>Website:&nbsp;&nbsp;</span>
    <span>None provided</span>
  </span>
  <span v-else-if="section.sln">
    <span>Website:&nbsp;&nbsp;</span>
    <a
      v-out="'Add Course Website'"
      :title="`Add Class Website for ${section.label}`"
      @click="addCourseWebsite"
    >Add</a>
    <div class="myuw-text-sm font-italic">
      A link to the course Canvas is automatically shown to students.
      Changes to the course website may take up to one hour to display
      on MyUW.
    </div>
  </span>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    pastTerm: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    addCourseWebsite() {
      window.open(
        "`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}&chanid=11`",
        'Add Class Website for ' + this.section.navtarget, 'width=700,height=400');
    },
    updateCourseWebsite() {
      window.open(
        "`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}&chanid=11`",
        'Update Class Website for ' + this.section.navtarget, 'width=700,height=400');
    },
  },
};
</script>

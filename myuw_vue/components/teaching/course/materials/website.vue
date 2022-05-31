<template>
  <span>
    <span>Website:&nbsp;&nbsp;</span>
    <span v-if="section.class_website_url">
      <a
        :href="section.class_website_url"
        :title="`Class Website of ${section.label}`"
        class="me-2"
      >View class website</a>
      <a
        v-if="!section.pastTerm"
        v-out="'Update Course Website'"
        :href="`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}`"
        :title="`Update Class Website of ${section.label}`"
        target="_blank"
      >Update</a>
    </span>
    <span v-else>
      <span v-if="section.pastTerm" class="text-muted">None provided</span>
      <span v-else-if="section.sln">
        <a
          v-out="'Add Course Website'"
          :href="`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}`"
          :title="`Add Class Website for ${section.label}`"
          target="_blank"
        >Add</a>
        <div class="myuw-text-sm fst-italic">
          A link to the course Canvas is automatically shown to students.
          Changes to the course website may take up to one hour to display
          on MyUW.
        </div>
      </span>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>

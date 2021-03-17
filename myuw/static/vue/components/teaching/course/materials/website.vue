<template>
  <li v-if="section.class_website_url">
    <span>Website:&nbsp;&nbsp;</span>
    <span>
      <a
        v-out="`View Course Website ${section.id}`"
        :href="section.class_website_url"
        target="_blank"
        :title="`Course Website: ${section.id}`"
      >View class website</a>
      <span v-if="!pastTerm">
        <a
          v-out="`Update Course Website ${section.id}`"
          target="_blank"
          :href="`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}&chanid=11`"
          :title="`Update Course Website: ${section.id}`"
        >Update</a>
      </span>
    </span>
  </li>
  <li v-else-if="section.pastTerm">
    <span>Website:&nbsp;&nbsp;</span>
    <span>None provided</span>
  </li>
  <li v-else-if="section.sln">
    <span>Website:&nbsp;&nbsp;</span>
    <a
      v-out="`Add Course Website ${section.id}`"
      target="_blank"
      :href="`https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/classurl.aspx?quarter=${section.quarter}+${section.year}&sln=${section.sln}&chanid=11`"
      :title="`Add Course Website: ${section.id}`"
    >Add</a>
    <div>
      A link to the course Canvas is automatically shown to students.
      Changes to the course website may take up to one hour to display
      on MyUW.
    </div>
  </li>
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
};
</script>

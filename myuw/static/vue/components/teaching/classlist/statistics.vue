<template>
  <div>
    <h4>
      Statistics for {{ currAbbr }} {{ courseNum }} {{ sectionId }}
    </h4>
    <p v-if="majors && majors.length">
      {{ majors[0].percent_students }}% of your students
      are {{ titleCaseWord(majors[0].major) }} majors.
    </p>
    <a :href="getUrl"
      v-out="'Course Dashboard'"
      target="_blank"
      :title="getLabel">
      View more statistics for
      {{ currAbbr }} {{ courseNum }} {{ sectionId }}
    </a>
  </div>
</template>
<script>
export default {
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    currAbbr: {
      type: String,
      required: true,
    },
    courseNum: {
      type: String,
      required: true,
    },
    sectionId: {
      type: String,
      required: true,
    },
    quarter: {
      type: String,
      required: true,
    },
    year: {
      type: Number,
      required: true,
    },
    majors: {
      type: Array,
      default: undefined,
    },
  },
  computed: {
    getUrl() {
      return 'https://coda.uw.edu/#' + this.year + '-' +
        this.quarter + '-' + this.currAbbr + '-' + this.courseNum +
        '-' + this.sectionId;
    },
    getLabel() {
      return 'Course Dashboard for ' + this.year + ' ' +
        this.quarter + ' ' + this.currAbbr + ' ' + this.courseNum +
        ' ' + this.sectionId;
    },
  },
};
</script>

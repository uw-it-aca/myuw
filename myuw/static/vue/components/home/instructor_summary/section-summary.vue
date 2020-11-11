<template>
  <h4>
    <div class="c{{section.color_id}} simplesquare" aria-hidden="true" />
    <a
     :href="`/teaching/${section.href}`"
     :future-nav-target="section.navtarget">
        {{ section.curriculum_abbr }}
        <span class="text-nowrap">
          {{ section.course_number }}
          {{ section.section_id }}
        </span>
     </a>
  </h4>

  <div>
    <span>
      {{ section.section_type }}
    </span>
    <span v-if="section.sln && section.sln.length">
      <a
        :href="getTimeScheHref(schedule, section)"
        :title="`Time Schedule for SLN ${section.sln}`"
        :data-linklabel="getTimeScheLinkLable(section)"
        target="_blank">
         {{ section.sln }}
      </a>
    </span>
  </div>

  <uw-meeting-info :section="section" />

</template>

<script>
import MeetingInfo from './meeting-info.vue';

export default {
  components: {
    'uw-meeting-info': MeetingInfo,
  },
  props: {
    schedule: {
      type: Object,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getTimeScheHref(schedule, section) {
      return ("http://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?QTRYR=" +
              quarterAbbr(schedule.quarter) + "+" +
              schedule.year + "&SLN=" + section.sln);
    },
    getTimeScheLinkLable(section) {
      return ("SLN " + section.sln + ": " + section.curriculum_abbr + " " +
             section.course_number + " " + section.section_id);
    }
  },
};
</script>

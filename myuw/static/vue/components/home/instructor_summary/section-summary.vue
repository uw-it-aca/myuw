<template>
  <h4>
    <div class="c{{section.color_id}} simplesquare" aria-hidden="true" />
    <a
     :href="`/teaching/${section.href}`"
     :future-nav-target="section.href">
      <span>
        {{ section.curriculum_abbr }}
        {{ section.course_number }}
        {{ section.section_id }}
      </span>
    </a>
  </h4>
  <div>
    <span>
      {{ ucfirst(section.section_type) }}
    </span>
    <span v-if="section.sln">
      <a
        :href="getTimeScheHref(schedule, section)"
        :title="`Time Schedule for SLN ${section.sln}`"
        target="_blank"
        :data-linklabel="getTimeScheLinkLable(section)">
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

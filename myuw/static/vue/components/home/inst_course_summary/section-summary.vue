<template>
  <div>
    <div v-if="section.is_primary_section">
      <h4>
        <div :class="`c${section.color_id} simplesquare`" />
        <a
          :href="`/teaching/${section.href}`"
          :future-nav-target="section.navtarget"
        >
          {{ section.curriculum_abbr }}
          <span class="text-nowrap">
            {{ section.course_number }}
            {{ section.section_id }}
          </span>
        </a>
      </h4>

      <div>
        <span>
          {{ section.section_type.toUpperCase() }}
        </span>
        <span v-if="section.sln">
          <a
            :href="getTimeScheHref(schedule, section)"
            :title="`Time Schedule for SLN ${section.sln}`"
            :data-linklabel="getTimeScheLinkLable(section)"
            target="_blank"
          >
            {{ section.sln }}
          </a>
        </span>
      </div>
    </div>
    <div v-else>
      <div :class="`c${section.color_id}`" />
      <a
        :href="`/teaching/${section.href}`"
        :future-nav-target="section.navtarget"
      >
        {{ section.section_id }}
      </a>
      <span v-if="section.sln">
        <a
          :href="getTimeScheHref(schedule, section)"
          :title="`Time Schedule for SLN ${section.sln}`"
          :data-linklabel="getTimeScheLinkLable(section)"
          target="_blank"
        >
          {{ section.sln }}
        </a>
      </span>
      <span>
        {{ section.section_type.toUpperCase() }}
      </span>
    </div>

    <uw-meeting-info :section="section" />
  </div>
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
      const qAbb = (!schedule.quarter || schedule.quarter.length === 0) ?
            '' : schedule.quarter.substring(0, 3).toUpperCase();
      return ('http://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?QTRYR=' +
              qAbb + '+' + schedule.year + '&SLN=' + section.sln);
    },
    getTimeScheLinkLable(section) {
      return ('SLN ' + section.sln + ': ' + section.curriculum_abbr + ' ' +
             section.course_number + ' ' + section.section_id);
    },
  },
};
</script>

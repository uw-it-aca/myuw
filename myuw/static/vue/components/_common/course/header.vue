<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <div>
        <h4
          class="h5 mb-0 text-dark-beige myuw-font-encode-sans">
          {{ section.curriculum_abbr }}
          {{ section.course_number }}
          {{ section.section_id }}
        </h4>
        <div>{{ section.course_title }}</div>
      </div>
      <div class="d-flex">
        <span class="mr-2">
          SLN
          <a
          :href="getTimeScheHref(section)"
          :title="`Time Schedule for SLN ${section.sln}`"
          :data-linklabel="getTimeScheLinkLable(section)"
          target="_blank"
        >
          {{ section.sln }}
        </a>
        </span>
        <div>
          <div :class="`px-1 border myuw-text-sm
          text-uppercase text-c${section.color_id}`"
          >
            {{ ucfirst(section.section_type) }}
          </div>
        </div>
        <b-button v-if="section.mini_card"
            variant="dark" size="sm"
            :aria-label="`Remove ${section.id} mini-card`"
            title="Click to remove this mini-card"
            @click="toggleMini(section)">
          <font-awesome-icon :icon="faTimes" />
        </b-button>
      </div>
    </div>
    <div v-if="section.summer_term" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Term
      </h5>
      <div class="flex-fill myuw-text-md">
        Summer
        {{
          section.summer_term
            .split('-')
            .map(ucfirst)
            .join('-')
        }}
      </div>
    </div>
    <div v-if="section.cc_display_dates" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Dates
      </h5>
      <div class="flex-fill myuw-text-md">
        {{ sectionFormattedDates(section) }}
      </div>
    </div>

    <div v-if="section.on_standby" class="d-flex">
      <h5
        :class="[!showRowHeading ? 'sr-only' : '']"
        class="w-25 font-weight-bold myuw-text-md"
      >
        Your Status
      </h5>
      <div class="flex-fill myuw-text-md">
        On Standby
      </div>
    </div>
  </div>
</template>

<script>
import {
  faTimes,
} from '@fortawesome/free-solid-svg-icons';
import dayjs from 'dayjs';
import {mapActions} from 'vuex';

export default {
  props: {
    schedule: {
      type: Object,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      faTimes,
    };
  },
  methods: {
    ...mapActions('inst_schedule', [
      'toggleMini',
    ]),
    slnHref() {
      const quarterAbbr = this.getQuarterAbbr(this.schedule.quarter);
      const queryParams =
        `QTRYR=${quarterAbbr}+${this.schedule.year}&SLN=${this.section.sln}`;
      return `https://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?${queryParams}`;
    },
    sectionFormattedDates(section) {
      return `${dayjs(section.start_date).format('MMM D')} - ${dayjs(
          section.end_date).format('MMM D')}`;
    },
  },
};
</script>

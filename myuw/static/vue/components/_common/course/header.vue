<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <div>
        <h4 class="h5 mb-0 text-dark-beige myuw-font-encode-sans">
          {{ section.curriculum_abbr }}
          {{ section.course_number }}
          {{ section.section_id }}
        </h4>
        <div>{{ section.course_title }}</div>
      </div>
      <div class="d-flex">
        <span class="mr-2">
          SLN <a target="_blank" :href="slnHref()">{{ section.sln }}</a>
        </span>
        <div>
          <div :class="`px-1 border myuw-text-sm
          text-uppercase text-c${section.color_id}`"
          >
            {{ ucfirst(section.section_type) }}
          </div>
          <div
            v-if="section.is_primary_section && section.for_credit"
            :class="`px-1 myuw-text-sm text-right
            text-uppercase text-c${section.color_id}`"
          >
            {{ section.credits }} CR
          </div>
        </div>
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
  },
  methods: {
    slnHref() {
      const quarterAbbr = this.getQuarterAbbr(this.schedule.quarter);
      const queryParams =
        `QTRYR=${quarterAbbr}+${this.schedule.year}&SLN=${this.section.sln}`;
      return `https://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?${queryParams}`;
    },
  },
};
</script>

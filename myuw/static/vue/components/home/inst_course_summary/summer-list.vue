<template>
  <div>
    <div v-if="getFulltermSections().length">
      <h4>
        Full-Term
      </h4>
      <uw-section-list
        :sections="getFulltermSections()"
        :mobile-only="mobileOnly"
      />
    </div>

    <div v-if="getAtermSections().length">
      <h4>
        A-Term
      </h4>
      <uw-section-list
        :sections="getAtermSections()"
        :mobile-only="mobileOnly"
      />
    </div>

    <div v-if="getBtermSections().length">
      <h4>
        B-Term
      </h4>
      <uw-section-list
        :sections="getBtermSections()"
        :mobile-only="mobileOnly"
      />
    </div>
  </div>
</template>

<script>
import SectionList from './section-list.vue';

export default {
  components: {
    'uw-section-list': SectionList,
  },
  props: {
    schedule: {
      type: Object,
      required: true,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getAtermSections() {
      return this.schedule.sections.filter(
          (section) => (section.summer_term === 'A-term'),
      );
    },
    getBtermSections() {
      return this.schedule.sections.filter(
          (section) => (section.summer_term === 'B-term'),
      );
    },
    getFulltermSections() {
      return this.schedule.sections.filter(
          (section) => (section.summer_term !== 'A-term' &&
                      section.summer_term !== 'B-term'),
      );
    },
  },
};
</script>

<template>
  <div>
    <div v-if="getFulltermSections().length">
      <h4>
        Full-Term
      </h4>
      <uw-section-list
        :sections="getFulltermSections()"
      />
    </div>

    <div v-if="getAtermSections().length">
      <h4>
        A-Term
      </h4>
      <uw-section-list
        :sections="getAtermSections()"
      />
    </div>

    <div v-if="getBtermSections().length">
      <h4>
        B-Term
      </h4>
      <uw-section-list
        :sections="getBtermSections()"
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

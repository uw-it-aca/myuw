<template>
  <uw-card v-if="showContent"
           :loaded="isReadyTagged"
           :errored="isErroredTagged"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3>
        {{ sectionData.currAbbr }} {{ sectionData.courseNum }}
        {{ sectionData.sectionId }},
        {{ sectionData.quarter }} {{ sectionData.year }}
      </h3>
      <div>
        <h4>SLN</h4>
        <span>{{ sectionData.sln }}</span>
      </div>
    </template>
    <template #card-body />
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    sectionLabel: {
      type: String,
      required: true,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
    }),
    ...mapState('classlist', {
      sectionData(state) {
        return state.value[this.sectionLabel];
      },
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.sectionLabel);
    },
    isErrored() {
      return this.isErroredTagged(this.sectionLabel);
    },
    showContent() {
      return this.instructor && this.sectionData.sections.length;
    },
    showError() {
      return this.statusCodeTagged(this.sectionLabel) !== 404;
    },
  },
  created() {
    if (this.instructor) {
      this.fetchClasslist(this.sectionLabel);
    }
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
  },
};
</script>

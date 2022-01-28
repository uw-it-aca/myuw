<template>
  <div v-if="isReady">
    <uw-tabs
        pills
        justified
        small
        nav-class="bg-white rounded"
        nav-wrapper-class="mb-2 border rounded p-0 w-75 mx-auto">
      <template #tabs>
        <uw-tab-list-button panel-id="all">
          All
        </uw-tab-list-button>
        <uw-tab-list-button panel-id="breaks">
          <font-awesome-icon
            :icon="faCircle"
            class="align-baseline text-mid-beige myuw-text-tiny"
          />
          Breaks
        </uw-tab-list-button>
      </template>
      <template #panels>
        <uw-tab-panel panel-id="all">
          <uw-calendar-cards :events="allEvents" />
        </uw-tab-panel>
        <uw-tab-panel panel-id="breaks">
          <uw-calendar-cards :events="breakEvents" />
        </uw-tab-panel>
      </template>
    </uw-tabs>
  </div>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import CalendarCards from './calendar-cards.vue';
import Tabs from '../_templates/tabs/tab-container.vue';
import TabListButton from '../_templates/tabs/tab-list-button.vue';
import TabPanel from '../_templates/tabs/tab-panel.vue';


export default {
  components: {
    'uw-calendar-cards': CalendarCards,
    'uw-tabs': Tabs,
    'uw-tab-list-button': TabListButton,
    'uw-tab-panel': TabPanel,
  },
  data() {
    return {
      faCircle,
      urlExtra: '',
    };
  },
  computed: {
    ...mapState('academic_events', {
      eventsByTerms: (state) => state.value,
    }),
    ...mapGetters('academic_events', {
      isReadyTagged: 'isReadyTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    allEvents() {
      return this.eventsByTerms[this.urlExtra].filter((e) => e.myuw_categories.all);
    },
    breakEvents() {
      return this.eventsByTerms[this.urlExtra].filter((e) => e.myuw_categories.breaks);
    },
  },
  created() {
    this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('academic_events', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
::v-deep .nav-link.active {
  background-color:#4d307f !important;
}
</style>
<template>
  <div v-if="isReady">
    <b-tabs>
      <b-tab title="All">
        <uw-calendar-cards :events="allEvents" />
      </b-tab>
      <b-tab>
        <template #title>
          <font-awesome-icon :icon="faCircle" />
          Breaks
        </template>
        <uw-calendar-cards :events="breakEvents" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import CalendarCards from './calendar-cards.vue';

export default {
  components: {
    'uw-calendar-cards': CalendarCards,
  },
  computed: {
    ...mapState('academic_events', {
      allEvents: (state) => state.value.filter((e) => e.myuw_categories.all),
      breakEvents: (state) => state.value.filter((e) => e.myuw_categories.breaks),
    }),
    ...mapGetters('academic_events', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  data() {
    return {
      faCircle,
    };
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('academic_events', ['fetch']),
  },
}
</script>
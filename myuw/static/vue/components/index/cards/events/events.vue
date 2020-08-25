<template>
  <uw-card v-if="(shownEvents.length > 0) || futureCalCount > 0"
           :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3>
        Events
      </h3>
    </template>
    <template v-if="shownEvents.length > 0" #card-body>
      <div>Showing events in the next 14 days.</div>
      <uw-list-events :events="shownEvents" />
    </template>
    <template v-else #card-body>
      <div v-if="futureCalLinks.length > 0">
        No events in the next 14 days.
        <strong>{{ futureCalCount }}</strong>
        {{ futureCalCount > 1 ? 'events' : 'event' }}
        from {{ futureCalLinks.length }} calendars in the next 30 days.
        <ul>
          <li v-for="(event, i) in futureCalLinks" :key="i">
            <a :href="event.base_url">{{ event.title }}</a>
          </li>
        </ul>
      </div>
      <div v-else>
        No events in the next 14 days.
        <strong>{{ futureCalCount }}</strong>
        {{ futureCalCount > 1 ? 'events' : 'event' }}
        from
        <span v-for="(event, i) in futureCalLinks" :key="i">
          <a :href="event.base_url">{{ event.title }}</a>
        </span>
        in the next 30 days.
      </div>
    </template>
    <!-- v-if condition is common with #card-footer -->
    <template v-if="hiddenEvents.length > 0" #card-disclosure>
      <b-collapse id="hidden_events_collapse" v-model="isOpen">
        <uw-list-events :events="hiddenEvents" />
        <div v-if="calLinks.length > 1">
          See all events from:
          <ul>
            <li v-for="(event, i) in calLinks" :key="i">
              <a :href="event.base_url">{{ event.title }}</a>
            </li>
          </ul>
        </div>
        <div v-else>
          See all events from <a :href="calLinks[0].url">
            {{ calLinks[0].title }}
          </a> calendar.
        </div>
      </b-collapse>
    </template>
    <!-- Open disclosure -->
    <template v-else-if="calLinks.length > 0" #card-disclosure>
      <div v-if="calLinks.length > 1">
        See all events from:
        <ul>
          <li v-for="(event, i) in calLinks" :key="i">
            <a :href="event.url">{{ event.title }}</a>
          </li>
        </ul>
      </div>
      <div v-else>
        See all events from <a :href="calLinks[0].url">
          {{ calLinks[0].title }}
        </a> calendar.
      </div>
    </template>
    <template v-if="hiddenEvents.length > 0" #card-footer>
      <button v-if="!isOpen" v-b-toggle.hidden_events_collapse
              :aria-label="`Show ${hiddenEvents.length} more ${
                hiddenEvents.length > 1 ? 'events' : 'event'}`"
              title="Show additional events"
      >
        SHOW ({{ hiddenEvents.length }}) MORE
      </button>
      <button v-else v-b-toggle.hidden_events_collapse
              aria-label="Show less"
              title="Hide additional events"
      >
        SHOW LESS
      </button>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../../containers/card.vue';
import ListEvents from './list-events.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-list-events': ListEvents,
  },
  data: function() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapState({
      shownEvents: (state) => state.events.value.shownEvents || [],
      hiddenEvents: (state) => state.events.value.hiddenEvents || [],
      futureCalCount: (state) => state.events.value.futureCalCount,
      futureCalLinks: (state) => state.events.value.futureCalLinks || [],
      calLinks: (state) => state.events.value.calLinks || [],
    }),
    ...mapGetters('events', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('events', ['fetch']),
  },
};
</script>

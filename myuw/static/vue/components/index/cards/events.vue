<template>
  <uw-card :loaded="isReady">
    <template #card-heading>
      <h3>
        Events
      </h3>
    </template>
    <template v-if="!isErrored" #card-body>
      <div v-if="shownEvents.length > 0">
        <div>Showing events in the next 14 days.</div>
        <ul>
          <li v-for="(event, i) in shownEvents" :key="i">
            <span>
              {{ acalDateFormat(event.start_date, event.end_date) }}
            </span>
            <div>
              <span v-if="event.is_all_day">
                All Day
              </span>
              <span v-else>
                {{ event.start_time }}
              </span>
              <span>
                <a :href="event.event_url">{{ event.summary }}</a>
              </span>
            </div>
            <span v-if="event.event_location">
              <em>
                <font-awesome-icon :icon="['fas', 'location-arrow']" />
                {{ event.event_location }}
              </em>
            </span>
            <span v-else>
              <em>Location not available</em>
            </span>
          </li>
        </ul>
        <div v-if="hiddenEvents.length > 0">
          <b-collapse id="hidden_events_collapse">
            <ul>
              <li v-for="(event, i) in hiddenEvents" :key="i">
                <span>
                  {{ acalDateFormat(event.start_date, event.end_date) }}
                </span>
                <div>
                  <span v-if="event.is_all_day">
                    All Day
                  </span>
                  <span v-else>
                    {{ event.start_time }}
                  </span>
                  <span>
                    <a :href="event.event_url">{{ event.summary }}</a>
                  </span>
                </div>
                <span v-if="event.event_location">
                  <em>
                    <font-awesome-icon :icon="['fas', 'location-arrow']" />
                    {{ event.event_location }}
                  </em>
                </span>
                <span v-else>
                  <em>Location not available</em>
                </span>
              </li>
            </ul>
            <div v-if="calLinks.length > 0">
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
          </b-collapse>
          <a v-b-toggle.hidden_events_collapse
             :aria-label="`Show ${hiddenEvents.length} more ${
               hiddenEvents.length > 1 ? 'events' : 'event'}`"
          >
            SHOW ({{ hiddenEvents.length }}) MORE
          </a>
        </div>
        <div v-else>
          <div v-if="calLinks.length > 0">
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
        </div>
      </div>
      <div v-else>
        <div v-if="futureCalLinks.length > 0">
          No events in the next 14 days.
          <strong>{{ futureCalCount }}</strong>
          {{ futureCalCount > 1 ? 'events' : 'event' }}
          from {{ futureCalLinks.length }} calendars in the next 30 days.
          <ul>
            <li v-for="(event, i) in futureCalLinks" :key="i">
              <a :href="event.url">{{ event.title }}</a>
            </li>
          </ul>
        </div>
        <div v-else>
          No events in the next 14 days.
          <strong>{{ futureCalCount }}</strong>
          {{ futureCalCount > 1 ? 'events' : 'event' }}
          from
          <span v-for="(event, i) in futureCalLinks" :key="i">
            <a :href="event.url">{{ event.title }}</a>
          </span>
          in the next 30 days.
        </div>
      </div>
    </template>
    <template v-else>
      <p>
        <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
        An error occurred and MyUW cannot load event information right now.
        Please try again later.
      </p>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      shownEvents: (state) => state.events.value.shownEvents,
      hiddenEvents: (state) => state.events.value.hiddenEvents,
      needsDisclosure: (state) => state.events.value.needsDisclosure,
      futureCalCount: (state) => state.events.value.futureCalCount,
      futureCalLinks: (state) => state.events.value.futureCalLinks,
      calLinks: (state) => state.events.value.calLinks,
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
    acalDateFormat(d1, d2) {
      let formattedDate = d1.format('MMMM D');
      if (d1.format('D') !== d2.format('D')) {
        formattedDate += d2.format(' - D');
      }
      return formattedDate;
    },
  },
};
</script>

<template>
  <uw-card v-if="!isReady || (shownEvents.length > 0 || futureCalCount > 0)"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Events
      </h2>
    </template>
    <template v-if="shownEvents.length > 0" #card-body>
      <p class="text-muted myuw-text-md">
        Showing events in the next 14 days.
      </p>
      <uw-list-events :events="shownEvents" />
      <div v-if="hiddenEvents == 0">
        <div v-if="calLinks.length > 1" class="mt-3">
          <p class="text-muted myuw-text-md">
            See all events from:
          </p>
          <ul class="list-unstyled mb-0 myuw-text-md">
            <li v-for="(event, i) in calLinks" :key="i" class="mb-1">
              <a :href="event.url">{{ event.title }}</a>
            </li>
          </ul>
        </div>
        <div v-else class="mt-3">
          <p class="text-muted myuw-text-md">
            See all events from
            <a :href="calLinks[0].url">
              {{ calLinks[0].title }}
            </a>
            calendar.
          </p>
        </div>
      </div>
    </template>
    <template v-else #card-body>
      <div v-if="futureCalLinks.length > 0">
        <p class="myuw-text-md">
          No events in the next 14 days.
          <strong>{{ futureCalCount }}</strong>
          {{ futureCalCount > 1 ? 'events' : 'event' }}
          from {{ futureCalLinks.length }} calendars in the next 30 days.
        </p>
        <ul class="list-unstyled mb-0 myuw-text-md">
          <li v-for="(event, i) in futureCalLinks" :key="i">
            <a :href="event.base_url">{{ event.title }}</a>
          </li>
        </ul>
      </div>
      <div v-else>
        <p class="myuw-text-md">
          No events in the next 14 days.
          <strong>{{ futureCalCount }}</strong>
          {{ futureCalCount > 1 ? 'events' : 'event' }}
          from
          <span v-for="(event, i) in futureCalLinks" :key="i">
            <a :href="event.base_url">{{ event.title }}</a>
          </span>
          in the next 30 days.
        </p>
      </div>
    </template>
    <!-- v-if condition is common with #card-footer -->
    <template v-if="hiddenEvents.length > 0" #card-disclosure>
      <uw-collapse
        id="hidden_events_collapse"
        v-model="isOpen"
      >
        <uw-list-events :events="hiddenEvents" />
        <div v-if="calLinks.length > 1" class="mt-3">
          <p class="text-muted myuw-text-md">
            See all events from:
          </p>
          <ul class="list-unstyled mb-0 myuw-text-md">
            <li v-for="(event, i) in calLinks" :key="i" class="mb-1">
              <a :href="event.url">{{ event.title }}</a>
            </li>
          </ul>
        </div>
        <div v-else class="mt-3">
          <p class="text-muted myuw-text-md">
            See all events from
            <a :href="calLinks[0].url">
              {{ calLinks[0].title }}
            </a>
            calendar.
          </p>
        </div>
      </uw-collapse>
    </template>
    <template v-else-if="calLinks.length > 0" #card-disclosure>
      <uw-collapse
        id="hidden_events_collapse"
        v-model="isOpen"
      >
        <div v-if="calLinks.length > 1">
          <p class="text-muted myuw-text-md">
            See all events from:
          </p>
          <ul class="myuw-text-md">
            <li v-for="(event, i) in calLinks" :key="i" class="mb-1">
              <a :href="event.url">{{ event.title }}</a>
            </li>
          </ul>
        </div>
        <div v-else>
          See all events from <a :href="calLinks[0].url">
            {{ calLinks[0].title }}
          </a> calendar.
        </div>
      </uw-collapse>
    </template>
    <template v-if="hiddenEvents.length > 0" #card-footer>
      <button v-uw-collapse.hidden_events_collapse
        type="button"
        class="btn btn-link btn-sm w-100 p-0 border-0 text-dark"
      >
        Future Events
        <font-awesome-icon v-if="isOpen" :icon="faChevronUp" />
        <font-awesome-icon v-else :icon="faChevronDown" />
      </button>
    </template>
  </uw-card>
</template>

<script>
import {
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';

import Card from '../../_templates/card.vue';
import Collapse from '../../_templates/collapse.vue';
import ListEvents from './list-events.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
    'uw-list-events': ListEvents,
  },
  data: function() {
    return {
      isOpen: false,
      faChevronUp,
      faChevronDown,
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
      statusCode: 'statusCode',
    }),
    showError: function() {
      return this.isErrored && this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('events', ['fetch']),
  },
};
</script>

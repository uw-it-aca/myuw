<template>
  <div>
    <template v-for="(eventTerm, i) in splitByTerm(events)">
      <uw-card v-if="!eventTerm.termBreak" :key="i" loaded>
        <template #card-heading>
          <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
            {{ eventTerm.quarter }} {{ eventTerm.year }}
          </h2>
        </template>
        <template #card-body>
          <ul class="list-unstyled mb-0 myuw-text-md">
            <li v-for="(event, j) in eventTerm.events" :key="j" class="mb-2">
              <div class="fw-bold">{{ formatDateRange(event.start, event.end) }}</div>
              <font-awesome-icon
                v-if="event.myuw_categories.breaks"
                :icon="faCircle"
                class="align-baseline text-mid-beige myuw-text-tiny"
              />
              <a v-out="event.label" :href="event.event_url">
                {{ event.summary }}
              </a>
            </li>
          </ul>
        </template>
      </uw-card>
      <div v-else :key="i" class="mb-3 text-center myuw-text-md">
        <font-awesome-icon :icon="faCircle" class="align-baseline text-mid-beige myuw-text-tiny" />
        <a v-out="eventTerm.events[0].label" :href="eventTerm.events[0].event_url">
          {{ eventTerm.events[0].summary }}
        </a>
        <div class="fw-bold">
          {{ formatDateRange(eventTerm.events[0].start, eventTerm.events[0].end) }}
        </div>
      </div>
      
    </template>
  </div>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    events: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      faCircle,
    };
  },
  methods: {
    splitByTerm(events) {
      let groupOrder = [];
      let eventsByGroupName = {};

      events.forEach((event) => {
        let groupName = `${event.year} ${event.quarter}`;
        if (event.myuw_categories.term_breaks) groupName += ' break';

        if (!(groupName in eventsByGroupName)) {
          eventsByGroupName[groupName] = [];
          groupOrder.push({
            name: groupName,
            quarter: event.quarter,
            year: event.year,
            termBreak: event.myuw_categories.term_breaks,
          });
        }

        eventsByGroupName[groupName].push(event);
      });

      return groupOrder.map((group) => ({
        events: eventsByGroupName[group.name],
        quarter: group.quarter,
        year: group.year,
        termBreak: group.termBreak,
      }));
    },
  },
};
</script>
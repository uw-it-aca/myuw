<template>
  <div>
    <template v-for="(eventTerm, i) in splitByTerm(events)">
      <uw-card v-if="!eventTerm.termBreak" :key="i" loaded>
        <template #card-heading>
          <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
            {{ eventTerm.quarter }} {{ eventTerm.year }}
          </h3>
        </template>
        <template #card-body>
          <ul class="list-unstyled mb-0 myuw-text-md">
            <li v-for="(event, j) in eventTerm.events" :key="j" class="mb-2">
              <div class="font-weight-bold">{{ formatDateRange(event.start, event.end) }}</div>
              <font-awesome-icon
                v-if="event.myuw_categories.breaks"
                :icon="faCircle"
                class="align-baseline text-dark-beige myuw-text-tiny"
              />
              <a :href="event.event_url" :label="event.label">
                {{ event.summary }}
              </a>
            </li>
          </ul>
        </template>
      </uw-card>
      <div v-else :key="i" class="mb-3 text-center myuw-text-md">
        <font-awesome-icon :icon="faCircle" class="align-baseline text-dark-beige myuw-text-tiny" />
        <a :href="eventTerm.event_url" :label="eventTerm.label">
          {{ eventTerm.events[0].summary }}
        </a>
        <div> {{ eventTerm.event_url }} </div>
        <div class="font-weight-bold">
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
      let groups = [];
      let currentTerm = '';

      const byGroup = {};
      events.forEach((event) => {
        const termName = event.year + ' ' + event.quarter;
        let groupName = termName;

        var newGroup = {
          year: event.year,
          quarter: event.quarter,
          events: [],
        };

        if (event.myuw_categories.term_breaks) {
          groupName = groupName + '-break';
          newGroup.termBreak = true;

          byGroup[groupName] = newGroup;
          groups.push(newGroup);
        } else if (termName !== currentTerm) {
          currentTerm = termName;

          byGroup[groupName] = newGroup;
          groups.push(newGroup);
        }

        byGroup[groupName].events.push(event);
      });

      return groups;
    },
  },
};
</script>
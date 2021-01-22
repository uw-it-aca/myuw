<template>
  <div>
    <template v-for="(eventTerm, i) in splitByTerm(events)">
      <uw-card v-if="!eventTerm.termBreak" :key="i" loaded>
        <template #card-heading>
          {{eventTerm.quarter}} {{eventTerm.year}}
        </template>
        <template #card-body>
          <ul>
            <li v-for="(event, j) in eventTerm.events" :key="j">
              {{formatDateRange(event.start, event.end)}}
              <font-awesome-icon v-if="event.myuw_categories.breaks" :icon="faCircle" />
              {{event.summary}}
            </li>
          </ul>
        </template>
      </uw-card>
      <div v-else :key="i">
        <font-awesome-icon :icon="faCircle" />
        {{eventTerm.events[0].summary}}
        {{formatDateRange(eventTerm.events[0].start, eventTerm.events[0].end)}}
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
    }
  },
  methods: {
    splitByTerm(events) {
      let groups = [];
      let currentTerm = "";

      const byGroup = {};
      events.forEach((event) => {
          const termName = event.year + " " + event.quarter;
          let groupName = termName;

          var newGroup = {
              year: event.year,
              quarter: event.quarter,
              events: []
          };

          if (event.myuw_categories.term_breaks) {
              groupName = groupName+"-break";
              newGroup.termBreak = true;

              byGroup[groupName] = newGroup;
              groups.push(newGroup);
          }
          else if (termName !== currentTerm) {
              currentTerm = termName;

              byGroup[groupName] = newGroup;
              groups.push(newGroup);
          }

          byGroup[groupName].events.push(event);
      });

      return groups;
    },
  },
}
</script>
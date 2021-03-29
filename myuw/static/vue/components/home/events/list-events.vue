<template>
  <ul class="list-unstyled mb-0 myuw-text-md">
    <li v-for="(event, i) in events" :key="i" class="mb-2">
      <strong>
        {{ acalDateFormat(event.start_date, event.end_date) }}
      </strong>
      <a
        v-out="'View event details'"
        :href="event.event_url"
        class="d-block"
        :title="generateLabel(event)"
      >
        <span v-if="event.is_all_day" class="text-dark font-weight-light
        d-inline-block mr-1"
        >
          All Day
        </span>
        <span v-else class="text-dark font-weight-light d-inline-block mr-1">
          {{ event.start_time }}
        </span>
        {{ event.summary }}
      </a>
      <em v-if="event.event_location" class="text-muted
      font-weight-light myuw-text-xs"
      >
        <font-awesome-icon :icon="faLocationArrow" size="sm" />
        {{ getLocation(event) }}
      </em>
    </li>
  </ul>
</template>

<script>
import {
  faLocationArrow,
} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    events: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      faLocationArrow,
    };
  },
  methods: {
    acalDateFormat(d1, d2) {
      let formattedDate = d1.format('MMMM D');
      if (d1.format('D') !== d2.format('D')) {
        formattedDate += d2.format(' - D');
      }
      return formattedDate;
    },
    generateLabel(event) {
      let label = '';

      if (event.start_date && event.end_date) {
        label += `${
          this.acalDateFormat(event.start_date, event.end_date)
        }. ${event.start_date.format('h:mm A')}. `;
      }

      label += `${event.summary}`;

      if (event.event_location.indexOf('.zoom.') >= 0) {
        label = '. Zoom';
      } else if (event.event_location) {
        label += `. ${event.event_location}`;
      } else {
        label += `. Location not available`;
      }

      return label;
    },
    getLocation(event) {
      if (event.event_location.indexOf('.zoom.') >= 0) {
        return 'Zoom';
      }
      return event.event_location;
    },
  },
};
</script>

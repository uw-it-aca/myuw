<template>
  <ul class="list-unstyled mb-0 myuw-text-md">
    <li v-for="(event, i) in events" :key="i" class="border-bottom pb-2 mb-2">
      <strong>
        {{ acalDateFormat(event.start_date, event.end_date) }}
      </strong>
      <a :href="event.event_url" class="d-block">
        <span v-if="event.is_all_day" class="text-dark d-inline-block mr-1">
          All Day
        </span>
        <span v-else class="text-dark d-inline-block mr-1">
          {{ event.start_time }}
        </span>
        {{ event.summary }}
      </a>
      <em v-if="event.event_location" class="text-muted
      font-weight-light myuw-text-xs"
      >
        <font-awesome-icon :icon="['fas', 'location-arrow']" size="sm" />
        {{ event.event_location }}
      </em>
      <em v-else class="text-muted font-weight-light myuw-text-xs">
        Location not available
      </em>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    events: {
      type: Array,
      required: true,
    },
  },
  methods: {
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

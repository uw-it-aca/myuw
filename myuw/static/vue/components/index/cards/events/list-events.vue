<template>
  <ul>
    <li v-for="(event, i) in events" :key="i">
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

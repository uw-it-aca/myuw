<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Academic Calendar
      </h3>
    </template>
    <template #card-body>
      <div v-for="(ev, index) in events" :key="index">
        {{ formatBannerDate(ev) }} <br>
        <a :href="ev.event_url">{{ ev.summary }}</a>
      </div>
    </template>
    <template #card-error>
      An error has occurred and MyUW cannot display calendar data right now.
      In the meantime, try the
      <a href="http://www.washington.edu/students/reg/calendar.html"
         data-linklabel="UW Academic Calendars"
         target="_blank"
      >UW Academic calendars page</a>.
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';
import dayjs from 'dayjs';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState('acad_calendar', {
      events: (state) => state.value,
    }),
    ...mapGetters('acad_calendar', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
    }),
    showCard: function () {
      return !this.isReady || (this.instructor && this.events.length > 0);
    },
    showError: function () {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('acad_calendar', ['fetch']),
    formatBannerDate(event) {
      let start = dayjs(event.start);
      let end = dayjs(event.end);
      let result = '';
      result += start.format('MMM D');
      if (event.is_all_day) {
        result += ' (' + start.format('dddd') + ')';
      } else {
        result += ' - ' + end.format('MMM D');
      }
      return result;
    },
  },
};
</script>

<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Academic Calendar
      </h2>
    </template>
    <template #card-body>
      <ul class="list-unstyled mb-0 myuw-text-md">
        <li v-for="(ev, index) in events" :key="index"
          class="mb-2">
          <strong>
          {{ formatBannerDate(ev) }}
          </strong>
          <a :href="ev.event_url" class="d-block">{{ ev.summary }}</a>
        </li>
      </ul>
      <div>
        <a href="/academic_calendar/"
           title="Navigate to Academic calendar"
        >View all events</a>
      </div>
    </template>
    <template #card-error>
      An error has occurred and MyUW cannot display calendar data right now.
      In the meantime, try the
      <a href="http://www.washington.edu/students/reg/calendar.html"
      >UW Academic Calendars</a> page.
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {
      urlExtra: 'current/',
    };
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
      events: function(state) {
        return state.academic_events.value[this.urlExtra];
      },
    }),
    ...mapGetters('academic_events', [
      'isReadyTagged',
      'isErroredTagged',
      'statusCodeTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    isErrored() {
      return this.isErroredTagged(this.urlExtra);
    },
    statusCode() {
      return this.statusCodeTagged(this.urlExtra);
    },
    showCard() {
      return this.instructor && (!this.isReady || this.events.length > 0);
    },
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.instructor) this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('academic_events', ['fetch']),
    formatBannerDate(event) {
      let start = event.start;
      let end = event.end;
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

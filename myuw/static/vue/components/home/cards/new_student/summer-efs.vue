<template>
  <uw-card
    v-if="!isReady || hasRegisterNotices"
    :loaded="isReady" :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h3 v-if="isErrored">
        Summer &amp; Early Fall Start
      </h3>
    </template>

    <template #card-body>
      <div v-for="notice in notices" :key="notice.id_hash">
        <h3>Review Critical Summer Registration Info</h3>
        <div v-html="notice.notice_body" />
      </div>

      <h3>Consider Early Fall Start</h3>
      <div>
        Early Fall Start is a single 5-credit intensive course held
        over four weeks before autumn quarter begins. Benefit from a small
        class size, an early introduction to college life, and a lighter
        course load during autumn quarter. The language courses may be
        particularly helpful to international students!
        <a href="http://www.outreach.washington.edu/efs/">Learn more about Early Fall Start and register</a>.
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState('notices', {
      notices: (state) => {
        return state.value.filter((notice) =>
          notice.location_tags.includes('checklist_summerreg'),
        );
      },
    }),
    ...mapGetters('notices', [
      'hasRegisterNotices',
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>

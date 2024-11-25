<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Notices</h2>
    </template>
    <template v-if="isReady" #card-body>
      <p v-if="noDisplayableNotices">You do not have any notices at this time.</p>
      <uw-notice-list v-else :notices="sortNotices(notices)" />
    </template>
    <template v-else #card-body>
      <p class="text-danger myuw-text-md">
        <font-awesome-icon :icon="faExclamationTriangle" />
        An error occurred and MyUW cannot load your notices right now. Please try again later.
      </p>
    </template>
  </uw-card>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';
import NoticeList from './notice-items.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-notice-list': NoticeList,
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  computed: {
    ...mapState('notices', {
      allNotices: (state) => state.value,
    }),
    showCard() {
      return this.isFetching || this.isReady && this.allNotices;
    },
    notices() {
      return this.allNotices.filter(
        (notice) =>
          notice.is_critical ||
          notice.category.includes('Legal') ||
          notice.location_tags.includes('notices_date_sort') ||
          notice.location_tags.includes('notice_banner')
      );
    },
    noDisplayableNotices() {
      return this.notices && this.notices.length == 0;
    },
    ...mapGetters('notices', {
      isFetching: 'isFetching',
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>
<style lang="scss" scoped>
</style>

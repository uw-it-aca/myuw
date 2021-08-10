<template>
  <uw-card v-if="!isReady || hasAnyNotices" :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Notices</h2>
    </template>
    <template v-if="!isErrored" #card-body>
      <p v-if="notices.length == 0">You do not have any notices at this time.</p>
      <ul v-else class="list-unstyled mb-0 myuw-text-md">
        <li v-for="notice in sortNotices(notices)" :key="notice.id_hash" class="mb-1">
          <div class="d-flex d-sm-inline-flex notice-container">
            <div class="flex-grow-1 pe-1">
              <span class="notice-title">
                <button
                  v-uw-collapse="notice.id_hash"
                  v-no-track-collapse
                  class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
                >
                  <span
                    v-if="notice.is_critical"
                    class="d-inline-block fw-bold text-danger me-1 notice-critical"
                    >Critical:</span
                  ><span v-html="notice.notice_title" />
                </button>
              </span>
            </div>
            <div>
              <span
                v-if="!notice.is_read"
                class="badge bg-warning fw-normal notice-status text-dark p-1"
              >
                New
              </span>
            </div>
          </div>
          <uw-collapse :id="notice.id_hash" tabindex="0" @show="onShowNotice(notice)">
            <div class="p-3 mt-2 bg-light text-dark notice-body" v-html="notice.notice_body" />
          </uw-collapse>
        </li>
        <li class="mb-1">
          <covid-vaccine />
        </li>
      </ul>
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
import Collapse from '../../_templates/collapse.vue';
import Covid19 from './covid19.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
    'covid-vaccine': Covid19,
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
    hasAnyNotices() {
      return this.allNotices.length > 0;
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
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    onShowNotice(notice) {
      this.$logger.noticeOpen(this, notice);
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', ['fetch', 'setRead']),
  },
};
</script>
<style lang="scss" scoped>
::v-deep .date {
  font-weight: bold;
}
</style>

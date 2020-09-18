<template>
  <uw-card
    v-if="unreadNotices().length > 0"
    :loaded="isReady"
    :errored="isErrored"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        Payment Received, Thank You
      </h3>
    </template>
    <template #card-body>
      <div v-for="notice in notices" :key="notice.id_hash">
        <span
          v-if="!notice.is_read"
          v-html="notice.notice_content"
        />
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
    ...mapState({
      ty_notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_thankyou'),
        );
      },
      fp_notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_feespaid'),
        );
      },
      notices() {
        return this.ty_notices.concat(this.fp_notices);
      },
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    unreadNotices() {
      return this.notices.filter(
          (notice) => notice.is_read == false,
      );
    },
    onShowNotice(notice) {
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', ['fetch', 'setRead']),
  },
};
</script>

<style lang="scss" scoped>
</style>

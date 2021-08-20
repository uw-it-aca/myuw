<template>
  <uw-card
    v-if="student && (!isReady || showThankYou(notices))"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
    class="myuw-thank-you"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Payment Received, Thank You
      </h2>
    </template>
    <template #card-body>
      <div class="myuw-thank-you-notices myuw-text-md mb-2">
        <div
          v-for="notice in notices"
          v-once
          :key="notice.id_hash"
          v-html="notice.notice_content"
        />
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {
      showCard: true,
      ranOnce: false,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
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
      notices: function() {
        return this.ty_notices.concat(this.fp_notices).filter(
            (notice) => notice.is_read == false,
        );
      },
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student) this.fetch();
  },
  methods: {
    showThankYou(notices) {
      if (this.isReady) {
        if (this.ranOnce) {
          return this.showCard;
        } else {
          this.showCard = Boolean(notices.length > 0).valueOf();
          this.ranOnce = true;
          this.setNoticesRead(notices);
        }
      }
      return true;
    },
    setNoticesRead(notices) {
      notices.forEach((notice) => this.setRead(notice));
    },
    ...mapActions('notices', ['fetch', 'setRead']),
  },
};
</script>

<style lang="scss" scoped>
@import "../../../../css/myuw/variables.scss";

.myuw-thank-you {
  // override card background color using $success background
  ::v-deep .card-body {
    background-color: lighten($success, 57%) !important;
  }
  .myuw-thank-you-notices {
    div { margin-bottom: 1rem;
      &:last-child { margin-bottom: 0;}
    }
    ::v-deep .date {
      font-weight: bold;
    }
  }
}
</style>

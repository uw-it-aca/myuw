<template>
  <uw-card
    v-if="showThankYou(notices)"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
    class="myuw-thank-you"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        Payment Received, Thank You
      </h3>
    </template>
    <template #card-body>
      <div class="myuw-thank-you-notices myuw-text-md">
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
import Card from '../../../../containers/card.vue';

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
      return (this.statusCode == 543);
    },
  },
  created() {
    this.fetch();
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

<style lang="scss">
@import "../../../../../css/myuw/variables.scss";
.myuw-thank-you {
  .card {
    background-color: lighten($green, 57%);
  }
  .myuw-thank-you-notices {
    div { margin-bottom: 1rem;
      &:last-child { margin-bottom: 0;}
    }
  }
}
</style>

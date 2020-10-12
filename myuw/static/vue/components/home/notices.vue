<template>
  <uw-card
    v-if="!isReady || hasAnyNotices"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode">
        Notices
      </h3>
    </template>
    <template
      v-if="!isErrored"
      #card-body
    >
      <p v-if="notices.length == 0">
        You do not have any notices at this time.
      </p>
      <ul
        v-else
        class="list-unstyled mb-0 myuw-text-md"
      >
        <li
          v-for="notice in notices"
          :key="notice.id_hash"
          class="mb-1"
        >
          <div class="d-flex d-sm-inline-flex notice-container">
            <div class="flex-grow-1 pr-1">
              <span class="notice-title">
                <button
                  v-b-toggle="notice.id_hash"
                  class="btn btn-link p-0 border-0 align-top
                    notice-link text-left myuw-text-md"
                >
                  <span
                    v-if="notice.is_critical"
                    class="d-inline-block font-weight-bold
                    text-danger mr-1 notice-critical"
                  >Critical:</span><span v-html="notice.notice_title" />
                </button>
              </span>
            </div>
            <div>
              <b-badge
                v-if="!notice.is_read"
                variant="warning"
                class="font-weight-normal notice-status"
              >
                New
              </b-badge>
            </div>
          </div>
          <b-collapse
            :id="notice.id_hash"
            tabindex="0"
            @show="onShowNotice(notice)"
          >
            <div
              class="p-3 mt-2 mb-2 bg-light text-dark notice-body"
              v-html="notice.notice_body"
            />
          </b-collapse>
        </li>
      </ul>
    </template>
    <template
      v-else
      #card-body
    >
      <p class="text-danger myuw-text-md">
        <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
        An error occurred and MyUW cannot load your notices right now. Please
        try again later.
      </p>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.is_critical ||
              notice.category.includes('Legal') ||
              notice.location_tags.includes('notices_date_sort') ||
              notice.location_tags.includes('notice_banner'),
        ).sort((n1, n2) => {
          if (n1.is_critical !== n2.is_critical) {
            return n2.is_critical - n1.is_critical;
          }
          return n2.date - n1.date;
        });
      },
      hasAnyNotices: (state) => {
        return state.notices.value.length > 0;
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
    onShowNotice(notice) {
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', ['fetch', 'setRead']),
  },
};
</script>

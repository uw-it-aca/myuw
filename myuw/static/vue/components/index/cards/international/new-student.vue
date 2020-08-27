<template>
  <uw-card
    v-if="!isReady || internationalStudent && notices.length > 0"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h3 class="myuw-card-header">
        International Student Resources
      </h3>
    </template>
    <template v-if="!isErrored" #card-body>
      <div
        v-for="notice in notices"
        :key="notice.id_hash"
        v-html="notice.notice_body"
      />
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
      internationalStudent: (state) => state.user.affiliations.intl_stud,
      notices: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_fiuts'),
        );
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
    ...mapActions('notices', ['fetch']),
  },
};
</script>

<template>
  <uw-card
    v-if="!isReady || internationalStudent && notices.length > 0"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        International Student Resources
      </h2>
    </template>
    <template v-if="!isErrored" #card-body>
      <div
        v-for="notice in notices"
        :key="notice.id_hash"
        class="myuw-text-md"
        v-html="notice.notice_body"
      />
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

<template>
  <uw-card :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3 class="text-dark-beige">
        Payment Received, Thank You
      </h3>
    </template>
    <template #card-body>
      <!-- notice template where data is inserted -->
      <div v-for="notice in notices" :key="notice.id_hash">
        {{ notice.notice_content }}
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
      isResident: (state) => {
        let isResident = true;
        const notices = state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_residence'),
        )[0];

        if (notices) {
          notices.attributes.forEach((attr) => {
            if (attr.name === 'ResidencyStatus' &&
                attr.value !== '1' &&
                attr.value !== '2') {
              isResident = false;
            }
          });
        }

        return isResident;
      },
      student: (state) => state.user.affiliations.student,
      notices () {
        return ty_notices.concat(fp_notices);
      }
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      hasRegisterNotices: 'hasRegisterNotices',
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

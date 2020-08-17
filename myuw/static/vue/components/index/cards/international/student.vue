<template>
  <uw-card
    v-if="user.affiliations.intl_stud"
    :loaded="true"
  >
    <template #card-heading>
      <h3>International Student</h3>
    </template>
    <template
      v-if="user.affiliations.seattle ||
        user.affiliations.bothell || user.affiliations.tacoma"
      #card-body
    >
      <uw-seattle v-if="user.affiliations.seattle" />
      <uw-bothell v-if="user.affiliations.bothell" />
      <uw-tacoma v-if="user.affiliations.tacoma" />
    </template>
    <template
      v-else
      #card-body
    >
      <b-tabs>
        <b-tab
          title="Seattle"
          active
        >
          <uw-seattle />
        </b-tab>
        <b-tab
          title="Bothell"
        >
          <uw-bothell />
        </b-tab>
        <b-tab
          title="Tacoma"
        >
          <uw-tacoma />
        </b-tab>
      </b-tabs>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../../../../containers/card.vue';
import Seattle from './seattle.vue';
import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-seattle': Seattle,
    'uw-bothell': Bothell,
    'uw-tacoma': Tacoma,
  },
  computed: mapState({
    user: (state) => state.user,
  }),
};
</script>

<style scoped>

</style>

<template>
  <uw-card
    v-if="intl_stud"
    :loaded="true"
  >
    <template #card-heading>
      <h3>International Student</h3>
    </template>
    <template
      v-if="seattle || bothell || tacoma"
      #card-body
    >
      <uw-seattle v-if="seattle" />
      <uw-bothell v-if="bothell" />
      <uw-tacoma v-if="tacoma" />
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
    seattle: (state) => state.user.affiliations.seattle,
    bothell: (state) => state.user.affiliations.bothell,
    tacoma: (state) => state.user.affiliations.tacoma,
    intl_stud: (state) => state.user.affiliations.intl_stud,
  }),
};
</script>

<style scoped>

</style>

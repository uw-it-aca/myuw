<template>
  <uw-card v-if="internationalStudent" :loaded="true">
    <template #card-heading>
      <h3 class="text-dark-beige">
        International Student
      </h3>
    </template>
    <template v-if="seattle || bothell || tacoma" #card-body>
      <uw-seattle v-if="seattle" />
      <uw-bothell v-if="bothell" />
      <uw-tacoma v-if="tacoma" />
    </template>
    <template v-else #card-body>
      <b-tabs
        pills
        nav-wrapper-class="mb-3 p-1"
        nav-class=""
        active-nav-item-class="bg-beige text-body font-weight-bold"
      >
        <b-tab
          title="Seattle"
          title-item-class="bg-light text-nowrap text-uppercase
               myuw-text-xs mr-1 mb-1"
          title-link-class="text-body h-100"
          active
        >
          <uw-seattle />
        </b-tab>
        <b-tab
          title="Bothell"
          title-item-class="bg-light text-nowrap text-uppercase
               myuw-text-xs mr-1 mb-1"
          title-link-class="text-body h-100"
        >
          <uw-bothell />
        </b-tab>
        <b-tab
          title="Tacoma"
          title-item-class="bg-light text-nowrap text-uppercase
               myuw-text-xs mr-1 mb-1"
          title-link-class="text-body h-100"
        >
          <uw-tacoma />
        </b-tab>
      </b-tabs>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../../../../layouts/card.vue';
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
    internationalStudent: (state) => state.user.affiliations.intl_stud,
    seattle: (state) => state.user.affiliations.seattle,
    bothell: (state) => state.user.affiliations.bothell,
    tacoma: (state) => state.user.affiliations.tacoma,
  }),
};
</script>

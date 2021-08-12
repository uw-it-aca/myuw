<template>
  <uw-card v-if="internationalStudent" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        International Student
      </h2>
    </template>
    <template v-if="seattle || bothell || tacoma" #card-body>
      <uw-seattle v-if="seattle" />
      <uw-bothell v-if="bothell" />
      <uw-tacoma v-if="tacoma" />
    </template>
    <template v-else #card-body>
      <uw-tabs
        pills
        nav-wrapper-class="mb-3 p-0"
        active-nav-item-class="bg-transparent rounded-0
          myuw-border-bottom border-dark text-body"
      >
        <uw-tab
          title="Seattle"
          title-item-class="text-nowrap myuw-text-md me-2 mb-1"
          title-link-class="rounded-0 px-2 py-1 h-100
               text-body myuw-border-bottom"
          active
        >
          <uw-seattle />
        </uw-tab>
        <uw-tab
          title="Tacoma"
          title-item-class="text-nowrap myuw-text-md me-2 mb-1"
          title-link-class="rounded-0 px-2 py-1 h-100
               text-body myuw-border-bottom"
        >
          <uw-tacoma />
        </uw-tab>
        <uw-tab
          title="Bothell"
          title-item-class="text-nowrap myuw-text-md me-2 mb-1"
          title-link-class="rounded-0 px-2 py-1 h-100
               text-body myuw-border-bottom"
        >
          <uw-bothell />
        </uw-tab>
      </uw-tabs>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';

import Card from '../../_templates/card.vue';
import Tabs from '../../_templates/tabs/tabs.vue';
import Tab from '../../_templates/tabs/tab.vue';
import Seattle from './seattle.vue';
import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-tabs': Tabs,
    'uw-tab': Tab,
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

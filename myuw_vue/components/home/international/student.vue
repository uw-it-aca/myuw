<template>
  <uw-card v-if="internationalStudent" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">International Student</h2>
    </template>

    <template v-if="singleCampus" #card-body>
      <uw-seattle v-if="seattle" />
      <uw-bothell v-if="bothell" />
      <uw-tacoma v-if="tacoma" />
    </template>

    <template v-else #card-body>
      <uw-tabs pills bottom-border nav-wrapper-class="mb-3 p-0">
        <template #tabs>
          <uw-tab-button
            v-if="seattle || noCampus"
            panel-id="seattle"
            title-item-class="me-2 mb-1"
            title-link-class="rounded-0 text-body"
          >
            Seattle
          </uw-tab-button>
          <uw-tab-button
            v-if="tacoma || noCampus"
            panel-id="tacoma"
            title-item-class="me-2 mb-1"
            title-link-class="rounded-0 text-body"
          >
            Tacoma
          </uw-tab-button>
          <uw-tab-button
            v-if="bothell || noCampus"
            panel-id="bothell"
            title-item-class="me-2 mb-1"
            title-link-class="rounded-0 text-body"
          >
            Bothell
          </uw-tab-button>
        </template>
        <template #panels>
          <uw-tab-panel v-if="seattle || noCampus" panel-id="seattle">
            <uw-seattle />
          </uw-tab-panel>
          <uw-tab-panel v-if="tacoma || noCampus" panel-id="tacoma">
            <uw-tacoma />
          </uw-tab-panel>
          <uw-tab-panel v-if="bothell || noCampus" panel-id="bothell">
            <uw-bothell />
          </uw-tab-panel>
        </template>
      </uw-tabs>
    </template>
  </uw-card>
</template>

<script>
import { mapState } from 'vuex';

import Card from '../../_templates/card.vue';
import Tabs from '../../_templates/tabs/tabs.vue';
import TabButton from '../../_templates/tabs/button.vue';
import TabPanel from '../../_templates/tabs/panel.vue';
import Seattle from './seattle.vue';
import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-tabs': Tabs,
    'uw-tab-button': TabButton,
    'uw-tab-panel': TabPanel,
    'uw-seattle': Seattle,
    'uw-bothell': Bothell,
    'uw-tacoma': Tacoma,
  },
  computed: {
    ...mapState({
      internationalStudent: (state) => state.user.affiliations.intl_stud,
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
    }),
    singleCampus() {
      return (
        this.seattle && !(this.bothell || this.tacoma) ||
        this.bothell && !(this.seattle || this.tacoma) ||
        this.tacoma && !(this.seattle || this.bothell));
    },
    noCampus() {
      return !(this.seattle || this.bothell || this.tacoma);
    },
  }
};
</script>

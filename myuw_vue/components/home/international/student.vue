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
          bottom-border
          nav-wrapper-class="mb-3 p-0">
        <template #tabs>
          <uw-tab-list-button panel-id="seattle"
              title-item-class="me-2 mb-1"
              title-link-class="rounded-0 text-body">
            Seattle
          </uw-tab-list-button>
          <uw-tab-list-button panel-id="tacoma"
              title-item-class="me-2 mb-1"
              title-link-class="rounded-0 text-body">
            Tacoma
          </uw-tab-list-button>
          <uw-tab-list-button panel-id="bothell"
              title-item-class="me-2 mb-1"
              title-link-class="rounded-0 text-body">
            Bothell
          </uw-tab-list-button>
        </template>
        <template #panels>
          <uw-tab-panel panel-id="seattle">
            <uw-seattle />
          </uw-tab-panel>
          <uw-tab-panel panel-id="tacoma">
            <uw-tacoma />
          </uw-tab-panel>
          <uw-tab-panel panel-id="bothell">
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
import Tabs from '../../_templates/tabs/tab-container.vue';
import TabListButton from '../../_templates/tabs/tab-list-button.vue';
import TabPanel from '../../_templates/tabs/tab-panel.vue';
import Seattle from './seattle.vue';
import Bothell from './bothell.vue';
import Tacoma from './tacoma.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-tabs': Tabs,
    'uw-tab-list-button': TabListButton,
    'uw-tab-panel': TabPanel,
    'uw-seattle': Seattle,
    'uw-bothell': Bothell,
    'uw-tacoma': Tacoma,
  },
  computed: mapState({
    internationalStudent: state => state.user.affiliations.intl_stud,
    seattle: state => state.user.affiliations.seattle,
    bothell: state => state.user.affiliations.bothell,
    tacoma: state => state.user.affiliations.tacoma,
  }),
};
</script>

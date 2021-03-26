<template>
  <uw-card
    v-if="showCard"
    :loaded="true"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        UW Retirement Association (UWRA)
      </h2>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        The UWRA informs, connects, and advocates for UW retirees and
        pre-retirees. The UWRA encourages continued engagement with
        the UW and fosters a purposeful retirement through educational
        and social programs.
      </p>
      <ul class="list-unstyled mb-0 myuw-text-md">
        <li>
          <a v-out="'UWRA'"
            href="http://www.washington.edu/uwra/"
            target="_blank">
            Learn more about UWRA
          </a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../../_templates/card.vue';
export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      showCard: (state) => state.user.affiliations.retiree,
    }),
  },
};
</script>

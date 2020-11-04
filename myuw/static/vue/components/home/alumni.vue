<template>
  <uw-card v-if="alum" :loaded="true">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Alumni and Alumni Association
      </h3>
    </template>
    <template #card-body>
      <p>
        Sharing a connection across three campuses and extending to places
        all over the world, UW alumni are united in the belief that together
        we will make a difference.
      </p>
      <ul>
        <li>
          <a href="https://www.washington.edu/alumni" target="_blank"
             data-linklabel="Alumni Info">Alumni News, Events and Services
          </a>
        </li>
        <li>
          <a href="https://magazine.washington.edu/" target="_blank"
             data-linklabel="Columns Magazine">Columns Magazine
          </a>
        </li>
      </ul>
      <h4>
        University of Washington Alumni Association (UWAA)
      </h4>
      <p>With 56,000 members, UWAA helps Huskies of all ages stay in touch
        and in the know.
      </p>
      <ul class="unstyled-list">
        <li>
          <a href="https://www.washington.edu/cms/alumni/membership/"
            target="_blank" data-linklabel="Alumni Association">
            Learn about the UWAA
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
      alum: (state) => state.user.affiliations.alumni,
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>

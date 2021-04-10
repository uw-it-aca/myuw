<template>
  <uw-card v-if="alum" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Alumni and Alumni Association
      </h2>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        Sharing a connection across three campuses and extending to places
        all over the world, UW alumni are united in the belief that together
        we will make a difference.
      </p>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'UW Alumni'"
            href="https://www.washington.edu/alumni"
          >Alumni News, Events and Services</a>
        </li>
        <li class="mb-1">
          <a href="https://magazine.washington.edu/"
          >Columns Magazine</a>
        </li>
      </ul>
      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        University of Washington Alumni Association (UWAA)
      </h3>
      <p class="myuw-text-md">
        With 56,000 members, UWAA helps Huskies of all ages stay in touch
        and in the know.
      </p>
      <ul class="list-unstyled mb-0 myuw-text-md">
        <li>
          <a v-out="'UWAA'"
            href="https://www.washington.edu/cms/alumni/membership/"
          >
            Learn about the UWAA
          </a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../_templates/card.vue';

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

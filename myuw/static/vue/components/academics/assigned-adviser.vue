<template>
  <uw-card
    v-if="showCard"
    :loaded="isReadyAdvisers && isReadyProfile"
    :errored="isErroredAdvisers || isErroredProfile"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Advisers
      </h2>
    </template>
    <template #card-body>
      <ul class="d-flex flex-wrap list-unstyled mb-0">
        <li
          v-for="(adviser, index) in advisers"
          :key="index"
          class="mb-3"
          :class="[$mq === 'mobile' ? 'w-100' : 'w-50']"
        >
          <div class="myuw-text-md">
            <div
              class="font-weight-bold myuw-font-encode-sans"
              style="color: #333;"
            >{{ adviser.program }}</div>
            <div>{{ adviser.full_name }} <span v-if="adviser.pronouns">({{ adviser.pronouns }})</span></div>
            <div>{{ adviser.email_address }}</div>
            <div>{{ formatPhoneNumberDisaply(adviser.phone_number) }}</div>
            <div v-if="adviser.booking_url">
              <a :href="adviser.booking_url">Make an appointment online</a>
            </div>
          </div>
        </li>
      </ul>
      <hr class="my-0">
      <uw-card-property title="Major" class="mt-3" :noMarginBottom="true">
          <ul class="list-unstyled">
            <template v-for="(termMajor, index) in termMajors">
              <li v-if="index == 0" :key="index" class="mb-1">
                {{ degreeListString(termMajor.majors) }}
              </li>
              <li v-else-if="termMajor.degrees_modified" :key="index" class="mb-1">
                Beginning {{ titilizeTerm(termMajor.quarter) }} {{ termMajor.year }}:
                &nbsp;&nbsp;
                <span v-if="termMajor.majors.length > 0">
                  {{ degreeListString(termMajor.majors) }}
                </span>
                <span v-else>
                  None
                </span>
              </li>
            </template>
          </ul>
      </uw-card-property>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your adviser information right now. In the meantime, to contact a general adviser, try the
      <a href="https://www.washington.edu/uaa/advising/">Undergraduate Advising</a> page and to contact a departmental or major adviser, try the 
      <a href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/">Departmental and Major Advising Offices</a> page.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';
export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
  },
  computed: {
    ...mapState({
      isUndergrad: (state) => state.user.affiliations.undergrad,
      advisers: (state) => state.advisers.value,
      profile: (state) => state.profile.value,
      termMajors: (state) => state.profile.value.term_majors,
    }),
    ...mapGetters('advisers', {
      isReadyAdvisers: 'isReady',
      isErroredAdvisers: 'isErrored',
      statusCodeAdvisers: 'statusCode',
    }),
    ...mapGetters('profile', {
      isReadyProfile: 'isReady',
      isErroredProfile: 'isErrored',
      statusCodeProfile: 'statusCode',
    }),
    showError: function() {
      return this.statusCodeProfile !== 404 || this.statusCodeAdvisers !== 404;
    },
    showCard: function() {
      return this.isUndergrad;
    }
  },
  created() {
    if (this.isUndergrad) {
      this.fetchAdvisers();
      this.fetchProfile();
    }
  },
  methods: {
    ...mapActions('advisers', {
      fetchAdvisers: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
    degreeListString(degrees) {
      let list = '';
      for (let i = 0; i < degrees.length; i++) {
        list += degrees[i].full_name;
        if (i < degrees.length - 1) {
          list += ', ';
        }
      }
      return list;
    },
  },
};
</script>



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
      <uw-card-property title="Major">
          <ul class="list-unstyled mb-0">
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
      <hr class="my-2">
      <ul class="d-flex flex-wrap list-unstyled">
        <li v-for="(adviser, index) in advisers" :key="index" class="w-50 mt-3">
          <div class="myuw-text-md">
            <div class="font-weight-bold">{{ adviser.program }}</div>
            <div>{{ adviser.full_name }} <span v-if="adviser.pronouns">({{ adviser.pronouns }})</span></div>
            <div>{{ adviser.email_address }}</div>
            <div>{{ formatPhoneNumberDisaply(adviser.phone_number) }}</div>
            <div v-if="adviser.booking_url">
              <a :href="adviser.booking_url">Make an appointment online</a>
            </div>
          </div>
        </li>
      </ul>
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



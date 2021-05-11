<template>
  <uw-card
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
      <div>
        <div v-for="(adviser, index) in advisers" :key="index">
          <ul class="list-unstyled myuw-text-md">
            <li class="font-weight-bold">{{ adviser.program }}</li>
            <li>{{ adviser.full_name }} ({{adviser.pronouns}})</li>
            <li>{{ adviser.email_address }}</li>
            <li>{{ formatPhoneNumberDisaply(adviser.phone_number) }}</li>
            <li v-if="adviser.booking_url">
              <a :href="adviser.booking_url">Make an appointment online</a>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';
//import CardPropertyGroup from '../_templates/card-property-group.vue';
export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
    //'uw-card-property-group': CardPropertyGroup,
  },
  computed: {
    ...mapState({
      isStudent: (state) => state.user.affiliations.student,
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
  },
  created() {
    if (this.isStudent) {
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



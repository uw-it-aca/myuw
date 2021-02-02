<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Applicant Profile
      </h3>
    </template>
    <template #card-body>
      <div vocab="http://schema.org/" typeof="Person">
        <b-container class="bv-example-row">
          <profile-entry title="Permanent Address">
            <template v-if="permanentAddress" #content>
              <span>
                {{ permanentAddress.street_line1 }}
                <br>
                {{ permanentAddress.street_line2 }}
                <br>
                {{ addressLocationString(permanentAddress) }}
                <br>
                {{ permanentAddress.country }}
              </span>
            </template>
            <template v-else #content>
              No address available
            </template>
          </profile-entry>
          <profile-entry title="">
            <template #content>
              <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/address.aspx"
                 title="Change address on Student Personal Services website"
              >Change Address</a>
            </template>
          </profile-entry>
          <profile-entry title="Email Address">
            <template #content>
              <span v-if="email">{{ email }}</span>
              <span v-else>No email address availabe</span>
            </template>
          </profile-entry>
        </b-container>
      </div>
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import ProfileEntry from './profile-entry.vue';

export default {
  components: {
    'uw-card': Card,
    'profile-entry': ProfileEntry,
  },
  computed: {
    ...mapState('profile', {
      profile: (state) => state.value,
      permanentAddress: (state) => state.value.permanent_address,
      email: (state) => state.value.email,
    }),
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      student: (state) => state.user.affiliations.student,
      applicant: (state) => state.user.affiliations.applicant,
    }),
    showCard: function () {
      return this.applicant && !this.student && Boolean(this.profile);
    },
    showError: function () {
      return false;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
    addressLocationString(address) {
      let location = '';
      if (address.city && address.state) {
        location += address.city + ', ' + address.state;
      }
      if (address.postal_code) {
        location += ' ' + address.postal_code;
      }
      if (address.zip_code) {
        location += ' ' + address.zip_code;
      }
      return location;
    }
  },
};
</script>

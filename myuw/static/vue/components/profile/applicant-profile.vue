<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Applicant Profile
      </h2>
    </template>
    <template #card-body>
      <div vocab="http://schema.org/" typeof="Person">
        <b-container>
          <uw-card-property title="Permanent Address">
            <div v-if="permanentAddress">
              <span>
                {{ permanentAddress.street_line1 }}
                <br>
                {{ permanentAddress.street_line2 }}
                <br>
                {{ addressLocationString(permanentAddress) }}
                <br>
                {{ permanentAddress.country }}
              </span>
            </div>
            <div v-else>
              No address available
            </div>
          </uw-card-property>
          <uw-card-property title="">
            <a v-out="'Change Student Address'"
              href="https://sdb.admin.uw.edu/sisStudents/uwnetid/address.aspx"
              title="Change address on Student Personal Services website"
            >Change Address</a>
          </uw-card-property>
          <hr>
          <uw-card-property title="Email Address">
            <span v-if="email">{{ email }}</span>
            <span v-else>No email address availabe</span>
          </uw-card-property>
        </b-container>
      </div>
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
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
    },
  },
};
</script>

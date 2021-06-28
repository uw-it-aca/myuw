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
      <uw-card-property-group>
        <uw-card-property title="Permanent Address">
          <div v-if="permanentAddress">
            <div v-if="permanentAddress.street_line1"
              v-text="permanentAddress.street_line1">
            </div>
            <div v-if="permanentAddress.street_line2"
              v-text="permanentAddress.street_line2">
            </div>
            <div v-text="addressLocationString(permanentAddress)">
            </div>
            <div v-if="permanentAddress.country"
              v-text="permanentAddress.country">
            </div>
          </div>
          <div v-else class="text-muted">
            No address available
          </div>
        </uw-card-property>
        <uw-card-property title="">
          <a v-out="'Change Student Address'"
            href="https://sdb.admin.uw.edu/sisStudents/uwnetid/address.aspx"
            title="Change address on Student Personal Services website"
          >Change Address</a>
        </uw-card-property>
      </uw-card-property-group>
      <uw-card-property-group>
        <uw-card-property title="Email Address">
          <span v-if="email">{{ email }}</span>
          <span v-else class="text-muted">No email address available</span>
        </uw-card-property>
      </uw-card-property-group>
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';
import CardPropertyGroup from '../_templates/card-property-group.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
    'uw-card-property-group': CardPropertyGroup,
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

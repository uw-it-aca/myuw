<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Employee Profile
      </h2>
    </template>
    <template #card-body>
      <div vocab="http://schema.org/" typeof="Person">
        <b-container>
          <template v-if="position">
            <uw-card-property title="Department">
              {{ position.department }}
            </uw-card-property>
            <uw-card-property title="Job Title">
              {{ position.title }}
            </uw-card-property>
          </template>
          <uw-card-property v-if="email" title="Email:">
            {{ email }}
          </uw-card-property>
          <uw-card-property title="Phone Number">
            <p v-if="noFormsOfContact" class="text-muted">
              No phone numbers listed
            </p>
            <ul v-else class="list-unstyled myuw-text-md">
              <li v-if="phone" class="mb-1">
                Office:&nbsp;&nbsp;{{ formatPhoneNumberDisaply(phone) }}
              </li>
              <li v-if="mobile" class="mb-1">
                Mobile:&nbsp;&nbsp;{{ formatPhoneNumberDisaply(mobile) }}
              </li>
              <li v-if="voiceMail" class="mb-1">
                Voicemail:&nbsp;&nbsp;{{ formatPhoneNumberDisaply(voiceMail) }}
              </li>
              <li v-if="fax" class="mb-1">
                Fax:&nbsp;&nbsp;{{ formatPhoneNumberDisaply(fax) }}
              </li>
            </ul>
          </uw-card-property>
          <uw-card-property title="Address">
            <p v-if="!mailstop && !address" class="text-muted">
              No address available
            </p>
            <div v-else>
              <p v-if="mailstop">Box {{ mailstop }}</p>
              <p v-if="address">{{ address }}</p>
            </div>
          </uw-card-property>
          <uw-card-property title="">
            <p>
              <uw-link-button
                class="myuw-workday"
                href="https://wd5.myworkday.com/uw/login.htmld"
                :style="`background-image: url(${staticUrl}images/wday_logo.png);`"
                >Manage profile in Workday
              </uw-link-button>
            </p>
          </uw-card-property>
          <hr>
          <uw-card-property title="UW Directory">
            <p>
              <template v-if="publishEmpDir">
                Name, position, work contact information are published.
              </template>
              <template v-else>
                Not published.
              </template>
              <br/>
              <a href="https://identity.uw.edu/">Change directory settings</a>
            </p>
            <p>
              Search for faculty, staff, and students in the
              <a v-if="isTacoma"
                  href="http://directory.tacoma.uw.edu/"
              >UW Tacoma Directory</a>
              <a v-else
                  href="https://www.washington.edu/home/peopledir/"
              >UW Directory</a>.
            </p>
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
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
    'uw-link-button': LinkButton,
  },
  computed: {
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      studentEmployee: (state) => state.user.affiliations.stud_employee,
      isTacoma: (state) => state.user.affiliations.tacoma,
      staticUrl: (state) => state.staticUrl,
    }),
    ...mapState('directory', {
      directory: (state) => state.value,
      position: (state) => state.value.positions.find(position => position.is_primary),
      email: (state) => state.value.email_addresses[0],
      phone: (state) => state.value.phones[0],
      mobile: (state) => state.value.mobiles[0],
      voiceMail: (state) => state.value.voice_mails[0],
      fax: (state) => state.value.faxes[0],
      mailstop: (state) => state.value.mailstop,
      address: (state) => state.value.addresses[0],
      publishEmpDir: (state) => state.value.publish_in_emp_directory,
    }),
    ...mapGetters('directory', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showCard: function () {
      return (this.employee || this.studentEmployee) && Boolean(this.directory);
    },
    showError: function () {
      return false;
    },
    noFormsOfContact() {
      return !this.phone && !this.mobile && !this.voiceMail && !this.fax;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('directory', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
// myuw workday button
.myuw-workday {
  background-repeat: no-repeat;
  background-position: 4% 50%;
  background-size: 18px;
  padding-left: 32px;
}
</style>
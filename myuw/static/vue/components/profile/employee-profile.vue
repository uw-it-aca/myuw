<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Employee Profile
      </h3>
    </template>
    <template #card-body>
      <div vocab="http://schema.org/" typeof="Person">
        <b-container class="bv-example-row">
          <template v-if="position">
            <profile-entry title="Department"
                          :content="position.department"
            />
            <profile-entry title="Job Title"
                          :content="position.title"
            />
          </template>
          <profile-entry v-if="email"
                         title="Email:"
                         :content="email"
          />
          <profile-entry title="Phone Number">
            <template #content>
              <p v-if="noFormsOfContact">No phone numbers listed</p>
              <span v-if="phone">Office:</span>&nbsp;&nbsp;<span>{{ formatPhoneNumberDisaply(phone) }}</span><br />
              <span v-if="mobile">Mobile:</span>&nbsp;&nbsp;<span>{{ formatPhoneNumberDisaply(mobile) }}</span><br />
              <span v-if="voiceMail">Voicemail:</span>&nbsp;&nbsp;<span>{{ formatPhoneNumberDisaply(voiceMail) }}</span><br />
              <span v-if="fax">Fax:</span>&nbsp;&nbsp;<span>{{ formatPhoneNumberDisaply(fax) }}</span><br />
            </template>
          </profile-entry>
          <profile-entry title="Address">
            <template #content>
              <p v-if="!mailstop && !address">No address available</p>
              <div v-else>
                <span v-if="mailstop">Box {{ mailstop }}</span>
                <span v-if="address">{{ address }}</span>
              </div>
            </template>
          </profile-entry>
          <profile-entry title="">
            <template #content>
              <p>
                <uw-link-button
                  class="myuw-workday"
                  href="https://wd5.myworkday.com/uw/login.htmld"
                  target="_blank"
                  data-linklabel="Workday"
                  :style="`background-image: url(${staticUrl}images/wday_logo.png);`"
                  >Manage profile in Workday
                </uw-link-button>
              </p>
            </template>
          </profile-entry>
          <profile-entry title="UW Directory">
            <template #content>
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
                >UW Directory</a>
              .</p>
            </template>
          </profile-entry>
        </b-container>
      </div>
    </template>
  </uw-card>
</template>

<script>
// ARRAYS ARE EMPTY NOT NULL
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import ProfileEntry from './profile-entry.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'profile-entry': ProfileEntry,
    'uw-link-button': LinkButton,
  },
  computed: {
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
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      studentEmployee: (state) => state.user.affiliations.stud_employee,
      isTacoma: (state) => state.user.affiliations.tacoma,
      staticUrl: (state) => state.staticUrl,
    }),
    showCard: function () {
      return (this.employee || this.studentEmployee) && Boolean(this.directory);
    },
    showError: function () {
      return false;
    },
    noFormsOfContact() {
      return !this.phone && !this.mobile && !this.voiceMail && !this.fax;
    }
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
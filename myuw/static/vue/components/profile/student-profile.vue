<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Student Profile</h3>
    </template>
    <template #card-body>
      <div vocab="http://schema.org/" typeof="Person">
        <b-container class="bv-example-row">
          <profile-entry :v-if="studentNumber"
                         title="Student Number"
                         :content="studentNumber"
          />
          <profile-entry :v-if="classStanding"
                         title="Class Standing"
                         :content="classStanding"
          />
          <profile-entry title="Major">
            <template #content>
              <ul>
                <template v-for="(termMajor, index) in termMajors">
                  <li v-if="index == 0" :key="index">
                    {{ degreeListString(termMajor.majors) }}
                  </li>
                  <li v-else-if="termMajor.degrees_modified" :key="index">
                    Beginning {{ termMajor.quarter }} {{ termMajor.year }}:
                    &nbsp;&nbsp;
                    {{ degreeListString(termMajor.majors) }}
                  </li>
                </template>
              </ul>
            </template>
          </profile-entry>
          <profile-entry :v-if="hasMinors" title="Minor">
            <template #content>
              <ul>
                <template v-for="(termMinor, index) in termMinors">
                  <li v-if="index == 0" :key="index">
                    {{ degreeListString(termMinor.minors) }}
                  </li>
                  <li v-else-if="termMinor.degrees_modified" :key="index">
                    Beginning {{ termMinor.quarter }} {{ termMinor.year }}:
                    &nbsp;&nbsp;
                    {{ degreeListString(termMinor.minors) }}
                  </li>
                </template>
              </ul>
            </template>
          </profile-entry>
          <profile-entry title="Local Address">
            <template v-if="localAddress" #content>
              <div v-if="localAddress.street_line1"
                   v-text="localAddress.street_line1">
              </div>
              <div v-if="localAddress.street_line2"
                   v-text="localAddress.street_line2">
              </div>
              <span v-text="addressLocationString(localAddress)" />
              <div v-if="localAddress.country"
                   v-text="localAddress.country">
              </div>
              <div v-if="localPhone">
                Phone: {{ formatPhoneNumberDisaply(localPhone) }}
              </div>
            </template>
            <template v-else #content>
              <span class="my-text-muted">No address available</span>
            </template>
          </profile-entry>
          <profile-entry title="Permanent Address">
            <template v-if="permanentAddress" #content>
              <div v-if="permanentAddress.street_line1"
                   v-text="permanentAddress.street_line1">
              </div>
              <div v-if="permanentAddress.street_line2"
                   v-text="permanentAddress.street_line2">
              </div>
              <span v-text="addressLocationString(permanentAddress)" />
              <div v-if="permanentAddress.country"
                   v-text="permanentAddress.country">
              </div>
              <div v-if="permanentPhone">
                Phone: {{ formatPhoneNumberDisaply(permanentPhone) }}
              </div>
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
          <profile-entry title="Student Directory Information">
            <template #content>
              <p>
                Releasable: <span v-text="directoryRelease ? 'YES' : 'NO'"/>
                <br><a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/address.aspx"
                  title="Change address release settings on Student Personal Services website"
                >Change your release settings</a>
              </p>
              <p>
                Name, phone number, email, major, and class standing are
                <em v-text="directoryRelease ? 'visible' : 'not visible'"/>
                in the UW Directory.
              </p>
              <p>
                Information such as date of birth, street address, and dates
                of attendance are
                <em v-text="directoryRelease ?
                            'releasable' : 'cannot be released'"
                />
                by the Office of the University Registrar when requested.
                <a href="http://www.washington.edu/students/reg/ferpa.html">
                  Learn more about your privacy (FERPA)
                </a>
              </p>
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
      studentNumber: (state) => state.value.student_number,
      classStanding: (state) => state.value.class_level,
      termMajors: (state) => state.value.term_majors,
      termMinors: (state) => state.value.term_minors,
      hasMinors: (state) => state.value.has_minors,
      localAddress: (state) => state.value.local_address,
      localPhone: (state) => state.value.local_phone,
      permanentAddress: (state) => state.value.permanent_address,
      permanentPhone: (state) => state.value.permanent_phone,
      directoryRelease: (state) => state.value.directory_release,
    }),
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      student: (state) => state.user.affiliations.student,
      studentEmployee: (state) => state.user.affiliations.stud_employee,
    }),
    showCard: function () {
      return this.student || this.studentEmployee;
    },
    showError: function () {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
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
    addressLocationString(address) {
      let location = '';
      if (address.city) {
        location += address.city + ', ';
      }
      if (address.state) {
        location += address.state + ' ';
      }
      if (address.postal_code) {
        location += address.postal_code + ' ';
      }
      if (address.zip_code) {
        location += address.zip_code;
      }
      return location;
    }
  },
};
</script>

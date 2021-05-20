<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Student Profile
      </h2>
    </template>
    <template #card-body>
      <uw-card-property-group>
        <uw-card-property :v-if="studentNumber" title="Student Number">
          {{ studentNumber }}
        </uw-card-property>
        <uw-card-property :v-if="classStanding" title="Class Standing">
          {{ classStanding }}
        </uw-card-property>
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
        <uw-card-property v-if="hasMinors" title="Minor">
          <ul class="list-unstyled mb-0">
            <template v-for="(termMinor, index) in termMinors">
              <li v-if="index == 0 && termMinor.minors.length" :key="index" class="mb-1">
                {{ degreeListString(termMinor.minors) }}
              </li>
              <li v-else-if="termMinor.degrees_modified" :key="index" class="mb-1">
                Beginning {{ titilizeTerm(termMinor.quarter) }} {{ termMinor.year }}:
                &nbsp;&nbsp;
                <span v-if="termMinor.minors.length > 0">
                  {{ degreeListString(termMinor.minors) }}
                </span>
                <span v-else>
                  None
                </span>
              </li>
            </template>
          </ul>
        </uw-card-property>
      </uw-card-property-group>
      <uw-card-property-group>
        <uw-card-property title="Local Address">
          <div v-if="localAddress">
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
          </div>
          <div v-else>
            <span class="my-text-muted">No address available</span>
          </div>
        </uw-card-property>
        <uw-card-property title="Permanent Address">
          <div v-if="permanentAddress">
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
      </uw-card-property-group>
      <uw-card-property-group>
        <uw-card-property title="Student Directory Information">
          <p>
            Releasable: <span v-text="directoryRelease ? 'YES' : 'NO'"/>
            <br><a v-out="'Change Student Address Release settings'"
              href="https://sdb.admin.uw.edu/sisStudents/uwnetid/address.aspx"
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
      return (this.student || this.studentEmployee) && Boolean(this.profile);
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

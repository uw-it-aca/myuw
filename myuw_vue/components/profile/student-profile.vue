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
        <uw-card-property :v-if="existClassLevel" title="Class Standing">
          {{ classStanding }}
        </uw-card-property>
        <uw-card-property title="Major">
          <major-list :term-majors="termMajors"></major-list>
        </uw-card-property>
        <uw-card-property v-if="hasMinors" title="Minor">
          <ul class="list-unstyled mb-0">
            <template v-for="(termMinor, index) in termMinors">
              <li v-if="index == 0 && termMinor.minors.length" :key="index" class="mb-1">
                {{ degreeListString(termMinor.minors) }}
              </li>
              <li v-else-if="termMinor.degrees_modified" :key="index" class="mb-1">
                Beginning {{ titleCaseWord(termMinor.quarter) }} {{ termMinor.year }}:
                &nbsp;&nbsp;
                <span v-if="termMinor.minors.length > 0">
                  {{ degreeListString(termMinor.minors) }}
                </span>
                <span v-else class="text-muted">
                  None
                </span>
              </li>
            </template>
          </ul>
        </uw-card-property>

        <uw-card-property v-if="showResidency" title="Residency">
          <span v-if="existResidency">
            {{ currentResidencyD }}
          </span>
          <span v-if="hasResidencyChange">
            <span v-if="existResidency">
              <br>
            </span>
            Beginning
            {{ titleCaseWord(pendingResidency.term.quarter) }}
            {{ pendingResidency.term.year }}:
            {{ pendingResidencyD }}
          </span>
          <br>
          <a v-out="'About residency statuses'"
            href="https://registrar.washington.edu/residency/"
            title="About residency statuses"
          >About residency statuses</a>
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
          <div v-else class="text-muted">
            No address available
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
        <uw-card-property title="Primary Emergency Contact">
          <div v-if="!primaryEmergencyContact" class="text-muted">
            No contact information added
          </div>
          <div v-else>
            <div v-if="primaryEmergencyContact.name">
              {{ titleCaseName(primaryEmergencyContact.name) }}
            </div>
            <div v-if="primaryEmergencyContact.phone_number"
              v-text="primaryEmergencyContact.phone_number">
            </div>
            <div v-else class="text-muted">
              No phone number added
            </div>
            <div v-if="primaryEmergencyContact.email"
              v-text="primaryEmergencyContact.email">
            </div>
            <div v-if="primaryEmergencyContact.relationship"
              v-text="primaryEmergencyContact.relationship">
            </div>
            <div v-else class="text-muted">
              No relationship added
            </div>
          </div>
        </uw-card-property>
        <uw-card-property title="Secondary Emergency Contact">
          <div v-if="!secondaryEmergencyContact" class="text-muted">
            No contact information added
          </div>
          <div v-else>
            <div v-if="secondaryEmergencyContact.name">
              {{ titleCaseName(secondaryEmergencyContact.name) }}
            </div>
            <div v-if="secondaryEmergencyContact.phone_number"
              v-text="secondaryEmergencyContact.phone_number">
            </div>
            <div v-else class="text-muted">
              No phone number added
            </div>
            <div v-if="secondaryEmergencyContact.email"
              v-text="secondaryEmergencyContact.email">
            </div>
            <div v-if="secondaryEmergencyContact.relationship"
              v-text="secondaryEmergencyContact.relationship">
            </div>
            <div v-else class="text-muted">
              No relationship added
            </div>
          </div>
        </uw-card-property>
        <uw-card-property title="">
          Please ensure that you at least have an up-to-date primary emergency contact.<br />
          <a v-out="'Edit Emergency contacts'"
            :href="emergencyContactsUrl"
            title="Go to Emergency Contacts website"
          >
            <span v-if="!primaryEmergencyContact && !secondaryEmergencyContact">Add</span>
            <span v-else>Edit</span> emergency contacts
          </a>
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
            of attendance
            <em v-text="directoryRelease ? 'are releasable' : 'cannot be released'"/>
            by the Office of the University Registrar when requested.
            <a href="https://www.washington.edu/students/reg/ferpa.html"
            >Learn more about your privacy (FERPA)</a>
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
import CurMajors from '../_common/major/cur-fut-majors.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
    'uw-card-property-group': CardPropertyGroup,
    'major-list': CurMajors,
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
      residentCode: (state) => state.value.resident_code,
      residentDesc: (state) => state.value.resident_desc,
      pendingResidency: (state) => state.value.pending_residency_change,
      emergencyContacts: (state) => state.value.emergency_contacts,
    }),
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    ...mapState({
      student: (state) => state.user.affiliations.student,
      studentEmployee: (state) => state.user.affiliations.stud_employee,
    }),
    showCard() {
      return (this.student || this.studentEmployee) && Boolean(this.profile);
    },
    showError() {
      return false;
    },
    // MUWM-5352
    existClassLevel () {
      return this.classStanding !== undefined && this.classStanding.length > 0;
    },
    existResidency () {
      return this.residentCode && this.residentCode !== "0"
    },
    currentResidencyD() {
      return this.titleCaseWord(
        this.formatResidency(this.residentCode, this.residentDesc));
    },
    hasPendingResidency () {
      return (
        this.pendingResidency && this.pendingResidency.pending_resident_code !== "0");
    },
    pendingResidencyD() {
      return this.hasPendingResidency ?
        this.titleCaseWord(this.formatResidency(
          this.pendingResidency.pending_resident_code,
          this.pendingResidency.pending_resident_desc)) :
        "-";
    },
    hasResidencyChange() {
      return this.hasPendingResidency && this.currentResidencyD != this.pendingResidencyD;
    },
    showResidency() {
      return this.existClassLevel  && (this.existResidency || this.hasResidencyChange);
    },
    // MUWM-5452
    primaryEmergencyContact() {
      return (
        this.emergencyContacts && this.emergencyContacts.length > 0 ?
        this.emergencyContacts[0] : null
      );
    },
    secondaryEmergencyContact() {
      return (
        this.emergencyContacts && this.emergencyContacts.length > 1 ?
        this.emergencyContacts[1] : null
      );
    },
    emergencyContactsUrl() {
      const hostname = window.location.hostname;
      return (hostname.includes("test") || hostname.includes("local")
       ? "https://test-personal.my.uw.edu/emergency"
       : "https://student-personal.my.uw.edu/emergency"
       );
    },
  },
  created() {
    if (this.student || this.studentEmployee) this.fetch();
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
    formatResidency(rcode, rdesc) {
      if(rcode === "5") return rdesc;
      if(rcode === "6") return "NONRESIDENT";
      return rdesc.replace(/\s.*/, '');
    }
  },
};
</script>

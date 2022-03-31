<template>
  <uw-card
    v-if="student && (!isReady || hasRegisterNotices)"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        To Register For Classes
      </h2>
    </template>
    <template #card-body>
      <div v-if="no_orient.length > 0">
        <div
          v-for="notice in no_orient"
          :key="notice.id_hash"
          class="d-flex mb-2"
        >
          <font-awesome-icon
            :icon="faCircle"
            class="me-3 mt-1 text-muted myuw-text-lg"
          />
          <div>
            <div class="mb-1 myuw-font-encode-sans" v-html="notice.notice_title" />
            <div class="myuw-text-md" v-html="notice.notice_body" />
          </div>
        </div>
      </div>

      <div
        v-for="notice in orient_after"
        :key="notice.id_hash"
        class="d-flex mb-2"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="me-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-1 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div
        v-for="notice in iss_before"
        :key="notice.id_hash"
        class="d-flex mb-2"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="me-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-1 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div
        v-for="notice in iss_after"
        :key="notice.id_hash"
        class="d-flex mb-2"
      >
        <font-awesome-icon
          :icon="faCheckCircle"
          class="me-3 mt-1 text-success myuw-text-lg"
        />
        <div class="myuw-text-md" v-html="notice.notice_content" />
      </div>

      <div
        v-for="notice in orient_before"
        :key="notice.id_hash"
        class="d-flex mb-2"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="me-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-1 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div class="d-flex mb-2">
        <font-awesome-icon
          :icon="faInfoCircle"
          class="me-3 mt-1 text-mid-beige myuw-text-lg"
        />
        <div class="mb-1"><span class="myuw-font-encode-sans">Required Immunizations</span>
          <ul class="list-unstyled myuw-text-md">
            <li>
              <button
                v-uw-collapse.covidvaccination
                type="button"
                class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
              >Proof of COVID Vaccination is required to register for classes</button>
              <uw-collapse id="covidvaccination">
                <div class="p-3 mt-2 bg-light text-dark notice-body">
                  <p>The University of Washington requires all students to be vaccinated against
                    COVID-19, with certain medical or religious exemptions allowed. 
                    <a v-if="seattle" href="https://www.washington.edu/newhuskies/must-do/send-proof-of-immunity/">
                    If you have not already, you must submit documents showing your proof of
                    vaccination or complete the medical or religious exemption request process</a>.
                    <a v-if="tacoma" href="https://www.tacoma.uw.edu/registrar/newly-admitted-students#permalink-16114">
                    If you have not already, you must submit documents showing your proof of
                    vaccination or complete the medical or religious exemption request process</a>.
                    <a v-if="bothell" href="https://wellbeing.uw.edu/medical/immunizations/immunization-requirement/">
                    If you have not already, you must submit documents showing your proof of
                    vaccination or complete the medical or religious exemption request process</a>.
                    You will not be allowed to register for classes until you have completed this
                    process.
                  </p>
                </div>
              </uw-collapse>
            </li>
            <li>
              <button
                v-uw-collapse.measlesimmunization
                type="button"
                class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md"
              >Measles, mumps immunization is required by the first day of classes</button>
              <uw-collapse id="measlesimmunization">
                <div class="p-3 mt-2 bg-light text-dark notice-body">
                  <p>All students under 22 must submit evidence of measles, mumps immunity and a
                    conjugate meningitis ACWY vaccination given at age 16 or older. Students age
                    22 and older must submit evidence of measles and mumps immunity, either through
                    vaccinations (two MMR vaccinations) or lab evidence of positive titer.
                    <a v-if="seattle" href="https://www.washington.edu/newhuskies/must-do/send-proof-of-immunity/">
                    Get detailed instructions here.</a>
                    <a v-if="tacoma" href="https://www.tacoma.uw.edu/registrar/newly-admitted-students#permalink-16114">
                    Get detailed instructions here.</a>
                    <a v-if="bothell" href="https://wellbeing.uw.edu/medical/immunizations/immunization-requirement/">
                    Get detailed instructions here.</a>
                  </p>
                </div>
              </uw-collapse>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {
  faCheckCircle, faInfoCircle,
} from '@fortawesome/free-solid-svg-icons';
import {
  faCircle,
} from '@fortawesome/free-regular-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
  },
  data() {
    return {
      faCheckCircle,
      faCircle,
      faInfoCircle,
      isOpen: false,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      seattle: (state) => state.user.affiliations.seattle,
      bothell: (state) => state.user.affiliations.bothell,
      tacoma: (state) => state.user.affiliations.tacoma,
      no_orient: (state) => {
        // newstudentclist_advorientregdateb
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_no_orient'),
        );
      },
      orient_after: (state) => {
        // newstudentclist_advorientregdatec
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_orient_after'),
        );
      },
      orient_before: (state) => {
        // newstudentclist_advorientregdatea
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_orient_before'),
        );
      },
      iss_before: (state) => {
        // newstudentclist_intlstucheckina
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_iss_before'),
        );
      },
      iss_after: (state) => {
        // newstudentclist_intlstucheckinb
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_iss_after'),
        );
      },
      measles_before: (state) => {
        // newstudentclist_measlesa
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_measles_before'),
        );
      },
      measles_after: (state) => {
        // newstudentclist_measlesb
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_measles_after'),
        );
      },
    }),
    ...mapGetters('notices', [
      'isReady',
      'isErrored',
      'statusCode',
      'hasRegisterNotices',
    ]),
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student) this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>
<style lang="scss" scoped>
::v-deep .date {
  font-weight: bold;
}
</style>

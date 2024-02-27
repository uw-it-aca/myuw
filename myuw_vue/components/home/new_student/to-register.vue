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
          <span class="text-muted fw-light fst-italic myuw-text-sm px-2">(Item does not reflect completion status)</span>
          <button
            v-uw-collapse.measlesimmunization
            type="button"
            class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md d-block"
          >Immunization records are required by the 3rd week of your first quarter</button>
          <uw-collapse id="measlesimmunization">
            <div class="p-3 mt-2 bg-light text-dark notice-body">
              <p>All students must submit evidence of Measles and Mumps immunity, either
                through vaccinations or lab evidence of positive titer. Students ages 16
                through 21 also are required to show proof of a Meningitis ACWY vaccination
                taken at 16 years old or older.
                <a href="https://wellbeing.uw.edu/medical/immunizations/immunization-requirement/">
                Learn more about immunization requirements and deadlines.</a>
              </p>
            </div>
          </uw-collapse>
        </div>
      </div>

      <div class="d-flex mb-2">
        <font-awesome-icon
          :icon="faInfoCircle"
          class="me-3 mt-1 text-mid-beige myuw-text-lg"
        />
        <div class="mb-1"><span class="myuw-font-encode-sans">Required Husky Prevention & Response
          student course</span>
          <span class="text-muted fw-light fst-italic myuw-text-sm px-2">(Item does not reflect completion status)</span>
          <button
            v-uw-collapse.titleix
            type="button"
            class="btn btn-link p-0 border-0 align-top notice-link text-start myuw-text-md d-block"
          >Learn about and complete the one-time online course</button>
          <uw-collapse id="titleix">
            <div class="p-3 mt-2 bg-light text-dark notice-body">
              <p><a href="https://www.washington.edu/titleix/title-ix-student-course/">Husky
                Prevention & Response</a> is a one-time online course on preventing and
                responding to sex-based and gender-based violence and harassment. Complete the
                  course — which takes 60–90 minutes — before the start of your first quarter.
                  If you do not complete the course, you may be unable to register for future
                  quarters. <a href="https://tixstudent.uw.edu">Access and complete the
                  course – tixstudent.uw.edu.</a>
              </p>
            </div>
          </uw-collapse>
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
      measles_before: (state) => {
        // newstudentclist_measlesa, no longer used
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_measles_before'),
        );
      },
      measles_after: (state) => {
        // newstudentclist_measlesb, no longer used
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

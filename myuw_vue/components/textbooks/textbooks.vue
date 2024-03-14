<template>
  <uw-panel :loaded="isReady" :errored="isErrored">
    <template #panel-body>
      <div v-if="showIacErrMsg"
        class="alert alert-warning myuw-text-md mb-5" role="alert"
      >
        <strong>UW Day One Access (digital material) information temporarily
          not available </strong><br>
         If any of your courses have been using UW Day One Access, please
        check back later – due to a data error, this information is
        currently not displayed.
      </div>
      <div v-if="displayDayOneAccessProgramPanel"
        class="alert alert-warning myuw-text-md mb-5" role="alert"
      >
        <div>
          <h2 class="myuw-text-lg">UW Day One Access Program</h2>
          <p>
            At least one of your enrolled courses provides you access to required digital
            materials in Canvas, on or before the first day of class.<br />
            <strong>
              To maintain access to required digital materials, you must
              <a v-out="'Make bookstore payment'" :href="iacData.bookstore_checkout_url"
              >pay for these materials</a>
              by
              <span class="d-inline-block">
                <uw-formatted-date :due-date="iacData.payment_due_day" />
              </span>.
            </strong>
            <a href="https://www.ubookstore.com/day-one-access-faq"
            >About the Day One Access Program.</a>
          </p>
          <ul>
            <li>
              <strong>Opting out:</strong>
              You can choose to opt-out of any item until the deadline.
              Opt out on your course Canvas <em>Digital Materials</em> page.
            </li>
            <li>
              <strong>Payment status:</strong>
              This page indicates your payment and opt in/out status for each digital material.
              Note: opt in/out changes may take 24 hours to be reflected here.
            </li>
            <li>
              <strong>Purchasing after the payment deadline:</strong>
              If you have opted-out but want to purchase the course materials, please contact
              <a href="mailto:dayoneaccess@ubookstore.com">dayoneaccess@ubookstore.com</a>.
            </li>
          </ul>
        </div>
      </div>
      <div v-if="bookData.teachingSections.length > 0">
        <h2 class="h5">Teaching</h2>
        <hr class="bg-secondary" />
        <uw-section
          v-for="(section, i) in bookData.teachingSections"
          :key="i"
          :section="section"
          :collapsable="bookData.collapseSections"
          instructor
        />
        <hr v-if="bookData.collapseSections" class="bg-secondary" />
        <div v-if="bookData.enrolledSections.length > 0">
          <h2 class="h5">Enrolled</h2>
          <hr class="bg-secondary" />
        </div>
      </div>

      <uw-section
        v-for="(section, i) in bookData.enrolledSections"
        :key="i"
        :section="section"
        :collapsable="bookData.collapseSections"
      />

      <div v-if="useBookstore" class="my-4 text-center">
        <uw-link-button :href="orderUrl">
          Start textbook shopping
        </uw-link-button>
      </div>

      <div>
        <p class="text-muted myuw-text-md">
          Information on course textbooks is collected by and provided courtesy of
          <a href="http://www.bookstore.washington.edu">University Book Store</a>
          and is subject to change regularly and without notice.
        </p>
      </div>
    </template>
    <template #panel-error>
      <div class="alert alert-light p-0 border-0 bg-transparent" role="alert">
        <div class="d-flex text-danger m-0 myuw-text-md">
          <div class="pe-2 flex-shrink-1">
            <font-awesome-icon :icon="faExclamationTriangle" />
          </div>
          <div class="w-100">
            An error has occurred and we can't load this content right now.
            Please try again later.
          </div>
        </div>
      </div>
    </template>
  </uw-panel>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Panel from '../_templates/panel.vue';
import LinkButton from '../_templates/link-button.vue';
import Section from './section.vue';
import FormattedDate from '../_common/formatted-date.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-section': Section,
    'uw-link-button': LinkButton,
    'uw-formatted-date': FormattedDate,
  },
  props: {
    term: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  computed: {
    ...mapState({
      seaStud: (state) => state.user.affiliations.seattle,
      botStud: (state) => state.user.affiliations.bothell,
    }),
    ...mapState('stud_schedule', {
      studSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapState('iac', {
      iacData(state) {
        return state.value;
      },
    }),
    ...mapGetters('stud_schedule', {
      isStudScheduleReady: 'isReadyTagged',
      isStudScheduleErrored: 'isErroredTagged',
      statusCodeStudSchedule: 'statusCodeTagged',
    }),
    ...mapGetters('inst_schedule', {
      isInstScheduleReady: 'isReadyTagged',
      isInstScheduleErrored: 'isErroredTagged',
      statusCodeInstSchedule: 'statusCodeTagged',
    }),
    ...mapGetters('textbooks', {
      isTextbookReady: 'isReadyTagged',
      isTextbookErrored: 'isErroredTagged',
      statusCodeTextbooks: 'statusCodeTagged',
      getProcessedData: 'getProcessedData',
    }),
    ...mapGetters('iac', {
      isIacReady: 'isReadyTagged',
      isIacErrored: 'isErroredTagged',
      statusCodeIac: 'statusCodeTagged',
    }),
    isReady() {
      return (
        this.isTextbookReady(this.term) &&
        (this.isStudScheduleReady(this.term) ||
         this.isStudScheduleErrored(this.term)) &&
        (this.isInstScheduleReady(this.term) ||
         this.isInstScheduleErrored(this.term))
      );
    },
    isErrored() {
      return this.isTextbookErrored(this.term);
    },
    bookData() {
      if (this.isReady) {
        return this.getProcessedData(this.studSchedule, this.instSchedule);
      }
      return {};
    },
    orderUrl() {
      if (this.bookData.orderUrl) {
        return this.bookData.orderUrl;
      }
      return 'http://www.ubookstore.com/adoption-search';
    },
    useBookstore() {
      // MUWM-5311
      let ret = false;
      this.bookData.sections.forEach((section) => {
        if (section.hasBooks) {
          ret = true;
          return;
        }
      });
      return ret;
    },
    showIacErrMsg() {
      return (this.seaStud || this.botStud) && this.isIacErrored;
    },
    displayDayOneAccessProgramPanel() {
      // MUWM-5272
      return (this.seaStud || this.botStud) && this.iacData && this.iacData.ia_courses;
    },
  },
  created() {
    this.fetchStudSchedule(this.term);
    this.fetchInstSchedule(this.term);
    this.fetchTextbooks(this.term);
    if (this.seaStud || this.botStud) this.fetchIac(this.term);
  },
  methods: {
    ...mapActions('stud_schedule', {
      fetchStudSchedule: 'fetch',
    }),
    ...mapActions('inst_schedule', {
      fetchInstSchedule: 'fetch',
    }),
    ...mapActions('textbooks', {
      fetchTextbooks: 'fetch',
    }),
    ...mapActions('iac', {
      fetchIac: 'fetch',
    }),
  },
};
</script>

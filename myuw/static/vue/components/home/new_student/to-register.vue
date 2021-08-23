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
            class="mr-3 mt-1 text-muted myuw-text-lg"
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
        v-for="notice in measles_before"
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
        v-for="notice in measles_after"
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
    </template>
  </uw-card>
</template>

<script>
import {
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';
import {
  faCircle,
} from '@fortawesome/free-regular-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data() {
    return {
      faCheckCircle,
      faCircle,
    };
  },
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
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

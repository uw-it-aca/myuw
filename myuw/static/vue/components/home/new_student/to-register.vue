<template>
  <uw-card
    v-if="!isReady || hasRegisterNotices"
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
      <div v-if="formatted_date">
        <p class="myuw-text-md">
          Register on <strong>{{ formatted_date }}</strong> through
          <a
            href="https://myplan.uw.edu/"
          >MyPlan</a> or
          <a
            href="https://sdb.admin.uw.edu/students/uwnetid/register.asp"
          >the registration screen</a>.
        </p>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a
              href="https://depts.washington.edu/sislearn/registration-resources/"
            >How to register</a>
          </li>
          <li class="mb-1">
            <a
              href="http://www.washington.edu/uaa/advising/academic-planning/choosing-courses/overview/"
            >How to choose courses</a>
          </li>
        </ul>
      </div>

      <div
        v-for="notice in orient_after"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="mr-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-3 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div
        v-for="notice in iss_before"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="mr-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-3 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div
        v-for="notice in iss_after"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCheckCircle"
          class="mr-3 mt-1 text-success myuw-text-lg"
        />
        <div class="myuw-text-md" v-html="notice.notice_content" />
      </div>

      <div
        v-for="notice in measles_before"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="mr-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-3 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div
        v-for="notice in measles_after"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCheckCircle"
          class="mr-3 mt-1 text-success myuw-text-lg"
        />
        <div class="myuw-text-md" v-html="notice.notice_content" />
      </div>

      <div
        v-for="notice in orient_before"
        :key="notice.id_hash"
        class="d-flex mb-3"
      >
        <font-awesome-icon
          :icon="faCircle"
          class="mr-3 mt-1 text-muted myuw-text-lg"
        />
        <div>
          <div class="mb-3 myuw-font-encode-sans" v-html="notice.notice_title" />
          <div class="myuw-text-md" v-html="notice.notice_body" />
        </div>
      </div>

      <div v-if="orient_after.length > 0" class="d-flex mb-2">
        <font-awesome-icon
          :icon="faCheckCircle"
          class="mr-3 mt-1 text-success myuw-text-lg"
        />
        <div class="myuw-text-md">
          You have registered for an Advising &amp; Orientation Session.
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
    formatted_date: function() {
      let date = false;
      if (this.isReady) {
        if (this.no_orient.length > 0) {
          date = this.no_orient[0].formattedDate;
        }
      }
      return date;
    },
    ...mapState({
      no_orient: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_no_orient'),
        );
      },
      orient_after: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_orient_after'),
        );
      },
      iss_before: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_iss_before'),
        );
      },
      iss_after: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_iss_after'),
        );
      },
      measles_before: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_measles_before'),
        );
      },
      measles_after: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_measles_after'),
        );
      },
      orient_before: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_orient_before'),
        );
      },
    }),
    ...mapGetters('notices', [
      'isReady',
      'isErrored',
      'statusCode',
      'hasRegisterNotices',
    ]),
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
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

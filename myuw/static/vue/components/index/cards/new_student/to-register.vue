<template>
  <uw-card
    v-if="!isReady || hasRegisterNotices"
    :loaded="isReady" :errored="isErrored"
    :erroredShow="showError"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        To Register For Classes
      </h3>
    </template>
    <template #card-body>
      <div v-if="formatted_date">
        <strong>Register on {{ formatted_date }} through
          <a target="_blank" href="https://uwstudent.washington.edu/student/myplan/mplogin/netid?rd=/student/myplan/">MyPlan</a>
          or
          <a target="_blank" href="https://sdb.admin.uw.edu/students/uwnetid/register.asp">the registration screen</a>.
        </strong>
        <ul>
          <li>
            <a href="https://depts.washington.edu/sislearn/registration-resources/">How to register</a>
          </li>
          <li>
            <a href="http://www.washington.edu/uaa/advising/academic-planning/choosing-courses/overview/">How to choose courses</a>
          </li>
        </ul>
      </div>
      <div v-for="notice in orient_after" :key="notice.id_hash">
        <font-awesome-icon :icon="['far', 'circle']" />
        <h4 class="h6 font-weight-bold" v-html="notice.notice_title" />
        <div class="mb-4 myuw-text-md" v-html="notice.notice_body" />
      </div>
      <div v-for="notice in iss_before" :key="notice.id_hash">
        <font-awesome-icon :icon="['far', 'circle']" />
        <h4 class="h6 font-weight-bold" v-html="notice.notice_title" />
        <div class="mb-4 myuw-text-md" v-html="notice.notice_body" />
      </div>
      <div v-for="notice in iss_after" :key="notice.id_hash">
        <font-awesome-icon :icon="['fas', 'check-circle']" />
        <span class="mb-4 myuw-text-md" v-html="notice.notice_content" />
      </div>
      <div v-for="notice in measles_before" :key="notice.id_hash">
        <font-awesome-icon :icon="['far', 'circle']" />
        <h4 class="h6 font-weight-bold" v-html="notice.notice_title" />
        <div class="mb-4 myuw-text-md" v-html="notice.notice_body" />
      </div>
      <div v-for="notice in measles_after" :key="notice.id_hash">
        <font-awesome-icon :icon="['fas', 'check-circle']" />
        <span class="mb-4 myuw-text-md" v-html="notice.notice_content" />
      </div>
      <div v-for="notice in orient_before" :key="notice.id_hash">
        <font-awesome-icon :icon="['far', 'circle']" />
        <h4 class="h6 font-weight-bold" v-html="notice.notice_title" />
        <div class="mb-4 myuw-text-md" v-html="notice.notice_body" />
      </div>
      <div v-if="orient_after.length > 0">
        <font-awesome-icon :icon="['fas', 'check-circle']" />
        <span
          class="mb-4 myuw-text-md"
        > You have registered for an Advising & Orientation Session.
        </span>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    formatted_date: function() {
      let date = false;
      if (this.isReady) {
        if (this.no_orient.length > 0) {
          const noMsgAttr = this.no_orient[0].attributes;
          noMsgAttr.forEach((attribute) => {
            if (attribute.name === 'Date') {
              date = attribute.formatted_value;
            }
          });
        }
      }
      return date;
    },
    ...mapState({
      no_orient: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_no_orient'),
        );
      },
      orient_after: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_orient_after'),
        );
      },
      iss_before: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_iss_before'),
        );
      },
      iss_after: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_iss_after'),
        );
      },
      measles_before: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_measles_before'),
        );
      },
      measles_after: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_measles_after'),
        );
      },
      orient_before: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_orient_before'),
        );
      },
    }),
    ...mapGetters('notices', [
      'isReady',
      'isErrored',
      'hasRegisterNotices',
    ]),
    showError: function() {
      return (this.statusCode == 543);
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
.notice-title, .notice-body-with-title, .non-notice-body-with-title {
  display: block;
}
</style>
